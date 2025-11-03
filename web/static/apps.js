/* app.js v8 — DEMO funcional sin backend
   - Usuarios/Roles (localStorage) → add, export, clear, change, remove
   - Plantilla editable y descargas CSV
   - Reportes / Búsqueda / Carga masiva (demo)
*/
(function () {
  window.NUAMX_VERSION = "v8";
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $all = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  // ---------- Utils ----------
  function toast(msg, type = "info") {
    try {
      let t = document.createElement("div");
      t.textContent = msg;
      t.className = "fixed bottom-4 right-4 bg-white border border-gray-200 shadow-xl rounded-lg px-2.5 py-1.5 text-sm z-[9999]";
      if (type === "success") t.classList.add("ring-2", "ring-green-200");
      if (type === "error") t.classList.add("ring-2", "ring-red-200");
      document.body.appendChild(t);
      setTimeout(() => t.remove(), 2200);
    } catch (e) { console.log("[toast]", msg); }
  }
  function toCSV(rows) {
    return rows.map(r => r.map(v => {
      const s = String(v ?? "");
      if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
      return s;
    }).join(",")).join("\n");
  }
  function downloadCSV(filename, rows) {
    const csv = toCSV(rows);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }
  function navTo(href) { if (href) window.location.href = href; }

  // ---------- Dashboard / Reportes / Búsqueda ----------
  function handleDownloadUltimasCargas() {
    const rows = [
      ["Fecha", "Usuario", "Registros", "Tipo", "Observaciones", "Estado"],
      ["04-09-2025 10:12", "admin@nuamx.com", 1200, "XLSX", "0 duplicados", "Completado"],
      ["03-09-2025 18:41", "analista@nuamx.com", 650, "CSV", "12 advertencias (montos)", "Advertencias"],
      ["02-09-2025 09:02", "admin@nuamx.com", 0, "Manual", "Error de formato", "Fallida"],
    ];
    downloadCSV("ultimas_cargas.csv", rows);
    toast("Se descargó ultimas_cargas.csv", "success");
  }
  function handleGenerateReport(periodo) {
    const now = new Date().toISOString().slice(0, 10);
    const rows = [
      ["Generado", now],
      [],
      ["RUT", "Razón social", "Periodo", "Tipo", "Folio", "Monto", "Estado"],
      ["11.111.111-1", "Ejemplo SpA", "2025-02", "Factura", "123456", 1500000, "Válida"],
      ["22.222.222-2", "Otro Ltda.", "2025-02", "Boleta", "778899", 250000, "Con advertencias"],
    ];
    downloadCSV(`reporte_${periodo}.csv`, rows);
    toast(`Reporte ${periodo} generado`, "success");
  }
  function handleSearchDemo() {
    const rut = $("#f_rut")?.value || "";
    const nombre = $("#f_nombre")?.value || "";
    const periodo = $("#f_periodo")?.value || "";
    const tipo = $("#f_tipo")?.value || "";
    const estado = $("#f_estado")?.value || "";
    const folio = $("#f_folio")?.value || "";
    const montoMin = $("#f_monto_min")?.value || "";
    const rows = [
      ["RUT", "Razón social", "Periodo", "Tipo", "Folio", "Monto", "Estado"],
      ["11.111.111-1", "Ejemplo SpA", "2025-02", "Factura", "123456", 1500000, "Válida"],
      ["22.222.222-2", "Otro Ltda.", "2025-02", "Boleta", "778899", 250000, "Con advertencias"],
    ];
    downloadCSV("resultado_busqueda.csv", rows);
    toast(`Búsqueda ejecutada. rut=${rut} nombre=${nombre} periodo=${periodo} tipo=${tipo} estado=${estado} folio=${folio} montoMin=${montoMin}`, "success");
  }

  // ---------- Carga masiva: archivo ----------
  function handleUploadDemo() {
    const input = $("#file_masivo");
    if (!input || !input.files || !input.files.length) { toast("Selecciona un archivo CSV/XLSX primero.", "error"); return; }
    const file = input.files[0];
    const resumen = [
      ["Archivo", file.name],
      ["Tamaño (KB)", Math.round(file.size / 1024)],
      ["Registros OK", 1200],
      ["Advertencias", 12],
      ["Errores", 0],
      ["Duplicados", 0],
    ];
    downloadCSV("resumen_carga_masiva.csv", resumen);
    toast("Carga masiva validada (demo). Se descargó el resumen.", "success");
    input.value = "";
  }

  // ---------- Carga masiva: plantilla editable ----------
  function toggleTemplate() {
    const wrap = $("#plantilla_wrap");
    if (!wrap) { toast("No se encontró la plantilla editable en esta página.", "error"); return; }
    const isHidden = wrap.hasAttribute("hidden") || wrap.style.display === "none";
    if (isHidden) {
      wrap.removeAttribute("hidden");
      wrap.style.display = "";
      const tbody = $("#plantilla_table tbody");
      if (tbody && !tbody.children.length) addTemplateRow();
      toast("Plantilla editable visible.", "success");
    } else {
      wrap.setAttribute("hidden", "");
      wrap.style.display = "none";
      toast("Plantilla editable oculta.", "success");
    }
  }
  function addTemplateRow(prefill) {
    const tpl = $("#tpl_row");
    const tbody = $("#plantilla_table tbody");
    if (!tpl || !tbody) return;
    const node = tpl.content.firstElementChild.cloneNode(true);
    if (prefill && Array.isArray(prefill)) {
      const inputs = $all("input, select", node);
      inputs[0].value = prefill[0] ?? "";
      inputs[1].value = prefill[1] ?? "";
      inputs[2].value = prefill[2] ?? "";
      inputs[3].value = prefill[3] ?? "";
      inputs[4].value = prefill[4] ?? "";
      inputs[5].value = prefill[5] ?? "";
      inputs[6].value = prefill[6] ?? "";
      inputs[7].value = prefill[7] ?? "";
    }
    tbody.appendChild(node);
  }
  function clearTemplate() {
    const tbody = $("#plantilla_table tbody");
    if (!tbody) return;
    tbody.innerHTML = "";
    addTemplateRow();
    toast("Plantilla limpiada.", "success");
  }
  function serializeTemplateToRows() {
    const tbody = $("#plantilla_table tbody");
    if (!tbody) return [];
    const rows = [];
    rows.push(["rut","razon_social","periodo","tipo_instrumento","folio","monto","estado_validacion","observaciones"]);
    for (const tr of $all("tr", tbody)) {
      const cells = $all("td", tr);
      if (!cells.length) continue;
      const vals = [];
      vals.push($("input,select", cells[0])?.value?.trim() || "");
      vals.push($("input,select", cells[1])?.value?.trim() || "");
      vals.push($("input,select", cells[2])?.value?.trim() || "");
      vals.push($("input,select", cells[3])?.value?.trim() || "");
      vals.push($("input,select", cells[4])?.value?.trim() || "");
      vals.push($("input,select", cells[5])?.value?.trim() || "");
      vals.push($("input,select", cells[6])?.value?.trim() || "");
      vals.push($("input,select", cells[7])?.value?.trim() || "");
      if (vals.every(v => v === "")) continue;
      rows.push(vals);
    }
    return rows;
  }
  function basicValidate(rows) {
    const header = rows[0] || [];
    const required = ["rut","razon_social","periodo","tipo_instrumento","folio","monto","estado_validacion","observaciones"];
    const missing = required.filter((k, i) => (header[i] || "").toLowerCase() !== k);
    const out = { ok: 0, warnings: 0, errors: 0, duplicates: 0 };
    if (missing.length) { out.errors++; return { ...out, header_error: `Encabezados inválidos: faltan/orden incorrecto (${missing.join(", ")})` }; }
    const seenKey = new Set();
    for (let i = 1; i < rows.length; i++) {
      const r = rows[i]; if (!r) continue;
      const [rut, razon, periodo, tipo, folio, monto, estado] = r;
      if (!rut || !razon || !periodo || !tipo || !folio || !monto || !estado) { out.errors++; continue; }
      if (!/^\d{4}-\d{2}$/.test(periodo)) out.warnings++;
      if (isNaN(Number(monto))) out.warnings++;
      const key = `${rut}|${periodo}|${tipo}|${folio}`;
      if (seenKey.has(key)) out.duplicates++; else seenKey.add(key);
      out.ok++;
    }
    return out;
  }
  function validateTemplateAndDownloadSummary() {
    const rows = serializeTemplateToRows();
    if (rows.length <= 1) { toast("La plantilla está vacía.", "error"); return; }
    const res = basicValidate(rows);
    const resumen = [
      ["Registros OK", res.ok],
      ["Advertencias", res.warnings],
      ["Errores", res.errors],
      ["Duplicados", res.duplicates],
    ];
    if (res.header_error) resumen.unshift(["Encabezado", res.header_error]);
    downloadCSV("resumen_carga_masiva.csv", resumen);
    toast("Validación completada. Se descargó el resumen.", "success");
  }
  function exportTemplateCSV() {
    const rows = serializeTemplateToRows();
    if (rows.length <= 1) { toast("No hay filas con datos para exportar.", "error"); return; }
    downloadCSV("plantilla_editable.csv", rows);
    toast("Se exportó la plantilla a CSV.", "success");
  }

  // ---------- Usuarios / Roles (localStorage) ----------
  const LS_KEY = "nuamx_roles_v1";
  function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email || "").trim());
  }
  function seedRoles() {
    const demo = [{ email: "admin@nuamx.com", role: "Administrador" }];
    saveRoles(demo);
    return demo;
  }
  function loadRoles() {
    try {
      const raw = localStorage.getItem(LS_KEY);
      if (!raw) return seedRoles();
      const data = JSON.parse(raw);
      if (!Array.isArray(data)) return seedRoles();
      return data;
    } catch { return seedRoles(); }
  }
  function saveRoles(arr) {
    localStorage.setItem(LS_KEY, JSON.stringify(arr || []));
  }
  function renderRoles() {
    const tbody = $("#roles_tbody");
    if (!tbody) return;
    const roles = loadRoles();
    tbody.innerHTML = "";
    for (const item of roles) {
      const tr = document.createElement("tr");
      tr.className = "border-b last:border-0";

      const tdEmail = document.createElement("td");
      tdEmail.className = "p-3 break-all";
      tdEmail.textContent = item.email;

      const tdRole = document.createElement("td");
      tdRole.className = "p-3";
      const sel = document.createElement("select");
      sel.className = "border p-1 rounded";
      sel.setAttribute("data-role-select", item.email);
      ["Administrador","Operador","Consulta"].forEach(r => {
        const opt = document.createElement("option");
        opt.value = r; opt.textContent = r;
        if (r === item.role) opt.selected = true;
        sel.appendChild(opt);
      });
      tdRole.appendChild(sel);

      const tdAcc = document.createElement("td");
      tdAcc.className = "p-3";
      const btnDel = document.createElement("button");
      btnDel.className = "btn-ghost";
      btnDel.textContent = "Quitar";
      btnDel.setAttribute("data-email", item.email);
      btnDel.addEventListener("click", () => {
        const roles = loadRoles().filter(r => r.email.toLowerCase() !== item.email.toLowerCase());
        saveRoles(roles); renderRoles(); toast("Usuario quitado.", "success");
      });
      tdAcc.appendChild(btnDel);

      tr.appendChild(tdEmail); tr.appendChild(tdRole); tr.appendChild(tdAcc);
      tbody.appendChild(tr);
    }
  }
  function handleRolesAdd() {
    const email = $("#role_email")?.value?.trim();
    const role  = $("#role_select")?.value?.trim();
    if (!validateEmail(email)) { toast("Correo inválido.", "error"); return; }
    if (!role) { toast("Selecciona un rol.", "error"); return; }
    const roles = loadRoles();
    if (roles.some(r => r.email.toLowerCase() === email.toLowerCase())) { toast("Ese usuario ya existe.", "error"); return; }
    roles.push({ email, role }); saveRoles(roles); renderRoles();
    $("#role_email").value = ""; $("#role_select").value = "";
    toast("Usuario asignado.", "success");
  }
  function handleRolesExport() {
    const roles = loadRoles();
    if (!roles.length) { toast("No hay usuarios para exportar.", "error"); return; }
    const rows = [["Email","Rol"], ...roles.map(r => [r.email, r.role])];
    downloadCSV("usuarios_roles.csv", rows);
    toast("Se exportó usuarios_roles.csv", "success");
  }
  function handleRolesClear() {
    if (!confirm("¿Seguro que quieres limpiar toda la lista de usuarios/roles?")) return;
    saveRoles([]);
    renderRoles();
    toast("Lista vaciada.", "success");
  }

  if ($("#roles_tbody")) renderRoles();

  // ---------- Enrutador de botones ----------
  document.addEventListener("click", (ev) => {
    const btn = ev.target.closest("[data-api]");
    if (!btn) return;
    const api = btn.getAttribute("data-api");
    if (!api) return;

    ev.preventDefault();
    switch (api) {
      // Dashboard/Reportes/Búsqueda/Carga masiva
      case "download:ultimas-cargas": handleDownloadUltimasCargas(); break;
      case "report:diario":           handleGenerateReport("diario"); break;
      case "report:semanal":          handleGenerateReport("semanal"); break;
      case "report:mensual":          handleGenerateReport("mensual"); break;
      case "search:demo":             handleSearchDemo(); break;
      case "upload:masiva":           handleUploadDemo(); break;

      // Plantilla
      case "template:toggle":         toggleTemplate(); break;
      case "template:add-row":        addTemplateRow(); break;
      case "template:clear":          clearTemplate(); break;
      case "template:export":         exportTemplateCSV(); break;
      case "template:validate":       validateTemplateAndDownloadSummary(); break;

      // Usuarios/Roles
      case "roles:add":               handleRolesAdd(); break;
      case "roles:export":            handleRolesExport(); break;
      case "roles:clear":             handleRolesClear(); break;

      default:
        toast(`Acción no implementada: ${api}`, "error");
    }
  });

  console.log("NUAMX app loaded", window.NUAMX_VERSION);
})();
