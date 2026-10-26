(function () {
  'use strict';

  var studio = document.getElementById('studio');
  if (!studio) return;

  var frame = document.getElementById('previewFrame');
  var stage = document.getElementById('stage');
  var loading = document.getElementById('previewLoading');
  var errorBox = document.getElementById('previewError');
  var retryBtn = document.getElementById('retryBtn');
  var saveBtn = document.getElementById('saveBtn');
  var saveSpin = document.getElementById('saveSpin');
  var saveIcon = document.getElementById('saveIcon');
  var badge = document.getElementById('statusBadge');
  var title = document.getElementById('previewTitle');
  var cards = Array.prototype.slice.call(studio.querySelectorAll('.tpl-card-btn'));

  var saveUrl = studio.dataset.saveUrl;
  var saved = studio.dataset.current;
  var selected = saved;
  var shown = null;
  var cache = {};
  var requestId = 0;
  var deviceWidth = 1280;
  var hoverTimer = null;
  var canHover = window.matchMedia('(hover: hover)').matches;

  function cardFor(slug) {
    return cards.filter(function (c) { return c.dataset.slug === slug; })[0];
  }
  function nameOf(slug) {
    var c = cardFor(slug);
    return c ? c.dataset.name : slug;
  }

  /* ---------------- iframe scaling (Fixing the blank preview) ---------------- */
  function fitFrame() {
    var sw = stage.clientWidth - 32; // Subtract padding
    var sh = stage.clientHeight - 32;
    var scale = Math.min(1, sw / deviceWidth);
    frame.style.flex = 'none';
    frame.style.width = deviceWidth + 'px';
    // Set height to fill the box after scaling
    frame.style.height = (sh / scale) + 'px';
    frame.style.transform = 'scale(' + scale + ')';
  }
  window.addEventListener('resize', fitFrame);

  document.querySelectorAll('[data-device]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('[data-device]').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      deviceWidth = parseInt(btn.dataset.device, 10);
      fitFrame();
    });
  });

  /* ---------------- showing a preview ---------------- */
  function setLoading(on) { loading.classList.toggle('show', on); }

  function putInFrame(html, slug) {
    frame.onload = function () {
      frame.classList.add('ready');
      setLoading(false);
      fitFrame(); // Fit after load
    };
    frame.srcdoc = html;
    shown = slug;
    updateTitle();
  }

  function showPreview(slug) {
    if (slug === shown) { setLoading(false); return; }
    errorBox.classList.add('d-none');
    var myId = ++requestId;

    if (cache[slug]) { putInFrame(cache[slug], slug); return; }

    setLoading(true);
    var url = cardFor(slug).dataset.previewUrl;
    fetch(url, {
      credentials: 'same-origin',
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.text();
      })
      .then(function (html) {
        cache[slug] = html;
        if (myId !== requestId) return;
        putInFrame(html, slug);
      })
      .catch(function () {
        if (myId !== requestId) return;
        setLoading(false);
        errorBox.classList.remove('d-none');
      });
  }

  function updateTitle() {
    var label = 'Previewing: ' + nameOf(shown || selected);
    if (shown === saved) label += ' (published)';
    else if (shown !== selected) label += ' (hover)';
    title.textContent = label;
  }

  function refreshUI() {
    cards.forEach(function (c) {
      c.classList.toggle('is-previewing', c.dataset.slug === selected);
    });
    var dirty = selected !== saved;
    saveBtn.disabled = !dirty;
    badge.classList.toggle('d-none', !dirty);
  }

  cards.forEach(function (card) {
    var slug = card.dataset.slug;

    card.addEventListener('click', function () {
      clearTimeout(hoverTimer);
      selected = slug;
      refreshUI();
      showPreview(slug);
    });

    if (canHover) {
      card.addEventListener('mouseenter', function () {
        clearTimeout(hoverTimer);
        hoverTimer = setTimeout(function () { showPreview(slug); }, 250);
      });
    }
  });

  retryBtn.addEventListener('click', function () {
    delete cache[selected];
    shown = null;
    showPreview(selected);
  });

  function csrfToken() {
    var el = document.querySelector('input[name=csrfmiddlewaretoken]');
    return el ? el.value : '';
  }

  function toast(message, isError) {
    var el = document.getElementById('toast');
    document.getElementById('toastBody').textContent = message;
    el.classList.toggle('text-bg-danger', !!isError);
    el.classList.toggle('text-bg-dark', !isError);
    bootstrap.Toast.getOrCreateInstance(el, { delay: 3500 }).show();
  }

  function setSaving(on) {
    saveBtn.disabled = on;
    saveSpin.classList.toggle('d-none', !on);
    saveIcon.classList.toggle('d-none', on);
  }

  saveBtn.addEventListener('click', function () {
    var slug = selected;
    var body = new FormData();
    body.append('template', slug);
    setSaving(true);

    fetch(saveUrl, {
      method: 'POST',
      body: body,
      credentials: 'same-origin',
      headers: { 'X-CSRFToken': csrfToken(), 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
      .then(function (res) {
        setSaving(false);
        if (!res.ok || !res.data.ok) throw new Error(res.data.error || 'Save failed');
        saved = res.data.slug;
        refreshUI();
        updateTitle();
        toast('Published! Your portfolio and PDF CV now use "' + res.data.name + '".');
      })
      .catch(function (err) {
        setSaving(false);
        refreshUI();
        toast(err.message || 'Could not save.', true);
      });
  });

  // Initialize
  setTimeout(function() {
    fitFrame();
    refreshUI();
    showPreview(selected);
  }, 100);
})();