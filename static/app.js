// Directory filters: region chips, borrow/donate chips, free-text search.
// Works without JS too (everything is visible by default).
(function () {
  var q = document.getElementById('q');
  var count = document.getElementById('count');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.listing'));
  var sections = Array.prototype.slice.call(document.querySelectorAll('[data-region-section]'));
  var state = { region: 'all', offer: 'all', text: '' };

  function setPressed(groupAttr, value) {
    document.querySelectorAll('.chip[' + groupAttr + ']').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute(groupAttr) === value ? 'true' : 'false');
    });
  }

  function apply() {
    var shown = 0;
    cards.forEach(function (c) {
      var okRegion = state.region === 'all' || c.dataset.region === state.region;
      var offers = (c.dataset.offers || '').split(' ');
      var okOffer = state.offer === 'all' || offers.indexOf(state.offer) !== -1;
      var okText = !state.text || (c.dataset.text || '').indexOf(state.text) !== -1;
      var show = okRegion && okOffer && okText;
      c.classList.toggle('hidden', !show);
      if (show) shown++;
    });
    sections.forEach(function (s) {
      var any = s.querySelectorAll('.listing:not(.hidden)').length > 0;
      s.classList.toggle('hidden', !any);
    });
    if (count) count.textContent = shown + (shown === 1 ? ' place' : ' places') + ' shown';
  }

  document.querySelectorAll('.chip[data-region]').forEach(function (b) {
    b.addEventListener('click', function () { state.region = b.dataset.region; setPressed('data-region', state.region); apply(); });
  });
  document.querySelectorAll('.chip[data-offer]').forEach(function (b) {
    b.addEventListener('click', function () { state.offer = b.dataset.offer; setPressed('data-offer', state.offer); apply(); });
  });
  if (q) q.addEventListener('input', function () { state.text = q.value.trim().toLowerCase(); apply(); });

  // Deep links like /tennessee/#region-east preselect a region.
  var m = location.hash.match(/^#region-(\w+)/);
  if (m) { state.region = m[1]; setPressed('data-region', state.region); }
  apply();
})();
