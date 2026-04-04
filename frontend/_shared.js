// ── SHARED ACROSS ALL PAGES ──────────────────────────────────────────────────
// Drop this inline <script> at the top of each page's <script> block.
const API_BASE = "https://gig-shield-ai-punu.onrender.com/api/v1";

function pageURL(page) {
  // page: "onboarding_registration" | "plan_selection" | "worker_dashboard" | "payout_history"
  const base = window.location.href.replace(/\/[^/]+\/code\.html.*$/, "");
  return `${base}/${page}/code.html`;
}

function showToast(msg, type = "success") {
  document.querySelectorAll(".gs-toast").forEach(e => e.remove());
  if (!document.getElementById("gs-anim")) {
    const s = document.createElement("style");
    s.id = "gs-anim";
    s.textContent = `@keyframes gsIn{from{opacity:0;transform:translateY(-14px)}to{opacity:1;transform:translateY(0)}}`;
    document.head.appendChild(s);
  }
  const bg = { success: "#16a34a", error: "#ba1a1a", info: "#00286d", warn: "#b45309" }[type] || "#00286d";
  const el = Object.assign(document.createElement("div"), { className: "gs-toast" });
  el.style.cssText = `position:fixed;top:20px;inset-inline:16px;background:${bg};color:#fff;padding:14px 18px;border-radius:14px;font-weight:600;font-family:Inter,sans-serif;font-size:14px;z-index:9999;text-align:center;box-shadow:0 8px 24px rgba(0,0,0,.2);animation:gsIn .25s ease`;
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3200);
}

function setBtnLoading(btn, loading, orig) {
  if (loading) { btn.disabled = true; btn._orig = btn.innerHTML; btn.textContent = "Please wait…"; btn.style.opacity = ".65"; }
  else { btn.disabled = false; btn.innerHTML = orig || btn._orig || btn.innerHTML; btn.style.opacity = ""; }
}

function requireAuth() {
  const token = localStorage.getItem("token");
  if (!token) { window.location.href = pageURL("onboarding_registration"); return null; }
  return token;
}
