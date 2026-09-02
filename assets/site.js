(function () {
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (id) { return document.getElementById(id); };

  /* ── year ── */
  var yr = $("yr");
  if (yr) yr.textContent = new Date().getFullYear();

  /* ── mobile menu ── */
  var burger = $("navBurger");
  var mobileMenu = $("mobileMenu");
  if (burger && mobileMenu) {
    var closeMenu = function () {
      burger.setAttribute("aria-expanded", "false");
      burger.setAttribute("aria-label", "Open menu");
      mobileMenu.hidden = true;
    };
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      burger.setAttribute("aria-label", open ? "Open menu" : "Close menu");
      mobileMenu.hidden = open;
    });
    mobileMenu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeMenu);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeMenu();
    });
    document.addEventListener("click", function (event) {
      if (burger.getAttribute("aria-expanded") === "true" &&
          !burger.contains(event.target) && !mobileMenu.contains(event.target)) {
        closeMenu();
      }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 720) closeMenu();
    });
  }

  /* ── word-by-word statement reveal (about page) ── */
  var statement = $("statement");
  if (statement) {
    (function splitWords() {
      var out = [];
      statement.childNodes.forEach(function (node) {
        var gold = node.nodeType === 1 && node.classList.contains("g");
        var text = node.textContent;
        text.split(/\s+/).forEach(function (w) {
          if (!w) return;
          out.push('<span class="w' + (gold ? " gold" : "") + '">' + w + "</span>");
        });
      });
      statement.innerHTML = out.join(" ");
    })();
    var words = statement.querySelectorAll(".w");
    var litWords = function () {
      var r = statement.getBoundingClientRect();
      var vh = window.innerHeight;
      var p = (vh * 0.85 - r.top) / (vh * 0.5 + r.height);
      p = Math.max(0, Math.min(1, p));
      var n = Math.round(p * words.length);
      words.forEach(function (w, i) { w.classList.toggle("lit", i < n); });
    };
    if (!reduceMotion) {
      window.addEventListener("scroll", litWords, { passive: true });
      litWords();
    } else {
      words.forEach(function (w) { w.classList.add("lit"); });
    }
  }

  /* ── reveal on scroll ── */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  document.querySelectorAll(".reveal, .speech-order").forEach(function (el) { io.observe(el); });

  /* ── calendar: search / filters + persistent notes (calendar page) ── */
  var search = $("calendarSearch");
  var monthSel = $("calendarMonth");
  var locSel = $("calendarLocation");
  var rowsHost = $("calendarRows");
  if (search && monthSel && locSel && rowsHost) {
    var rows = Array.prototype.slice.call(rowsHost.querySelectorAll("tr"));
    var empty = $("calendarEmpty");
    var countNum = $("calCountNum");
    if (countNum) countNum.textContent = rows.length;

    var applyFilters = function () {
      var q = (search.value || "").trim().toLowerCase();
      var m = monthSel.value;
      var l = locSel.value;
      var visible = 0;
      rows.forEach(function (tr) {
        var hit =
          (!m || tr.getAttribute("data-month") === m) &&
          (!l || tr.getAttribute("data-location") === l) &&
          (!q || tr.textContent.toLowerCase().indexOf(q) !== -1);
        tr.style.display = hit ? "" : "none";
        if (hit) visible++;
      });
      if (empty) empty.classList.toggle("show", visible === 0);
      if (countNum) countNum.textContent = visible;
    };
    search.addEventListener("input", applyFilters);
    monthSel.addEventListener("change", applyFilters);
    locSel.addEventListener("change", applyFilters);
  }

  var noteBoxes = document.querySelectorAll(".note-box");
  if (noteBoxes.length) {
    var NOTES_KEY = "prospect-calendar-notes";
    var saved = {};
    try { saved = JSON.parse(localStorage.getItem(NOTES_KEY) || "{}"); } catch (e) { saved = {}; }
    noteBoxes.forEach(function (box) {
      var key = box.getAttribute("data-note-key");
      if (saved[key]) box.textContent = saved[key];
      box.addEventListener("input", function () {
        saved[key] = box.textContent.trim();
        if (!saved[key]) delete saved[key];
        try { localStorage.setItem(NOTES_KEY, JSON.stringify(saved)); } catch (e) {}
      });
      box.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter") { ev.preventDefault(); box.blur(); }
      });
    });
  }
})();
