/* app.js v16 — Núcleo compartido: authFetch + Bus de eventos + sesión/rol + utilidades
   - Unifica llamadas a API con refresh automático de JWT.
   - Publica eventos entre módulos/pestañas: users:changed, calificaciones:changed, reportes:generated, session:changed, etc.
   - Recarga suave por defecto si no hay listeners de página.
   - Mantiene helpers y UI toasts existentes de v15.
*/
(function () {
  window.NUAMX_VERSION = "v16";

  // =========================
  // Utilidades básicas (UI)
  // =========================
  const $  = (s, c=document)=>c.querySelector(s);
  const $$ = (s, c=document)=>Array.from((c||document).querySelectorAll(s));

  function toast(msg, type="info"){
    try{
      const t = document.createElement("div");
      t.textContent = msg;
      t.className = "fixed bottom-4 right-4 bg-white border border-gray-200 shadow-xl rounded-lg px-2.5 py-1.5 text-sm z-[9999]";
      if(type==="success") t.classList.add("ring-2","ring-green-200");
      if(type==="error")   t.classList.add("ring-2","ring-red-200");
      document.body.appendChild(t); setTimeout(()=>t.remove(), 2200);
    }catch{ console.log(msg); }
  }

  function fmtDate(v){
    if(!v) return "—";
    try{
      const d = (v instanceof Date) ? v : new Date(String(v));
      if (isNaN(d.getTime())) return String(v);
      // Formato ISO para evitar TZ raras en lista; vistas específicas pueden re-formatear
      return d.toISOString();
    }catch{ return "—"; }
  }

  // CSV helpers usados por Admin/Roles
  function toCSV(rows){
    return rows.map(r => r.map(v => {
      const s = String(v ?? "");
      if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
      return s;
    }).join(",")).join("\n");
  }
  function downloadCSV(filename, rows){
    const blob = new Blob([toCSV(rows)], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
  }

  // Exponer utilidades que otras páginas ya estaban usando implícitamente
  window.NUAMX = window.NUAMX || {};
  Object.assign(window.NUAMX, { fmtDate, toast, downloadCSV });

  // =========================
  // Bus de eventos compartido
  // =========================
  const BUS_CH = "nuamx.bus.v1";

  const bc = (function(){
    try { return new BroadcastChannel(BUS_CH); } catch { return null; }
  })();

  const listeners = new Map(); // topic -> Set<fn>

  function publish(topic, payload){
    const msg = { topic, payload, ts: Date.now(), source: "web" };
    // Local (misma pestaña)
    (listeners.get(topic) || new Set()).forEach(fn => { try{ fn(payload); }catch{} });
    // CustomEvent para scripts inline
    document.dispatchEvent(new CustomEvent("nuamx:"+topic, { detail: payload }));
    // BroadcastChannel (entre pestañas)
    if (bc) try{ bc.postMessage(msg); }catch{}
    // Fallback con localStorage
    try { localStorage.setItem("__nuamx_bus__", JSON.stringify(msg)); localStorage.removeItem("__nuamx_bus__"); }catch{}
  }

  function subscribe(topic, fn){
    if (!listeners.has(topic)) listeners.set(topic, new Set());
    listeners.get(topic).add(fn);
    return () => listeners.get(topic)?.delete(fn);
  }

  // Entradas remotas
  if (bc) bc.onmessage = (ev)=>{ const {topic, payload} = ev.data || {}; if (topic) publish(topic, payload); };
  window.addEventListener("storage", (e)=>{
    if (e.key === "__nuamx_bus__" && e.newValue){
      try{ const {topic, payload} = JSON.parse(e.newValue)||{}; if(topic) publish(topic, payload); }catch{}
    }
  });

  // Exponer el bus
  window.NUAMX.bus = { publish, subscribe };

  // =========================
  // Gestión de tokens
  // =========================
  const TOKEN_KEYS   = ["nuamx_token","access","access_token","jwt","token"];
  const REFRESH_KEYS = ["nuamx_refresh","refresh","refresh_token","token_refresh"];

  const looksLikeJWT = s => (typeof s === "string" && s.split(".").length === 3);

  function readCookie(name) {
    try {
      const m = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
      return m ? decodeURIComponent(m[2]) : null;
    } catch { return null; }
  }

  function pickAccessFrom(raw){
    if (!raw) return null;
    try{
      const o = typeof raw === "string" ? JSON.parse(raw) : raw;
      if (o && typeof o === "object") {
        if (o.access && looksLikeJWT(o.access)) return o.access;
        if (o.token  && looksLikeJWT(o.token))  return o.token;
      }
    }catch{
      if (looksLikeJWT(raw)) return raw;
    }
    return null;
  }

  function getAccessTokenFromStores(){
    for (const k of TOKEN_KEYS){
      const v1 = localStorage.getItem(k); const t1 = pickAccessFrom(v1); if (t1) return t1;
      const v2 = sessionStorage.getItem(k); const t2 = pickAccessFrom(v2); if (t2) return t2;
      const v3 = readCookie(k); const t3 = pickAccessFrom(v3); if (t3) return t3;
    }
    return null;
  }

  function getRefreshToken(){
    for (const k of REFRESH_KEYS){
      const v1 = localStorage.getItem(k);
      if (v1 && looksLikeJWT(v1)) return v1;
      try { const o1 = JSON.parse(v1 || "null"); if (o1 && looksLikeJWT(o1.refresh)) return o1.refresh; }catch{}
      const v2 = sessionStorage.getItem(k);
      if (v2 && looksLikeJWT(v2)) return v2;
      try { const o2 = JSON.parse(v2 || "null"); if (o2 && looksLikeJWT(o2.refresh)) return o2.refresh; }catch{}
      const v3 = readCookie(k); if (v3 && looksLikeJWT(v3)) return v3;
    }
    return null;
  }

  async function refreshAccess(){
    const refresh = getRefreshToken();
    if (!refresh) return null;
    try{
      const res = await fetch("/api/token/refresh/", {
        method:"POST", headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ refresh })
      });
      if (!res.ok) return null;
      const data = await res.json();
      const access = data.access || data.token;
      if (access && looksLikeJWT(access)){
        localStorage.setItem("nuamx_token", JSON.stringify({ access }));
        // Dejar también en 'access' por compatibilidad con tu login.html
        localStorage.setItem("access", access);
        document.cookie = `access=${access}; Path=/; SameSite=Lax`;
        publish("session:changed", { kind:"refreshed" });
        return access;
      }
      return null;
    }catch{ return null; }
  }

  async function getAccessToken(){
    const direct = getAccessTokenFromStores();
    if (direct) return direct;
    return await refreshAccess();
  }

  // ===================================
  // authFetch (único punto de contacto)
  // ===================================
  const MUTATING = new Set(["POST","PATCH","PUT","DELETE"]);

  function guessTopicFromUrl(url){
    try{
      const u = new URL(url, location.origin);
      const p = u.pathname;
      if (/^\/api\/users\/?/i.test(p) || /^\/api\/roles\/assign\/?/i.test(p)) return "users:changed";
      if (/^\/api\/calificaciones\/?/i.test(p)) {
        if (/\/import_(preview|commit)\/?$/i.test(p)) return "calificaciones:changed";
        return "calificaciones:changed";
      }
      if (/^\/api\/reportes\/export\/?/i.test(p)) return "reportes:generated";
      if (/^\/api\/me\/?/i.test(p)) return "session:changed";
    }catch{}
    return null;
  }

  async function authFetch(input, init){
    const req = typeof input === "string" ? input : (input?.url ?? "");
    const opts = Object.assign({ method:"GET" }, init || {});
    const method = (opts.method || "GET").toUpperCase();

    // Añadir Authorization si tenemos token
    let access = await getAccessToken();
    const headers = new Headers(opts.headers || {});
    if (access && !headers.has("Authorization")) headers.set("Authorization", "Bearer " + access);
    if (!headers.has("Accept")) headers.set("Accept", "application/json, text/plain, */*");
    opts.headers = headers;

    // Intento #1
    let res = await fetch(req, opts);

    // Si expira, refrescamos y reintento una vez
    if (res.status === 401 || res.status === 403){
      const fresh = await refreshAccess();
      if (fresh){
        headers.set("Authorization", "Bearer " + fresh);
        res = await fetch(req, Object.assign({}, opts, { headers }));
      }
    }

    // Emitir eventos en éxito de mutaciones
    if (res.ok && MUTATING.has(method)){
      const topic = guessTopicFromUrl(req);
      if (topic) publish(topic, { url:req, method, status:res.status });
    }

    return res;
  }

  // Hacer disponible para todas las vistas (carga-masiva, detalle, admin-roles, reportes)
  window.authFetch = authFetch;

  // =========================
  // Perfil / RBAC (compat)
  // =========================
  const URLS = window.URLS || window.urls || {};
  const URL_ME          = URLS.me           || "/api/me/";
  const URL_LIST        = URLS.users_list   || $("#users_table")?.dataset?.urlList || "/api/users/";
  const URL_ROLE_ASSIGN = URLS.role_assign  || "/api/roles/assign/";
  const URL_CREATE      = URLS.register     || "/api/auth/register/";
  const URL_DETAIL_ZERO = URLS.user_detail0 || "/api/users/0/";
  const URL_PASS_ZERO   = URLS.user_pass0   || "/api/users/0/password/";
  const URL_ROLE_OF     = URLS.role_of      || null;

  const usersDetailUrl = (id)=> URL_DETAIL_ZERO.replace(/0\/?$/, String(id)+"/");
  const userPassUrl    = (id)=> URL_PASS_ZERO ? URL_PASS_ZERO.replace(/\/0(\/|$)/, `/${String(id)}$1`) : null;

  let me = {};
  let flags = { myRole:'Operador', isAdmin:false, isOper:true, isAuditor:false, isUsuario:false };
  const norm = (s)=>String(s||"").toLowerCase();
  const looksAdmin  = (s)=>/\b(superuser|admin|administrador|root)\b/.test(norm(s));
  const looksOper   = (s)=>/\b(oper|operador|operator|staff|editor)\b/.test(norm(s));
  const looksAudit  = (s)=>/\b(auditor|audit)\b/.test(norm(s));
  const looksUser   = (s)=>/\b(usuario|user)\b/.test(norm(s));

  function computeRoleFromMe(m){
    if (m?.is_superuser === true || String(m?.is_superuser).toLowerCase()==="true") return "Administrador";
    if (m?.is_staff     === true || String(m?.is_staff).toLowerCase()==="true")     return "Operador";
    const parts = [];
    ["role","rol","role_name","role_display","tipo","profile_role"].forEach(k=>m?.[k]&&parts.push(m[k]));
    if (Array.isArray(m?.groups)) m.groups.forEach(g=>parts.push(typeof g==="string"?g:(g?.name??"")));
    const blob = parts.filter(Boolean).join(" ");
    if (looksAdmin(blob)) return "Administrador";
    if (looksOper(blob))  return "Operador";
    if (looksAudit(blob)) return "Auditor";
    if (looksUser(blob))  return "Usuario";
    return "Operador";
  }
  function setFlags(role){
    flags = { myRole:role, isAdmin:role==="Administrador", isOper:role==="Operador", isAuditor:role==="Auditor", isUsuario:role==="Usuario" };
    window.NUAMX_RBAC_FLAGS = flags;
    const badge = $("#rbac_badge"); if (badge) badge.textContent = `Rol: ${role}`;
    const createCard = $("#create_card"); if (createCard) createCard.style.display = flags.isAdmin ? "" : "none";
    // informar a vistas
    document.dispatchEvent(new CustomEvent('nuamx:rbac-ready', { detail: flags }));
  }
  async function resolveMe(){
    try{ me = JSON.parse(localStorage.getItem("me")||"{}")||{}; }catch{ me={}; }
    try{ const r = await authFetch(URL_ME); if(r?.ok) me = Object.assign({}, me, await r.json()); }catch{}
    const role = computeRoleFromMe(me);
    try{ localStorage.setItem("me", JSON.stringify(Object.assign({}, me, {role}))); }catch{}
    setFlags(role);
  }

  // Rol por email (cache + endpoint opcional) — compat con Admin/Roles
  const roleCache = new Map(); // email -> rol
  function roleFromUser(u){
    if (u?.email && roleCache.has(u.email)) return roleCache.get(u.email);
    const r = (u?.role) || (u?.roles && u.roles[0]) || u?.rol || u?.role_name || null;
    if (u?.email && r) roleCache.set(u.email, r);
    return r || "Usuario";
  }
  async function fetchRoleByEmail(email){
    if (!email) return null;
    if (roleCache.has(email)) return roleCache.get(email);
    if (!URL_ROLE_OF) return null;
    try{
      const res = await authFetch(URL_ROLE_OF + (URL_ROLE_OF.includes("?")?"&":"?") + "email=" + encodeURIComponent(email));
      if(!res.ok) return null;
      const data = await res.json();
      const r = data?.role || data?.rol || data?.role_name || null;
      if (r){ roleCache.set(email, r); return r; }
      return null;
    }catch{ return null; }
  }

  async function hydrateOneRow(tr, id, email){
    try{
      const r = await authFetch(usersDetailUrl(id));
      if (r?.ok){
        const d = await r.json();
        const roleLocal  = roleFromUser(d);
        const roleRemote = roleLocal || await fetchRoleByEmail(d.email||email);
        const roleFinal  = roleRemote || roleLocal || "Usuario";

        tr.dataset.active = String(!!d.is_active);
        $(".col-email",tr).textContent   = d.email || email || "—";
        $(".col-phone",tr).textContent   = d.phone || d.telefono || "—";
        $(".col-created",tr).textContent = fmtDate(d.created_at || d.date_joined || d.created);
        $(".col-updated",tr).textContent = fmtDate(d.updated_at || d.modified || d.last_login || d.updated);
        $(".col-active",tr).innerHTML    = `<span class="pill">${d.is_active ? "Activo" : "Inactivo"}</span>`;
        $(".col-role",tr).textContent    = roleFinal;
        const tbtn = tr.querySelector('[data-act="toggle"]'); if (tbtn) tbtn.textContent = d.is_active ? "Desactivar" : "Activar";
      }else{
        const r2 = await fetchRoleByEmail(email);
        if (r2) $(".col-role",tr).textContent = r2;
      }
    }catch(_){}
  }

  // =========================
  // Auto-actualización suave
  // =========================
  // Si una página no se suscribe, hacemos una recarga suave (debounced) del módulo actual.
  let reloadTimer = null;
  function softReload(){
    if (reloadTimer) return;
    reloadTimer = setTimeout(()=>{ reloadTimer=null; location.reload(); }, 600);
  }

  // Heurísticas por módulo (no tocan HTML ni agregan JS extra)
  // Las vistas pueden cancelar llamando preventDefault en el CustomEvent "nuamx:auto-reload"
  function maybeAutoReload(topic){
    const ev = new CustomEvent("nuamx:auto-reload", { cancelable:true, detail:{ topic } });
    document.dispatchEvent(ev);
    if (ev.defaultPrevented) return; // la página ya maneja la actualización
    // Si estamos en módulos relativos al topic, recarga suave
    const p = location.pathname;
    if (topic.startsWith("users:") && (/usuarios|admin-roles|\/users/i.test(p))) return softReload();
    if (topic.startsWith("calificaciones:") && (/carga-masiva|detalle|calificaciones/i.test(p))) return softReload();
    if (topic.startsWith("reportes:") && (/reportes/i.test(p))) return; // descarga no necesita recarga
  }

  // Suscripciones globales
  ["users:changed","calificaciones:changed","reportes:generated","session:changed"].forEach(t=>{
    subscribe(t, ()=> maybeAutoReload(t));
  });

  // =========================
  // Boot mínimo para páginas
  // =========================
  (async function init(){
    try{ await resolveMe(); }catch{ setFlags("Operador"); }
    // Exponer helpers de compat para scripts inline existentes
    window.NUAMX._compat = {
      roleCache, roleFromUser, fetchRoleByEmail, hydrateOneRow,
      usersDetailUrl, userPassUrl, URL_LIST, URL_CREATE, URL_ROLE_ASSIGN
    };
  })();

  // =========================
  // Exportar helpers comunes
  // =========================
  window.NUAMX.helpers = Object.assign(window.NUAMX.helpers || {}, {
    $, $$, fmtDate, toCSV, downloadCSV
  });

  // Compat: seguir ofreciendo doFetch como en tus plantillas
  window.doFetch = (url, init) => authFetch(url, init);

  // ========= FIN núcleo =========
})();
