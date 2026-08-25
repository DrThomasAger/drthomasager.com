/* Theme morphing, mailing-list signup, and the timed popup. */
(function () {
  /* ---- Signup forms (hero, popup) ---- */
  var SUBSCRIBED_KEY = "dta-subscribed";
  function wireForm(form) {
    form.addEventListener("submit", function (e) {
      var placeholder = form.getAttribute("action") === "#";
      if (placeholder) e.preventDefault();
      var interests = [].map.call(
        form.querySelectorAll('input[name="tag"]:checked'),
        function (i) { return i.value; });
      localStorage.setItem(SUBSCRIBED_KEY, JSON.stringify({
        when: new Date().toISOString(), interests: interests
      }));
      form.classList.add("signup-done");
      var note = form.querySelector(".reassure");
      if (note) note.textContent =
        "Welcome. Your first email is on its way. (-:";
      var pop = document.getElementById("popup");
      if (pop && pop.contains(form)) {
        setTimeout(function () { pop.hidden = true; }, 2200);
      }
    });
  }
  [].forEach.call(document.querySelectorAll("form[data-signup]"), wireForm);

  /* ---- Popup: optimal timing ----
     Shows once per visitor at whichever comes first:
     33 seconds of reading, 55% scroll depth, or exit intent.
     Never for subscribers; dismissal rests it for 11 days. */
  var popup = document.getElementById("popup");
  if (!popup) return;
  var DISMISS_KEY = "dta-popup-dismissed";
  var shown = false;

  function eligible() {
    if (shown || localStorage.getItem(SUBSCRIBED_KEY)) return false;
    var d = localStorage.getItem(DISMISS_KEY);
    if (d && (Date.now() - Number(d)) < 11 * 24 * 60 * 60 * 1000) return false;
    return true;
  }
  function show() {
    if (!eligible()) return;
    shown = true;
    popup.hidden = false;
  }
  function dismiss() {
    popup.hidden = true;
    localStorage.setItem(DISMISS_KEY, String(Date.now()));
  }
  document.getElementById("popup-close").addEventListener("click", dismiss);
  [].forEach.call(document.querySelectorAll("[data-open-popup]"), function (b) {
    b.addEventListener("click", function () { popup.hidden = false; shown = true; });
  });
  popup.addEventListener("click", function (e) {
    if (e.target === popup) dismiss();
  });
  setTimeout(show, 33000);
  window.addEventListener("scroll", function () {
    var depth = (window.scrollY + window.innerHeight) /
      document.documentElement.scrollHeight;
    if (depth > 0.55) show();
  }, { passive: true });
  document.addEventListener("mouseout", function (e) {
    if (!e.relatedTarget && e.clientY <= 0) show();
  });
})();
