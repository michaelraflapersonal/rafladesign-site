(function () {
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Header: compact on scroll; mobile action bar appears after the hero */
  var hdr = document.querySelector('[data-hdr]');
  var mbar = document.querySelector('.mbar');
  function onScroll() {
    var y = window.scrollY || 0;
    if (hdr) hdr.classList.toggle('is-scrolled', y > 8);
    if (mbar) mbar.classList.toggle('is-on', y > 420);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Mobile menu */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Close' : 'Menu';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.textContent = 'Menu'; }
    });
  }

  /* Count-up on the dimension strip, and process tracks that draw as they come into view */
  var counters = [].slice.call(document.querySelectorAll('[data-count]'));
  var tracks = [].slice.call(document.querySelectorAll('.track'));
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target; io.unobserve(el);
        if (el.hasAttribute('data-count')) countUp(el);
        else { el.style.transition = 'transform 1.6s cubic-bezier(.2,.7,.2,1)'; el.style.transform = 'scale(1)'; }
      });
    }, { threshold: 0.35 });
    counters.forEach(function (el) { io.observe(el); });
    tracks.forEach(function (el) {
      var vertical = getComputedStyle(el).transformOrigin.indexOf('top') === 0 || el.closest('.timeline') || window.innerWidth <= 900;
      el.style.transform = vertical ? 'scaleY(0)' : 'scaleX(0)';
      io.observe(el);
    });
  }
  function countUp(el) {
    var end = parseInt(el.getAttribute('data-count'), 10);
    var suffix = el.getAttribute('data-suffix') || '';
    var t0 = null, dur = 1400;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur);
      var e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * e).toLocaleString('en-AU') + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* Pre-select a project type from links like contact.html#granny-flat */
  function applyHash() {
    var h = (location.hash || '').replace('#', '');
    if (!h) return;
    var chip = document.getElementById('type-' + h);
    if (chip) {
      chip.checked = true;
      var form = document.getElementById('enquire');
      if (form) form.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    }
  }
  applyHash();
  window.addEventListener('hashchange', applyHash);

  /* Enquiry form.
     Static hosting has no server, so the form posts to a form service.
     Set data-endpoint on the <form> (e.g. a Formspree, Web3Forms or Cloudflare Worker URL) to switch it on. */
  [].forEach.call(document.querySelectorAll('form[data-enquiry]'), function (form) {
    var status = form.querySelector('.form-status');
    function show(kind, msg) {
      status.hidden = false;
      status.className = 'form-status ' + kind;
      status.textContent = msg;
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.querySelector('[name="name"]');
      var phone = form.querySelector('[name="phone"]');
      var email = form.querySelector('[name="email"]');
      var bad = null;
      [name, phone].forEach(function (f) { f.removeAttribute('aria-invalid'); });
      if (!name.value.trim()) bad = name;
      else if (!phone.value.trim() && !email.value.trim()) bad = phone;
      if (bad) {
        bad.setAttribute('aria-invalid', 'true'); bad.focus();
        show('err', bad === name ? 'Add your name so we know who to call back.' : 'Add a phone number or email so we can reach you.');
        return;
      }
      var endpoint = form.getAttribute('data-endpoint');
      if (!endpoint) {
        show('err', 'This form isn’t connected yet. Once the site is live it will send your details to Rafla Design. For now, call 0409 701 575.');
        return;
      }
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true; btn.textContent = 'Sending…';
      fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error();
          form.reset();
          if (window.gtag) gtag('event', 'generate_lead', { form: 'enquiry' });
          show('ok', 'Thanks, your request is in. We’ll call you to arrange your free consultation.');
        })
        .catch(function () { show('err', 'Your request didn’t send. Check your connection and try again, or call 0409 701 575.'); })
        .then(function () { btn.disabled = false; btn.textContent = 'Request my free consultation'; });
    });
  });

  /* Analytics: phone and email link clicks */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"], a[href^="mailto:"]');
    if (a && window.gtag) gtag('event', a.getAttribute('href').indexOf('tel:') === 0 ? 'click_phone' : 'click_email');
  });

  /* Cutaway: turn the model around */
  [].forEach.call(document.querySelectorAll('.cutaway'), function (fig) {
    var btn = fig.querySelector('.turn'); var imgs = fig.querySelectorAll('img');
    btn.addEventListener('click', function () { imgs[0].hidden = !imgs[0].hidden; imgs[1].hidden = !imgs[1].hidden; });
  });

  /* Portfolio filter */
  var filters = document.querySelector('.filters');
  if (filters) {
    filters.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      [].forEach.call(filters.querySelectorAll('button'), function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      var f = b.getAttribute('data-filter');
      [].forEach.call(document.querySelectorAll('.work'), function (w) {
        w.hidden = !(f === 'all' || (w.getAttribute('data-type') || '').indexOf(f) > -1);
      });
    });
  }
})();
