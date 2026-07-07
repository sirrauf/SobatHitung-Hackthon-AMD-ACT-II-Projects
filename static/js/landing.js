/**
 * SobatHitung — Landing Page Interactions
 * Hamburger menu + scroll-triggered fade-up animations
 */
(function () {
  "use strict";

  // Hamburger toggle
  var hamburger = document.getElementById("hamburger");
  var navLinks = document.getElementById("navLinks");
  if (hamburger && navLinks) {
    hamburger.addEventListener("click", function () {
      navLinks.classList.toggle("open");
    });
  }

  // Scroll-triggered fade-up animations with stagger
  var fadeEls = document.querySelectorAll(".fade-up");
  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            // Stagger based on sibling index
            var parent = entry.target.parentElement;
            var siblings = Array.from(parent.querySelectorAll(".fade-up"));
            var idx = siblings.indexOf(entry.target);
            setTimeout(function () {
              entry.target.classList.add("visible");
            }, idx * 80);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 },
    );

    fadeEls.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    // Fallback: show everything
    fadeEls.forEach(function (el) {
      el.classList.add("visible");
    });
  }
})();
