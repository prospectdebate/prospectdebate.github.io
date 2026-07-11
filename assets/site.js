(function () {
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (id) { return document.getElementById(id); };

  /* ── year ── */
  var yr = $("yr");
  if (yr) yr.textContent = new Date().getFullYear();

  /* ── nav scrolled state ── */
  var nav = $("nav");

  /* ── mobile menu ── */
  var burger = $("navBurger");
  var mobileMenu = $("mobileMenu");
  if (burger && mobileMenu) {
    var closeMenu = function () {
      burger.setAttribute("aria-expanded", "false");
      mobileMenu.classList.remove("open");
    };
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      mobileMenu.classList.toggle("open", !open);
    });
    mobileMenu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeMenu);
    });
  }

  /* ── hero parallax + prep clock (single rAF loop) ── */
  var heroBg = $("heroBg");
  var heroContent = $("heroContent");
  var clock = $("prepClock");
  var pcTime = $("pcTime");
  var ticking = false;

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var y = window.scrollY || 0;
      var vh = window.innerHeight;

      if (nav) nav.classList.toggle("scrolled", y > 40);

      /* hero: bg zooms slowly, content parallaxes up + fades */
      if (heroBg && heroContent && !reduceMotion && y < vh * 1.4) {
        var p = Math.min(1, y / vh);
        heroBg.style.transform = "scale(" + (1 + p * 0.14) + ") translateY(" + p * 4 + "%)";
        heroContent.style.transform = "translateY(" + (-p * 46) + "px)";
        heroContent.style.opacity = String(1 - p * 1.15);
      }

      /* prep clock: 20:00 -> 00:00 across the full page scroll */
      if (clock && pcTime) {
        var max = document.documentElement.scrollHeight - vh;
        var total = max > 0 ? Math.min(1, y / max) : 0;
        var secs = Math.round(1200 * (1 - total));
        var m = Math.floor(secs / 60), s = secs % 60;
        pcTime.textContent = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
        clock.classList.toggle("on", y > vh * 0.4 && total < 0.985);
      }

      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

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
