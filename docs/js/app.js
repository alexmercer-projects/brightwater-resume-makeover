(function () {
  document.documentElement.classList.add('js');
  // Before / after tabs (only visible on narrow screens)
  var tabs = [].slice.call(document.querySelectorAll('[role="tab"]'));
  var mq = matchMedia('(max-width: 860px)');
  function select(tab) {
    tabs.forEach(function (t) {
      var on = t === tab, pane = document.getElementById(t.getAttribute('aria-controls'));
      t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1;
      if (mq.matches) pane.hidden = !on; else pane.hidden = false;
    });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { var n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; select(n); n.focus(); }
    });
  });
  if (/[?&]before\b/.test(location.search) && tabs[0]) tabs.forEach(function (t, k) { t.setAttribute('aria-selected', k === 0); });
  function sync() { select(tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0] || tabs[1]); }
  if (tabs.length) { sync(); (mq.addEventListener ? mq.addEventListener('change', sync) : mq.addListener(sync)); }

  // Fade-ins
  var els = [].slice.call(document.querySelectorAll('.reveal'));
  if (document.documentElement.classList.contains('anim') && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 60 + 'ms'; io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('is-in'); });

  // Highlight the section in the nav
  var links = [].slice.call(document.querySelectorAll('.nav a'));
  if ('IntersectionObserver' in window && links.length) {
    var map = {}; links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { links.forEach(function (a) { a.classList.remove('is-on'); }); if (map[e.target.id]) map[e.target.id].classList.add('is-on'); } });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) so.observe(s); });
  }
})();
