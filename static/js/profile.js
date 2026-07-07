/**
 * SobatHitung — Profile Page Interactions
 */
(function () {
  'use strict';

  // Hamburger
  var hamburger = document.getElementById('hamburger');
  var navLinks = document.getElementById('navLinks');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function () {
      navLinks.classList.toggle('open');
    });
  }

  // Toggle switches
  document.querySelectorAll('.toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      this.classList.toggle('on');
    });
  });

  // Profile form
  var form = document.getElementById('profileForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      alert('Profil berhasil disimpan! (Prototype — belum terhubung backend)');
    });
  }
})();
