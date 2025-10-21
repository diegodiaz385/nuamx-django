// web/static/app.js
(function(){
  function getCSRF(){
    const m = document.querySelector('meta[name="csrf-token"]');
    return m ? m.getAttribute('content') : '';
  }
  async function api(url, method="GET", body=null){
    const headers = {"Accept":"application/json"};
    if (method !== "GET") {
      headers["Content-Type"] = "application/json";
      headers["X-CSRFToken"] = getCSRF();
    }
    const res = await fetch(url, {method, headers, body: body ? JSON.stringify(body) : null});
    return await res.json();
  }

  // click genérico: <button data-api="ping"> o <button data-api="login" data-email="..." data-password="...">
  document.addEventListener("click", async (e)=>{
    const btn = e.target.closest("[data-api]");
    if (!btn) return;
    e.preventDefault();

    const action = btn.getAttribute("data-api");
    try {
      if (action === "ping") {
        const r = await api("/api/ping/");
        alert("PING → " + JSON.stringify(r));
      }
      if (action === "login") {
        const email = btn.getAttribute("data-email") || document.querySelector("#email")?.value;
        const password = btn.getAttribute("data-password") || document.querySelector("#password")?.value;
        const r = await api("/api/login/", "POST", {email, password});
        alert("LOGIN → " + JSON.stringify(r));
      }
      if (action === "roles") {
        const r = await api("/api/roles/");
        console.log("ROLES", r);
        alert("ROLES → " + (r?.data?.roles?.map(x=>x.nombre).join(", ") || "sin datos"));
      }
    } catch (err){
      console.error(err);
      alert("Error llamando API");
    }
  });
})();
