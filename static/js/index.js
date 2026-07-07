/**
 * SobatHitung — Index (Explorer) Page Interactions
 * Sidebar navigation, iframe page loading, keyboard nav, mobile menu
 */
(function () {
  'use strict';

  var frame = document.getElementById('pageFrame');
  var overlay = document.getElementById('loadingOverlay');
  var breadcrumb = document.getElementById('breadcrumb');
  var btnOpenNew = document.getElementById('btnOpenNew');
  var sidebar = document.getElementById('explorerSidebar');
  var overlayEl = document.getElementById('sidebarOverlay');
  var mobileBtn = document.getElementById('mobileMenuBtn');

  var currentPage = 'landing';

  var pageNames = {
    'landing': 'Beranda',
    'about': 'Tentang Kami',
    'contact': 'Hubungi Kami',
    'register': 'Daftar',
    'login': 'Masuk',
    'forgot-password': 'Lupa Password',
    'dashboard': 'Dashboard',
    'profile': 'Profil'
  };

  var pageRoutes = {
    'landing': '/landing',
    'about': '/about',
    'contact': '/contact',
    'register': '/register',
    'login': '/login',
    'forgot-password': '/forgot-password',
    'dashboard': '/dashboard',
    'profile': '/profile'
  };

  var pages = Object.keys(pageNames);

  function navigateTo(page) {
    if (page === currentPage) return;
    currentPage = page;

    // Show loading
    overlay.classList.add('visible');

    // Update iframe
    frame.src = pageRoutes[page] || ('/' + page);

    // Update breadcrumb
    breadcrumb.innerHTML = '<span>SobatHitung</span> / ' + (pageNames[page] || page);

    // Update sidebar active state + aria-current
    document.querySelectorAll('.sidebar-nav a[data-page]').forEach(function (a) {
      var isActive = a.getAttribute('data-page') === page;
      a.classList.toggle('active', isActive);
      a.setAttribute('aria-current', isActive ? 'page' : 'false');
    });

    // Update open-in-new-tab button
    btnOpenNew.setAttribute('href', pageRoutes[page] || ('/' + page));

    // Close mobile sidebar
    sidebar.classList.remove('open');
    overlayEl.classList.remove('open');

    // Hide loading when iframe loads
    frame.onload = function () {
      overlay.classList.remove('visible');
    };
  }

  // Sidebar click handler
  document.querySelectorAll('.sidebar-nav a[data-page]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      navigateTo(this.getAttribute('data-page'));
    });
  });

  // Mobile menu toggle
  if (mobileBtn) {
    mobileBtn.addEventListener('click', function () {
      sidebar.classList.toggle('open');
      overlayEl.classList.toggle('open');
    });
  }

  // Close sidebar on overlay click
  if (overlayEl) {
    overlayEl.addEventListener('click', function () {
      sidebar.classList.remove('open');
      overlayEl.classList.remove('open');
    });
  }

  // Keyboard navigation — only when focus is NOT inside the iframe
  document.addEventListener('keydown', function (e) {
    if (document.activeElement === frame) return;

    var idx = pages.indexOf(currentPage);
    if (e.key === 'ArrowRight' && idx < pages.length - 1) {
      e.preventDefault();
      navigateTo(pages[idx + 1]);
    } else if (e.key === 'ArrowLeft' && idx > 0) {
      e.preventDefault();
      navigateTo(pages[idx - 1]);
    }
  });
})();
