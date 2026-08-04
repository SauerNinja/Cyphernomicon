(function () {
  "use strict";

  /* ---------- Mobile sidebar toggle ---------- */
  var sidebar = document.querySelector(".sidebar");
  var scrim = document.querySelector(".sidebar-scrim");
  var toggles = document.querySelectorAll(".nav-toggle");

  function openSidebar() {
    if (sidebar) sidebar.classList.add("open");
    if (scrim) scrim.classList.add("open");
  }
  function closeSidebar() {
    if (sidebar) sidebar.classList.remove("open");
    if (scrim) scrim.classList.remove("open");
  }
  toggles.forEach(function (t) {
    t.addEventListener("click", function () {
      if (sidebar && sidebar.classList.contains("open")) closeSidebar();
      else openSidebar();
    });
  });
  if (scrim) scrim.addEventListener("click", closeSidebar);

  /* ---------- Desktop collapse/expand ---------- */
  var NAV_KEY = "cyphernomicon-nav";
  document.querySelectorAll("[data-action='collapse-nav']").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.body.classList.add("nav-collapsed");
      try { localStorage.setItem(NAV_KEY, "collapsed"); } catch (e) {}
    });
  });
  document.querySelectorAll("[data-action='expand-nav']").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.body.classList.remove("nav-collapsed");
      try { localStorage.setItem(NAV_KEY, "expanded"); } catch (e) {}
    });
  });

  /* ---------- Highlight current chapter in sidebar ---------- */
  var here = document.body.getAttribute("data-section");
  if (here) {
    document.querySelectorAll(".sidebar__nav a[data-section]").forEach(function (a) {
      if (a.getAttribute("data-section") === here) a.classList.add("active");
    });
  }

  /* ---------- Expand all / collapse all ---------- */
  document.querySelectorAll("[data-action='expand-all']").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll("main details").forEach(function (d) { d.open = true; });
    });
  });
  document.querySelectorAll("[data-action='collapse-all']").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll("main details.chunk").forEach(function (d, i) {
        // keep top-level (depth-1) sections open, collapse the rest
        d.open = d.classList.contains("depth-1");
      });
      document.querySelectorAll("main ul.outline details").forEach(function (d) { d.open = false; });
    });
  });

  /* If a URL hash targets a node inside a collapsed <details>, open its ancestors */
  function revealHash() {
    var id = decodeURIComponent(location.hash || "").slice(1);
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    var p = el.parentElement;
    while (p) {
      if (p.tagName === "DETAILS") p.open = true;
      p = p.parentElement;
    }
    setTimeout(function () { el.scrollIntoView({ block: "start" }); }, 30);
  }
  window.addEventListener("hashchange", revealHash);
  revealHash();

  /* ---------- Search overlay ---------- */
  var overlay = document.getElementById("search-overlay");
  var input = document.getElementById("search-input");
  var results = document.getElementById("search-results");
  var openers = document.querySelectorAll("[data-action='open-search']");
  var ROOT = document.body.getAttribute("data-root") || "";
  var index = null;
  var selIdx = -1;
  var current = [];

  function loadIndex() {
    if (index) return Promise.resolve(index);
    return fetch(ROOT + "assets/data/search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; return data; });
  }

  function openSearch() {
    overlay.classList.add("open");
    loadIndex().then(function () {
      input.focus();
      input.select();
    });
  }
  function closeSearch() {
    overlay.classList.remove("open");
  }
  openers.forEach(function (o) { o.addEventListener("click", openSearch); });
  if (overlay) {
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closeSearch();
    });
  }
  document.addEventListener("keydown", function (e) {
    var isMeta = e.metaKey || e.ctrlKey;
    if (isMeta && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (overlay.classList.contains("open")) closeSearch(); else openSearch();
    } else if (e.key === "/" && document.activeElement.tagName !== "INPUT") {
      e.preventDefault();
      openSearch();
    } else if (e.key === "Escape") {
      closeSearch();
    } else if (overlay && overlay.classList.contains("open")) {
      if (e.key === "ArrowDown") { e.preventDefault(); moveSel(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); moveSel(-1); }
      else if (e.key === "Enter") {
        e.preventDefault();
        if (current[selIdx]) location.href = current[selIdx].href;
      }
    }
  });

  function moveSel(dir) {
    if (!current.length) return;
    selIdx = (selIdx + dir + current.length) % current.length;
    renderSel();
  }
  function renderSel() {
    var nodes = results.querySelectorAll(".search-hit");
    nodes.forEach(function (n, i) { n.classList.toggle("sel", i === selIdx); });
    if (nodes[selIdx]) nodes[selIdx].scrollIntoView({ block: "nearest" });
  }

  function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function highlight(text, q) {
    var re = new RegExp("(" + escRe(q) + ")", "ig");
    return text.replace(re, "<mark>$1</mark>");
  }

  function runSearch(q) {
    selIdx = -1;
    if (!q || q.trim().length < 2) {
      results.innerHTML = '<div class="search-empty">Type at least 2 characters — searches all 20 sections.</div>';
      current = [];
      return;
    }
    var terms = q.toLowerCase().trim().split(/\s+/).filter(Boolean);
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var e = index[i];
      var hay = e.t.toLowerCase();
      var ok = true;
      for (var j = 0; j < terms.length; j++) {
        if (hay.indexOf(terms[j]) === -1) { ok = false; break; }
      }
      if (ok) {
        hits.push(e);
        if (hits.length >= 60) break;
      }
    }
    current = hits.map(function (e) {
      return { href: ROOT + e.h };
    });
    if (!hits.length) {
      results.innerHTML = '<div class="search-empty">No matches. Try different terms.</div>';
      return;
    }
    var html = hits.map(function (e) {
      var snip = e.t.length > 160 ? e.t.slice(0, 160) + "…" : e.t;
      return '<a class="search-hit" href="' + ROOT + e.h + '">' +
        '<span class="path">' + e.p + '</span>' +
        '<span class="snip">' + highlight(escapeHtml(snip), q.trim()) + '</span>' +
        '</a>';
    }).join("");
    results.innerHTML = html;
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  if (input) {
    var t;
    input.addEventListener("input", function () {
      clearTimeout(t);
      var v = input.value;
      t = setTimeout(function () { runSearch(v); }, 90);
    });
  }

  /* ---------- Consent banner (GA4 / Consent Mode v2) ---------- */
  var banner = document.getElementById("consent-banner");
  if (banner) {
    var CONSENT_KEY = "cyphernomicon-consent";
    var saved = null;
    try { saved = localStorage.getItem(CONSENT_KEY); } catch (e) {}
    function setConsent(state) {
      if (typeof gtag === "function") {
        gtag("consent", "update", {
          ad_storage: state, analytics_storage: state,
          ad_user_data: state, ad_personalization: state
        });
      }
      try { localStorage.setItem(CONSENT_KEY, state); } catch (e) {}
    }
    if (!saved) {
      banner.classList.add("show");
    } else {
      setConsent(saved);
    }
    banner.querySelectorAll("[data-consent]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var state = btn.getAttribute("data-consent") === "accept" ? "granted" : "denied";
        setConsent(state);
        banner.classList.remove("show");
      });
    });
  }
})();
