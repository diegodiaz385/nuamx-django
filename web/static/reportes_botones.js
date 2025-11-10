/* reportes_botones.js v3 — Usa el núcleo authFetch + publica eventos de reporte
   - Mantiene exactamente el mismo comportamiento de descarga.
   - Si no hay token, intenta refresh vía núcleo; si falla, muestra alerta.
   - Publica "reportes:generated" en éxito para que otros módulos se enteren.
*/
(function () {
  // ----- Utilidades locales -----
  function saveBlobAndDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename || "reporte.xlsx";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function showToast(msg, type = "info") {
    try {
      (window.NUAMX?.toast || alert)(msg);
    } catch { alert(msg); }
    if (type === "error") console.error(msg); else console.log(msg);
  }

  // ----- Descarga con authFetch del núcleo -----
  async function descargar(scope, formato) {
    const authFetch = window.authFetch || window.fetch;

    const params = new URLSearchParams();
    params.set("scope", scope || "diario");
    if (String(formato || "xlsx").toLowerCase() === "xlsx") params.set("fmt", "xlsx");
    if (String(formato || "").toLowerCase() === "csv")  params.set("fmt", "csv");

    const url = `/api/reportes/export/?${params.toString()}`;

    try {
      const res = await authFetch(url, { method: "GET" });
      if (!res.ok) {
        const txt = await res.text().catch(()=>"(sin cuerpo)");
        showToast(`No se pudo generar el reporte (${res.status}). ${txt}`, "error");
        return;
      }

      const disp = res.headers.get("Content-Disposition") || "";
      const isCSV = /text\/csv/i.test(res.headers.get("Content-Type") || "") || /fmt=csv/.test(url);
      let filename = isCSV ? "reporte.csv" : "reporte.xlsx";
      const m = /filename\*?=(?:UTF-8'')?("?)([^";]+)\1/i.exec(disp);
      if (m && m[2]) filename = decodeURIComponent(m[2]);

      const blob = await res.blob();
      saveBlobAndDownload(blob, filename);

      // Avisar a otras vistas
      try { window.NUAMX?.bus?.publish("reportes:generated", { scope, fmt: isCSV ? "csv" : "xlsx", filename }); } catch {}
    } catch (e) {
      console.error(e);
      showToast("Error de red al generar el reporte.", "error");
    }
  }

  // ----- Wireup de botones (data-scope / data-fmt) -----
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("button.btn[data-scope]").forEach(btn => {
      btn.addEventListener("click", async (ev) => {
        ev.preventDefault();
        const scope = btn.getAttribute("data-scope") || "diario";
        const fmt   = (btn.getAttribute("data-fmt") || "xlsx").toLowerCase();
        await descargar(scope, fmt);
      });
    });
  });
})();
