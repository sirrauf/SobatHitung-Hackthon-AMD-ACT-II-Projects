/**
 * SobatHitung — Auth Pages (Register, Login, Forgot Password)
 * Shared across register.html, login.html, forgot-password.html
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

  // Register form
  var regForm = document.getElementById('registerForm');
  if (regForm) {
    regForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var valid = true;

      var fields = [
        { id: 'rName', errId: 'rNameError', check: function (v) { return v.trim().length >= 2 ? '' : 'Nama minimal 2 karakter.'; } },
        { id: 'rEmail', errId: 'rEmailError', check: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? '' : 'Format email tidak valid.'; } },
        { id: 'rPassword', errId: 'rPasswordError', check: function (v) { return v.length >= 8 ? '' : 'Password minimal 8 karakter.'; } },
        { id: 'rPasswordConfirm', errId: 'rPasswordConfirmError', check: function (v) { return v === document.getElementById('rPassword').value ? '' : 'Password tidak cocok.'; } }
      ];

      fields.forEach(function (f) {
        var input = document.getElementById(f.id);
        var error = document.getElementById(f.errId);
        var msg = f.check(input.value);
        error.textContent = msg;
        input.classList.toggle('error', !!msg);
        if (msg) valid = false;
      });

      var terms = document.getElementById('rTerms');
      var termsErr = document.getElementById('rTermsError');
      if (!terms.checked) { termsErr.textContent = 'Anda harus menyetujui syarat dan ketentuan.'; valid = false; }
      else { termsErr.textContent = ''; }

      if (valid) {
        alert('Registrasi berhasil! (Prototype — belum terhubung backend)');
        window.location.href = '/dashboard';
      }
    });
  }

  // Login form
  var loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var valid = true;
      var email = document.getElementById('lEmail');
      var pass = document.getElementById('lPassword');
      var emailErr = document.getElementById('lEmailError');
      var passErr = document.getElementById('lPasswordError');

      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        emailErr.textContent = 'Format email tidak valid.';
        email.classList.add('error');
        valid = false;
      } else { emailErr.textContent = ''; email.classList.remove('error'); }

      if (pass.value.length < 1) {
        passErr.textContent = 'Password harus diisi.';
        pass.classList.add('error');
        valid = false;
      } else { passErr.textContent = ''; pass.classList.remove('error'); }

      if (valid) {
        alert('Login berhasil! (Prototype — belum terhubung backend)');
        window.location.href = '/dashboard';
      }
    });
  }

  // Forgot password form
  var forgotForm = document.getElementById('forgotForm');
  if (forgotForm) {
    forgotForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = document.getElementById('fpEmail');
      var err = document.getElementById('fpEmailError');

      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        err.textContent = 'Format email tidak valid.';
        email.classList.add('error');
        return;
      }
      err.textContent = '';
      email.classList.remove('error');

      var toast = document.getElementById('toast');
      if (toast) {
        toast.classList.add('show');
        this.reset();
        setTimeout(function () { toast.classList.remove('show'); }, 4000);
      }
    });
  }
})();
