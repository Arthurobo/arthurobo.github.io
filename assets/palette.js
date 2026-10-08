// palette.js: the only script on the site. It remembers the palette chosen in
// the footer (a class on <html>, see palettes.css) in localStorage. A one-line
// inline script in <head> re-applies it before first paint so nothing flashes.
(function () {
  var KEY = "palette";
  var NAMES = ["graphite", "midnight", "terminal", "ember", "daylight"];

  function apply(name) {
    if (NAMES.indexOf(name) < 0) name = NAMES[0];
    var html = document.documentElement;
    NAMES.forEach(function (n) { html.classList.remove("p-" + n); });
    html.classList.add("p-" + name);
    document.querySelectorAll(".palette-option").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-palette") === name));
    });
    var label = document.querySelector(".palette-current");
    if (label) label.textContent = name.charAt(0).toUpperCase() + name.slice(1);
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".palette-option");
    if (!b) return;
    var name = b.getAttribute("data-palette");
    try { localStorage.setItem(KEY, name); } catch (_) {}
    apply(name);
    var d = b.closest("details");
    if (d) d.removeAttribute("open");
  });

  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (_) {}
  apply(saved || NAMES[0]);
})();
