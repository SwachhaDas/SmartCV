(function () {
  'use strict';
  const THEME_KEY = 'smartcv-theme';
  const root = document.documentElement;

  function applyTheme(theme) {
    root.setAttribute('data-bs-theme', theme);
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
    document.querySelectorAll('[data-theme-toggle] i').forEach(function (icon) {
      icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    applyTheme(root.getAttribute('data-bs-theme') || 'light');
    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        applyTheme(root.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark');
      });
    });

    const items = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12 });
      items.forEach(function (el) { io.observe(el); });
    }

    document.querySelectorAll('[data-count]').forEach(function (el) {
      const target = parseInt(el.dataset.count, 10) || 0;
      const duration = 900;
      const start = performance.now();
      function tick(now) {
        const p = Math.min((now - start) / duration, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    });

    document.querySelectorAll('form.needs-validation').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        let firstBad = null;
        form.querySelectorAll('input[required], select[required], textarea[required]').forEach(function (field) {
          const wrap = field.closest('.input-icon') || field.parentElement;
          const ok = field.checkValidity() && field.value.trim() !== '';
          wrap.classList.toggle('has-error', !ok);
          if (!ok) {
            wrap.classList.remove('shake');
            void wrap.offsetWidth;
            wrap.classList.add('shake');
            firstBad = firstBad || field;
          }
        });
        if (firstBad) { e.preventDefault(); firstBad.focus(); }
      });
    });
  });
})();