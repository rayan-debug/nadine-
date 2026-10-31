/* Conference deck runtime: fit-to-viewport stage, click-advanced builds,
   presenter notes, slide index. No dependencies, no network. */
(function () {
  var stage = document.getElementById('stage');
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var notesEl = document.getElementById('notes');
  var notesBody = notesEl.querySelector('.bd');
  var notesHd = notesEl.querySelector('.hd');
  var indexEl = document.getElementById('index');
  var progress = document.getElementById('progress');
  var showAll = /[?&]all=1/.test(location.search);

  var i = 0, step = 0;

  function fit() {
    var s = Math.min(innerWidth / 1920, innerHeight / 1080);
    stage.style.transform = 'translate(-50%,-50%) scale(' + s + ')';
  }
  addEventListener('resize', fit);

  /* dash-length for any traced path, so the gold draws on rather than blinks */
  document.querySelectorAll('.hart-trace').forEach(function (p) {
    try { p.style.setProperty('--len', p.getTotalLength()); } catch (e) {}
  });

  function steps(sl) {
    return Array.prototype.slice.call(sl.querySelectorAll('[data-step]'))
      .map(function (el) { return +el.getAttribute('data-step'); })
      .reduce(function (a, b) { return Math.max(a, b); }, 0);
  }

  function paint() {
    slides.forEach(function (sl, k) { sl.classList.toggle('on', k === i); });
    var sl = slides[i];
    sl.querySelectorAll('[data-step]').forEach(function (el) {
      el.classList.toggle('in', showAll || +el.getAttribute('data-step') <= step);
    });
    progress.style.width = ((i + 1) / slides.length * 100) + '%';

    var n = sl.querySelector('.notes');
    notesBody.innerHTML = n ? n.innerHTML : '<p>—</p>';
    var nxt = slides[i + 1];
    notesHd.innerHTML =
      '<span>Slide ' + (i + 1) + ' / ' + slides.length + '</span>' +
      '<span>' + (steps(sl) ? 'build ' + step + ' / ' + steps(sl) : 'no build') + '</span>' +
      '<span class="nx">Next: ' + (nxt ? (nxt.dataset.title || '—') : 'end of deck') + '</span>';
    location.hash = 'slide-' + (i + 1);
  }

  function go(d) {
    var max = steps(slides[i]);
    if (!showAll && d > 0 && step < max) { step++; return paint(); }
    if (!showAll && d < 0 && step > 0) { step--; return paint(); }
    var j = i + d;
    if (j < 0 || j >= slides.length) return;
    i = j;
    step = (d < 0 && !showAll) ? steps(slides[i]) : 0;
    paint();
  }

  function jump(k) { i = k; step = showAll ? 0 : 0; paint(); indexEl.classList.remove('open'); }

  addEventListener('keydown', function (e) {
    var k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'Enter') { e.preventDefault(); go(1); }
    else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'Backspace') { e.preventDefault(); go(-1); }
    else if (k === 'ArrowDown') { e.preventDefault(); i = Math.min(i + 1, slides.length - 1); step = 0; paint(); }
    else if (k === 'ArrowUp') { e.preventDefault(); i = Math.max(i - 1, 0); step = 0; paint(); }
    else if (k === 'Home') { jump(0); }
    else if (k === 'End') { jump(slides.length - 1); }
    else if (k === 'n' || k === 'N') { notesEl.classList.toggle('open'); }
    else if (k === 'o' || k === 'O') { indexEl.classList.toggle('open'); }
    else if (k === 'f' || k === 'F') {
      if (document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen();
    }
    else if (k === 'Escape') { indexEl.classList.remove('open'); notesEl.classList.remove('open'); }
  });

  /* click anywhere on the stage advances the build - the animations are
     meant to fire on click, never on a timer */
  stage.addEventListener('click', function (e) {
    go(e.clientX < innerWidth * 0.14 ? -1 : 1);
  });

  indexEl.querySelectorAll('li').forEach(function (li) {
    li.addEventListener('click', function () { jump(+li.dataset.go); });
  });

  if (showAll) document.documentElement.classList.add('no-anim');
  var m = /#slide-(\d+)/.exec(location.hash);
  if (m) i = Math.min(slides.length - 1, Math.max(0, +m[1] - 1));

  fit();
  paint();
})();
