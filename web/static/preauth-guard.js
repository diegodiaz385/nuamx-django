/* preauth-guard.js — Cargar PRIMERO en <head>
   Objetivo: Garantizar credenciales y Authorization en llamadas API incluso
   si páginas legadas usan fetch/axios/XMLHttpRequest antes de app.js.
   - Same-origin: añade credentials:'same-origin'
   - Usa access token desde (local/sessionStorage o cookies)
   - Auto-refresh con /api/token/refresh/ en 401/403 (si hay refresh)
*/

(function(){
  // -------- Token helpers (idéntico espíritu a app.js; sin depender de él)
  const TOKEN_KEYS   = ["nuamx_token","access","access_token","jwt","token"];
  const REFRESH_KEYS = ["nuamx_refresh","refresh","refresh_token","token_refresh"];
  const looksLikeJWT = s => (typeof s === "string" && s.split(".").length === 3);

  function readCookie(name){
    try{
      const m = document.cookie.match(new RegExp("(^| )"+name+"=([^;]+)"));
      return m ? decodeURIComponent(m[2]) : null;
    }catch{ return null; }
  }
  function pickAccessFrom(raw){
    if (!raw) return null;
    try{
      const o = typeof raw==="string" ? JSON.parse(raw) : raw;
      if (o && typeof o === "object"){
        if (o.access && looksLikeJWT(o.access)) return o.access;
        if (o.token  && looksLikeJWT(o.token))  return o.token;
      }
    }catch{
      if (looksLikeJWT(raw)) return raw;
    }
    return null;
  }
  function getAccessToken(){
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
      try{ const o1 = JSON.parse(v1||"null"); if (o1 && looksLikeJWT(o1.refresh)) return o1.refresh; }catch{}
      const v2 = sessionStorage.getItem(k);
      if (v2 && looksLikeJWT(v2)) return v2;
      try{ const o2 = JSON.parse(v2||"null"); if (o2 && looksLikeJWT(o2.refresh)) return o2.refresh; }catch{}
      const v3 = readCookie(k); if (v3 && looksLikeJWT(v3)) return v3;
    }
    return null;
  }
  async function refreshAccess(){
    const refresh = getRefreshToken();
    if (!refresh) return null;
    try{
      const r = await fetch("/api/token/refresh/", {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        credentials:"same-origin",
        body: JSON.stringify({ refresh })
      });
      if (!r.ok) return null;
      const data = await r.json();
      const access = data.access || data.token;
      if (access && looksLikeJWT(access)){
        try{ localStorage.setItem("nuamx_token", JSON.stringify({ access })); }catch{}
        try{ localStorage.setItem("access", access); }catch{}
        document.cookie = `access=${access}; Path=/; SameSite=Lax`;
        return access;
      }
      return null;
    }catch{ return null; }
  }

  function isSameOrigin(url){
    try{
      const u = new URL(url, location.origin);
      return u.origin === location.origin;
    }catch{
      // Rutas relativas => same-origin
      return true;
    }
  }

  // ===============================
  // GUARD #1 — fetch (universal)
  // ===============================
  (function wrapFetch(){
    if (!window.fetch) return;
    const nativeFetch = window.fetch.bind(window);

    window.fetch = async function(input, init){
      const reqUrl = typeof input === "string" ? input : (input && input.url) || "";
      const same = isSameOrigin(reqUrl);
      const opts = Object.assign({ method:"GET" }, init||{});
      const headers = new Headers(opts.headers || {});
      if (same){
        // credenciales por defecto
        if (!opts.credentials) opts.credentials = "same-origin";
        // Authorization si hay token
        const token = getAccessToken();
        if (token && !headers.has("Authorization")) headers.set("Authorization", "Bearer " + token);
      }
      if (!headers.has("Accept")) headers.set("Accept","application/json, text/plain, */*");
      opts.headers = headers;

      let res = await nativeFetch(input, opts);

      if ((res.status===401 || res.status===403) && same){
        const fresh = await refreshAccess();
        if (fresh){
          headers.set("Authorization", "Bearer " + fresh);
          res = await nativeFetch(input, Object.assign({}, opts, { headers }));
        }
      }
      return res;
    };
  })();

  // ===============================
  // GUARD #2 — Axios (si existe)
  // ===============================
  (function wrapAxios(){
    const ax = window.axios || window.Axios;
    if (!ax || !ax.interceptors) return;

    ax.interceptors.request.use(async (config)=>{
      try{
        if (isSameOrigin(config.url||"")){
          const token = getAccessToken();
          config.headers = config.headers || {};
          if (token && !config.headers['Authorization']) config.headers['Authorization'] = 'Bearer ' + token;
          if (config.withCredentials === undefined) config.withCredentials = true;
        }
      }catch{}
      return config;
    });

    ax.interceptors.response.use(
      (resp)=>resp,
      async (error)=>{
        try{
          const cfg = error?.config || {};
          if (cfg.__retried) throw error;
          if ((error?.response?.status===401 || error?.response?.status===403) && isSameOrigin(cfg.url||"")){
            const fresh = await refreshAccess();
            if (fresh){
              cfg.__retried = true;
              cfg.headers = cfg.headers || {};
              cfg.headers['Authorization'] = 'Bearer ' + fresh;
              if (cfg.withCredentials === undefined) cfg.withCredentials = true;
              return (window.axios || ax)(cfg);
            }
          }
        }catch{}
        throw error;
      }
    );
  })();

  // =========================================
  // GUARD #3 — XMLHttpRequest (muy legacy)
  // =========================================
  (function wrapXHR(){
    const NativeXHR = window.XMLHttpRequest;
    if (!NativeXHR) return;

    function sameOrigin(url){ return isSameOrigin(url); }

    function PatchedXHR(){
      const xhr = new NativeXHR();
      let _url = null;

      const origOpen = xhr.open;
      xhr.open = function(method, url, async, user, password){
        _url = url;
        return origOpen.apply(xhr, arguments);
      };

      const origSend = xhr.send;
      xhr.send = async function(body){
        try{
          if (sameOrigin(_url||"")){
            try{ xhr.withCredentials = true; }catch{}
            const token = getAccessToken();
            if (token) try{ xhr.setRequestHeader("Authorization", "Bearer " + token); }catch{}
          }
        }catch{}
        return origSend.apply(xhr, arguments);
      };

      return xhr;
    }

    // Sustituir constructor global conservando constantes/prototipo
    window.XMLHttpRequest = function(){ return PatchedXHR(); };
    window.XMLHttpRequest.UNSENT = NativeXHR.UNSENT;
    window.XMLHttpRequest.OPENED = NativeXHR.OPENED;
    window.XMLHttpRequest.HEADERS_RECEIVED = NativeXHR.HEADERS_RECEIVED;
    window.XMLHttpRequest.LOADING = NativeXHR.LOADING;
    window.XMLHttpRequest.DONE = NativeXHR.DONE;
    window.XMLHttpRequest.prototype = NativeXHR.prototype;
  })();

  // Fin preauth-guard
})();
