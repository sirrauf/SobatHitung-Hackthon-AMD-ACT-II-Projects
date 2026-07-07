/**
 * SobatHitung — Contact Page Interactions
 */
(function () {
  'use strict';

  var hamburger = document.getElementById('hamburger');
  var navLinks = document.getElementById('navLinks');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function () {
      navLinks.classList.toggle('open');
    });
  }

  var form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var valid = true;

    var fields = [
      { id: 'cName', errId: 'cNameError', validate: function (v) { return v.trim().length >= 2 ? '' : 'Nama minimal 2 karakter.'; } },
      { id: 'cEmail', errId: 'cEmailError', validate: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? '' : 'Format email tidak valid.'; } },
      { id: 'cSubject', errId: 'cSubjectError', validate: function (v) { return v.trim().length >= 2 ? '' : 'Subjek minimal 2 karakter.'; } },
      { id: 'cMessage', errId: 'cMessageError', validate: function (v) { return v.trim().length >= 10 ? '' : 'Pesan minimal 10 karakter.'; } }
    ];

    fields.forEach(function (f) {
      var input = document.getElementById(f.id);
      var error = document.getElementById(f.errId);
      var msg = f.validate(input.value);
      error.textContent = msg;
      input.classList.toggle('error', !!msg);
      if (msg) valid = false;
    });

    if (valid) {
      var toast = document.getElementById('toast');
      toast.classList.add('show');
      form.reset();
      setTimeout(function () { toast.classList.remove('show'); }, 3000);
    }
  });
})();
