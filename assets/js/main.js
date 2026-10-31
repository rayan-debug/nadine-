/* The Majora Code — illustrations, scroll choreography, presenter tools, interactions */
(() => {
'use strict';

const NS = 'http://www.w3.org/2000/svg';
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

function S(tag, attrs = {}, parent) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function T(parent, x, y, text, cls = '', extra = {}) {
  const t = S('text', { x, y, class: cls, ...extra }, parent);
  t.textContent = text;
  return t;
}
function rand(seed) {
  let s = seed % 2147483647; if (s <= 0) s += 2147483646;
  return () => (s = s * 16807 % 2147483647) / 2147483647;
}
function wave(x0, x1, y, amp, freq, phase = 0, amp2 = 0, freq2 = 0, n = 30) {
  const p = [];
  for (let i = 0; i <= n; i++) {
    const x = x0 + (x1 - x0) * i / n;
    p.push([x, y + amp * Math.sin(x * freq + phase) + amp2 * Math.sin(x * freq2 + phase * 1.7)]);
  }
  return p;
}
// Catmull-Rom through points → cubic Béziers
function smooth(p, move = true) {
  const f = v => v.toFixed(1);
  let d = (move ? 'M' : 'L') + f(p[0][0]) + ' ' + f(p[0][1]);
  for (let i = 0; i < p.length - 1; i++) {
    const p0 = p[i - 1] || p[i], p1 = p[i], p2 = p[i + 1], p3 = p[i + 2] || p2;
    d += `C${f(p1[0] + (p2[0] - p0[0]) / 6)} ${f(p1[1] + (p2[1] - p0[1]) / 6)} ${f(p2[0] - (p3[0] - p1[0]) / 6)} ${f(p2[1] - (p3[1] - p1[1]) / 6)} ${f(p2[0])} ${f(p2[1])}`;
  }
  return d;
}
const band = (top, bot) => smooth(top) + smooth([...bot].reverse(), false) + 'Z';
const yAt = (pts, x) => {
  for (let i = 0; i < pts.length - 1; i++) if (x >= pts[i][0] && x <= pts[i + 1][0]) {
    const t = (x - pts[i][0]) / (pts[i + 1][0] - pts[i][0]);
    return pts[i][1] + t * (pts[i + 1][1] - pts[i][1]);
  }
  return pts[pts.length - 1][1];
};

/* ---------------- decorative: watercolour washes ---------------- */
const TONES = {
  rose: ['#E8B8C1', '#DA95A8', '#F2D2D6', '#E6A9B8', '#D8BFD5', '#EFC7C2'],
  plum: ['#CFA9C6', '#B886AD', '#E2C8DB', '#A97BA0', '#E8B8C1'],
  wine: ['#7E2D4B', '#9A4565', '#5E2238', '#B0587C']
};
$$('.wash').forEach((w, i) => {
  const r = rand(+w.dataset.seed || i + 3), pal = TONES[w.dataset.tone || 'rose'], n = +w.dataset.n || 7;
  const svg = S('svg', { viewBox: '0 0 1000 1000', 'aria-hidden': 'true' });
  const g = S('g', { filter: 'url(#wc)' }, svg);
  for (let k = 0; k < n; k++) {
    const c = pal[k % pal.length];
    S('circle', { cx: 220 + r() * 560, cy: 220 + r() * 560, r: 120 + r() * 190, fill: c,
      'fill-opacity': (.32 + r() * .34).toFixed(2), stroke: c, 'stroke-opacity': .55, 'stroke-width': 4 }, g);
  }
  w.appendChild(svg);
});

/* ---------------- decorative: gold botanical sprigs ---------------- */
$$('svg.sprig').forEach((s, i) => {
  const r = rand(+s.dataset.seed || i + 11), curl = +(s.dataset.curl || 30), n = +s.dataset.leaves || 9;
  s.setAttribute('viewBox', '0 0 200 420');
  s.setAttribute('aria-hidden', 'true');
  const g = S('g', { class: 'draw' }, s);
  const P = t => [100 + curl * Math.sin(t * 2.4) * t, 410 - 390 * t];
  const pts = []; for (let k = 0; k <= 20; k++) pts.push(P(k / 20));
  S('path', { d: smooth(pts), class: 'stem', pathLength: 1 }, g);
  for (let k = 0; k < n; k++) {
    const t = .14 + .8 * k / (n - 1), [x, y] = P(t), [x2, y2] = P(t + .01);
    const ang = Math.atan2(y2 - y, x2 - x) * 180 / Math.PI, side = k % 2 ? 1 : -1;
    const L = (48 - 26 * t) * (.85 + r() * .3), W = L * .32;
    const leaf = S('g', { transform: `translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${(ang + side * (46 + r() * 16)).toFixed(1)})` }, g);
    S('path', { d: `M0 0C${L * .3} ${-W} ${L * .72} ${-W} ${L} 0C${L * .72} ${W} ${L * .3} ${W} 0 0Z`, class: r() < .5 ? 'leaf f' : 'leaf', pathLength: 1 }, leaf);
    S('path', { d: `M0 0L${L * .88} 0`, class: 'rib', pathLength: 1 }, leaf);
  }
  const tip = P(1);
  S('circle', { cx: tip[0], cy: tip[1], r: 2.6, class: 'bud' }, g);
});

/* ---------------- 01 hero: layered tissue lens ---------------- */
(function hero() {
  const svg = $('#heroSvg'); if (!svg) return;
  const defs = S('defs', {}, svg);
  const cp = S('clipPath', { id: 'lens' }, defs); S('circle', { cx: 300, cy: 300, r: 210 }, cp);
  const g = S('g', { 'clip-path': 'url(#lens)' }, svg);
  const X0 = 60, X1 = 540;
  const top = wave(X0, X1, 150, 10, .012, .4, 3, .05);
  const der = wave(X0, X1, 196, 9, .011, 1.2);
  const dar = wave(X0, X1, 207, 9, .011, 1.25);
  const fat = wave(X0, X1, 372, 20, .010, 2.1, 8, .03);
  const fas = wave(X0, X1, 386, 20, .010, 2.1, 8, .03);
  const bot = wave(X0, X1, 600, 0, 0);
  const sky = wave(X0, X1, 60, 0, 0);
  S('path', { d: band(sky, top), fill: '#FBF1EE' }, g);
  S('path', { d: band(top, der), fill: '#E8B8C1' }, g);
  S('path', { d: band(der, dar), fill: '#C995AE' }, g);
  const fatD = band(dar, fat);
  S('path', { d: fatD, fill: '#F8E7DD' }, g);
  S('path', { d: band(fat, fas), fill: '#EAD5B0' }, g);
  S('path', { d: band(fas, bot), fill: '#E6D3E0' }, g);
  // adipose lobules
  const fcp = S('clipPath', { id: 'heroFat' }, defs); S('path', { d: fatD }, fcp);
  const lob = S('g', { 'clip-path': 'url(#heroFat)' }, g), r = rand(17);
  for (let y = 205; y < 400; y += 27) for (let x = 60; x < 545; x += 31)
    S('circle', { cx: x + (r() - .5) * 12 + (y % 2 ? 14 : 0), cy: y + (r() - .5) * 10, r: 11 + r() * 6, fill: 'none', stroke: '#E4C1B2', 'stroke-width': 1.2 }, lob);
  // deep fibres
  for (let k = 0; k < 6; k++) S('path', { d: smooth(wave(X0, X1, 420 + k * 22, 6, .014, k)), fill: 'none', stroke: '#D2B8CC', 'stroke-width': 1 }, g);
  // fascia & surface lines
  const lines = S('g', { class: 'draw' }, g);
  S('path', { d: smooth(fat), fill: 'none', stroke: '#B8914A', 'stroke-width': 1.2, pathLength: 1 }, lines);
  S('path', { d: smooth(top), fill: 'none', stroke: '#AE6E8C', 'stroke-width': 1.2, pathLength: 1 }, lines);
  // vessels & nerve
  S('path', { d: 'M70 470C170 450 220 330 300 300S440 230 540 215', fill: 'none', stroke: '#7E2D4B', 'stroke-width': 3, 'stroke-linecap': 'round', pathLength: 1 }, lines);
  S('path', { d: 'M70 486C175 466 230 346 308 316S446 246 540 231', fill: 'none', stroke: '#6F5771', 'stroke-width': 2.4, 'stroke-linecap': 'round', pathLength: 1 }, lines);
  S('path', { d: 'M300 300C310 260 300 230 320 200M440 245C450 225 445 212 462 200', fill: 'none', stroke: '#7E2D4B', 'stroke-width': 1.4, pathLength: 1 }, lines);
  S('path', { d: smooth(wave(X0, X1, 285, 14, .016, 3)), fill: 'none', stroke: '#B8914A', 'stroke-width': 1.6, 'stroke-dasharray': '1 5', 'stroke-linecap': 'round' }, g);
  // lens rings
  const ring = S('g', { class: 'draw' }, svg);
  S('circle', { cx: 300, cy: 300, r: 210, class: 'o', fill: 'none', stroke: '#B8914A', 'stroke-width': 1.2, pathLength: 1 }, ring);
  S('circle', { cx: 300, cy: 300, r: 240, class: 'o', fill: 'none', stroke: '#B8914A', 'stroke-width': .7, pathLength: 1, style: '--dd:.8s;opacity:.6' }, ring);
  [[-38, 3.5], [148, 2.6], [214, 3.2]].forEach(([a, rr]) => {
    const t = a * Math.PI / 180;
    S('circle', { cx: 300 + 240 * Math.cos(t), cy: 300 + 240 * Math.sin(t), r: rr, fill: '#B8914A' }, svg);
  });
})();

/* ---------------- 03 anatomy: schematic layered section ---------------- */
const LAYER_INFO = {
  '': '<b>Variability is the rule</b>Vessels and nerves do not respect a fixed depth. There is no universally guaranteed vascular-free injection plane.',
  skin: '<b>Skin</b>Hair-bearing, with sebaceous, apocrine and eccrine glands. Thickness varies — thin skin raises the risk of visible or palpable product.',
  fascia: '<b>Fascial layers</b>A thin smooth-muscle and fibrous layer lies beneath the dermis; deeper, the membranous layer of superficial fascia is continuous with Colles’ fascia. Nomenclature varies between sources.',
  fat: '<b>Subcutaneous adipose</b>Volume and distribution vary with the individual, age, weight and hormonal status. Terminal fibres of the round ligament reach this region. No universally accepted discrete compartment.',
  art: '<b>Arterial supply</b>Anterior: external pudendal arteries (from the femoral artery). Posterior: posterior labial branches of the internal pudendal system (via the perineal artery). Course and depth vary; anastomoses exist.',
  vein: '<b>Venous drainage</b>Anteriorly to the external pudendal veins and great saphenous vein; posteriorly to internal pudendal tributaries. Plexuses are variable.',
  nerve: '<b>Sensory innervation</b>Anterior labial nerves (ilioinguinal; genital branch of genitofemoral). Posterior labial nerves (pudendal, via the perineal nerve). Perineal branch of the posterior femoral cutaneous nerve laterally.',
  lymph: '<b>Lymphatic drainage</b>Predominantly to the superficial inguinal lymph nodes.'
};
(function anatomy() {
  const svg = $('#anatSvg'); if (!svg) return;
  svg.setAttribute('viewBox', '0 0 830 470');
  const X0 = 48, X1 = 580;
  const defs = S('defs', {}, svg);
  const top = wave(X0, X1, 42, 5, .015, .3);
  const rete = wave(X0, X1, 58, 3, .09, 0, 1.5, .02, 80);
  const der = wave(X0, X1, 110, 6, .013, 1);
  const dar = wave(X0, X1, 122, 6, .013, 1.05);
  const fat = wave(X0, X1, 318, 18, .011, 2, 7, .034);
  const fas = wave(X0, X1, 332, 18, .011, 2, 7, .034);
  const bot = wave(X0, X1, 452, 0, 0);

  const gSkin = S('g', { class: 'L L-skin' }, svg);
  S('path', { d: band(top, rete), fill: '#E3A9B7' }, gSkin);
  S('path', { d: band(rete, der), fill: '#F1CCD3' }, gSkin);
  const gFas = S('g', { class: 'L L-fascia' }, svg);
  S('path', { d: band(der, dar), fill: '#CB97B0' }, gFas);
  for (let k = 0; k < 2; k++) S('path', { d: smooth(wave(X0, X1, 114 + k * 4, 6, .013, 1.02)), fill: 'none', stroke: '#AE6E8C', 'stroke-width': .6 }, gFas);
  const gFat = S('g', { class: 'L L-fat' }, svg);
  const fatD = band(dar, fat);
  S('path', { d: fatD, fill: '#F8E7DD' }, gFat);
  const cp = S('clipPath', { id: 'anFat' }, defs); S('path', { d: fatD }, cp);
  const lob = S('g', { 'clip-path': 'url(#anFat)' }, gFat), r = rand(29);
  for (let y = 132; y < 345; y += 25) for (let x = X0; x < X1 + 20; x += 29)
    S('circle', { cx: x + (r() - .5) * 10 + ((y / 25 | 0) % 2 ? 14 : 0), cy: y + (r() - .5) * 8, r: 10 + r() * 5, fill: '#FBEFE8', stroke: '#E4C1B2', 'stroke-width': 1.1 }, lob);
  S('path', { d: band(fat, fas), fill: '#EBD8B5' }, gFas);
  S('path', { d: smooth(fat), fill: 'none', stroke: '#B8914A', 'stroke-width': 1.2, 'stroke-dasharray': '6 4' }, gFas);
  S('path', { d: smooth(fas), fill: 'none', stroke: '#B8914A', 'stroke-width': 1.2, 'stroke-dasharray': '6 4' }, gFas);
  const gDeep = S('g', { class: 'L L-fascia' }, svg);
  S('path', { d: band(fas, bot), fill: '#E8D9E4' }, gDeep);
  for (let k = 0; k < 4; k++) S('path', { d: smooth(wave(X0, X1, 360 + k * 24, 4, .02, k)), fill: 'none', stroke: '#D4BCCF', 'stroke-width': 1 }, gDeep);
  // follicles & glands
  [95, 205, 318, 432, 545].forEach(x => {
    const y = yAt(top, x);
    S('path', { d: `M${x} ${y}L${x + 18} 102`, stroke: '#9C6A82', 'stroke-width': 1.4, fill: 'none' }, gSkin);
    S('ellipse', { cx: x + 19, cy: 104, rx: 4, ry: 5.5, fill: '#B87C98' }, gSkin);
    S('path', { d: `M${x} ${y}L${x - 9} ${y - 24}`, stroke: '#6F5771', 'stroke-width': 1.1 }, gSkin);
    S('circle', { cx: x + 14, cy: y + 30, r: 4, fill: '#F7E0C9', stroke: '#D9B877' }, gSkin);
    S('circle', { cx: x + 19, cy: y + 34, r: 3.4, fill: '#F7E0C9', stroke: '#D9B877' }, gSkin);
  });
  // arteries
  const A = { fill: 'none', stroke: '#7E2D4B', 'stroke-linecap': 'round' };
  const gArt = S('g', { class: 'L L-art' }, svg);
  S('path', { ...A, d: smooth(wave(X0, X1, 402, 9, .012, .5)), 'stroke-width': 5 }, gArt);
  S('path', { ...A, d: 'M150 404C138 330 178 250 160 126', 'stroke-width': 3 }, gArt);
  S('path', { ...A, d: 'M430 400C452 330 398 232 420 126', 'stroke-width': 3 }, gArt);
  S('path', { ...A, d: 'M300 398C330 300 420 214 580 204', 'stroke-width': 2.6 }, gArt);
  S('path', { ...A, d: smooth(wave(X0, X1, 124, 3, .03, 2)), 'stroke-width': 1.6 }, gArt);
  T(gArt, 452, 196, 'course depth varies', 's');
  // veins
  const V = { fill: 'none', stroke: '#6F5771', 'stroke-linecap': 'round' };
  const gVein = S('g', { class: 'L L-vein' }, svg);
  S('path', { ...V, d: smooth(wave(X0, X1, 418, 9, .012, .6)), 'stroke-width': 5.5 }, gVein);
  S('path', { ...V, d: 'M164 418C152 336 192 254 174 130', 'stroke-width': 3 }, gVein);
  S('path', { ...V, d: 'M444 416C466 334 412 236 434 130', 'stroke-width': 3 }, gVein);
  S('path', { ...V, d: smooth(wave(X0, X1, 131, 3, .03, 2.4)), 'stroke-width': 1.4 }, gVein);
  // nerves
  const gNerve = S('g', { class: 'L L-nerve' }, svg);
  const nv = { fill: 'none', stroke: '#B8914A', 'stroke-width': 2, 'stroke-dasharray': '2 4', 'stroke-linecap': 'round' };
  S('path', { ...nv, d: smooth(wave(X0, X1, 262, 14, .015, 1.4)) }, gNerve);
  S('path', { ...nv, d: 'M262 268C250 210 280 160 268 104M268 104l-10 -12M268 104l10 -10' }, gNerve);
  S('path', { ...nv, d: 'M520 262C536 200 506 150 522 102M522 102l-9 -12M522 102l11 -9' }, gNerve);
  // lymphatics
  const gLy = S('g', { class: 'L L-lymph' }, svg);
  S('path', { d: smooth(wave(X0 + 20, X1, 178, 7, .02, .8)), fill: 'none', stroke: '#DA95A8', 'stroke-width': 1.6, 'stroke-dasharray': '7 4' }, gLy);
  [210, 380].forEach(x => S('ellipse', { cx: x, cy: 178 + 7 * Math.sin(x * .02 + .8), rx: 6, ry: 4, fill: '#E8B8C1', stroke: '#AE6E8C' }, gLy));
  S('path', { d: 'M76 172l-12 6 12 6', fill: 'none', stroke: '#AE6E8C', 'stroke-width': 1.4 }, gLy);
  T(gLy, 86, 166, 'to superficial inguinal nodes', 's');
  // orientation
  const o = S('g', {}, svg);
  S('path', { d: 'M22 60V420M16 72l6-12 6 12M16 408l6 12 6-12', stroke: '#B8914A', fill: 'none', 'stroke-width': 1 }, o);
  T(o, 12, 240, 'SUPERFICIAL → DEEP', 'o', { transform: 'rotate(-90 12 240)', 'text-anchor': 'middle' });
  // labels with leaders
  const labels = [
    ['skin', 70, yAt(der, X1) - 30, 'Skin', 'hair-bearing · glands'],
    ['fascia', 124, 128, 'Smooth-muscle / fibrous layer', ''],
    ['fat', 230, 222, 'Subcutaneous adipose', 'variable volume & distribution'],
    ['fascia', 326, yAt(fat, X1) + 7, 'Membranous layer', 'continuous with Colles’ fascia'],
    ['fascia', 404, 404, 'Deeper perineal structures', '']
  ];
  labels.forEach(([k, ly, ty, a, b]) => {
    const g = S('g', { class: 'L L-' + k }, svg);
    S('path', { d: `M${X1 - 4} ${ty}L${X1 + 18} ${ty}L${X1 + 30} ${ly}`, fill: 'none', stroke: '#B8914A', 'stroke-width': .8 }, g);
    S('circle', { cx: X1 - 4, cy: ty, r: 2.4, fill: '#B8914A' }, g);
    T(g, X1 + 38, ly + 4, a);
    if (b) T(g, X1 + 38, ly + 20, b, 's');
  });
})();

/* ---------------- 06 HA network ---------------- */
(function molecule() {
  const svg = $('#molSvg'); if (!svg) return;
  const chains = [50, 105, 160, 215].map((y, i) => wave(20, 500, y, 11, .045, i * 1.9, 4, .11, 60));
  const r = rand(61);
  for (let k = 0; k < 16; k++) S('circle', { class: 'h2o', cx: 30 + r() * 460, cy: 25 + r() * 215, r: 3 + r() * 4 }, svg);
  chains.forEach(c => S('path', { class: 'chain', d: smooth(c) }, svg));
  const xls = [];
  for (let k = 0; k < 12; k++) {
    const pair = k % 3, x = 46 + k * 37 + (r() - .5) * 10;
    xls.push(S('line', { class: 'xl', x1: x, x2: x, y1: yAt(chains[pair], x), y2: yAt(chains[pair + 1], x) }, svg));
  }
  const order = xls.map((_, i) => i).sort(() => r() - .5);
  const input = $('#xlink'), out = $('#xlinkOut');
  const upd = () => {
    const v = +input.value;
    order.forEach((idx, i) => xls[idx].classList.toggle('off', i >= v));
    out.textContent = v <= 3 ? 'Lightly crosslinked — softer, spreads more, generally degrades sooner.'
      : v <= 8 ? 'Moderately crosslinked — a balance of support and adaptability.'
      : 'Highly crosslinked — firmer, resists deformation, generally lasts longer.';
    out.insertAdjacentHTML('beforeend', '<br><span class="note">Real behaviour also depends on concentration, gel structure and manufacturing — product-specific.</span>');
  };
  input.addEventListener('input', upd); upd();
})();

/* ---------------- generic single-select panels ---------------- */
function selectable(container, items, out, { initial = -1, onPick } = {}) {
  const pick = i => {
    items.forEach((b, k) => b.setAttribute('aria-pressed', k === i ? 'true' : 'false'));
    if (out) {
      out.classList.add('swap');
      setTimeout(() => { out.innerHTML = items[i].dataset.d; out.classList.remove('swap'); }, 160);
    }
    onPick && onPick(i);
  };
  items.forEach((b, i) => b.addEventListener('click', () => pick(i)));
  if (initial >= 0) pick(initial);
}
// 02 fork
const forkLines = $$('.fork-lines path');
selectable($('#fork'), $$('#fork .opt'), $('#forkOut'), { onPick: i => forkLines.forEach((p, k) => p.classList.toggle('on', k === i)) });
// 06 HA properties
selectable($('#haChips'), $$('#haChips .chip'), $('#haOut'));
// 07 funnel
selectable($('#funnel'), $$('#funnel .tier'), $('#tierOut'));
// 08 steps
selectable($('#steps'), $$('#steps .step'), $('#stepOut'), {
  onPick: () => {}
});
$$('#steps .step').forEach(b => { b.dataset.d = `<b>${b.textContent.replace(/^\d+/, '').trim()}</b>${b.dataset.d}`; });
// 15 vote
selectable($('#vote'), $$('#vote button'), $('#voteOut'), { onPick: () => $('#rationale').classList.add('show') });

// 03 layers
(function layers() {
  const svg = $('#anatSvg'), out = $('#layerOut'), chips = $$('#layerChips .chip');
  const set = l => {
    if (l) svg.dataset.focus = l; else delete svg.dataset.focus;
    chips.forEach(c => c.setAttribute('aria-pressed', c.dataset.l === l ? 'true' : 'false'));
    out.innerHTML = LAYER_INFO[l];
  };
  chips.forEach(c => c.addEventListener('click', () => set(c.dataset.l === svg.dataset.focus ? '' : c.dataset.l)));
  set('');
})();

// 04 contour morph
(function contour() {
  const path = $('#contourPath'), out = $('#contourOut'), chips = $$('#contourChips .chip');
  const D = [
    'M20 210C80 210 110 70 200 70C290 70 320 210 380 210',
    'M20 210C80 210 120 140 200 140C280 140 320 210 380 210',
    'M20 210C95 210 105 105 185 122C265 139 330 224 380 224',
    'M20 210C100 210 140 112 200 112C260 112 300 210 380 210'
  ];
  const TXT = [
    '<b>Reference</b>A schematic reference contour — not an ideal to achieve.',
    '<b>Adipose deflation</b>Volume loss with preserved skin. Filler may partially address this mechanism.',
    '<b>Skin laxity</b>Redundant, descending skin. Volume alone does not tighten — and may add weight.',
    '<b>Constitutional morphology</b>A slender but normal variant. Education first; correction is not a medical necessity.'
  ];
  const set = i => {
    path.style.d = `path("${D[i]}")`; path.setAttribute('d', D[i]);
    chips.forEach((c, k) => c.setAttribute('aria-pressed', k === i ? 'true' : 'false'));
    out.innerHTML = TXT[i];
  };
  chips.forEach((c, i) => c.addEventListener('click', () => set(i)));
  set(0);
})();

// 09 correction slider
(function fill() {
  const input = $('#fill'), path = $('#fillPath'), out = $('#fillOut');
  path.style.transition = 'none';
  const Z = [
    [30, '<b>Under-correction</b>Easily addressed later, once tissue has accommodated.', 'rgba(232,184,193,.25)'],
    [60, '<b>Target zone</b>Conservative and harmonious — oedema and hydration are still to come.', 'rgba(201,179,122,.25)'],
    [80, '<b>Approaching the limit</b>Rising tension and visibility risk. This is where experienced injectors stop.', 'rgba(211,154,134,.3)'],
    [101, '<b>Over-correction</b>Hard to undo cleanly. HA is reversible — but not without cost or risk.', 'rgba(126,45,75,.25)']
  ];
  let last = -1;
  const upd = () => {
    const v = +input.value, py = 178 - v * 1.38, s = v * .15;
    path.setAttribute('d', `M20 210C80 210 ${115 - s} ${py} 200 ${py}C${285 + s} ${py} 320 210 380 210`);
    const z = Z.findIndex(([m]) => v < m);
    path.style.fill = Z[z][2];
    path.style.stroke = z === 3 ? 'var(--wine)' : '';
    if (z !== last) { out.innerHTML = Z[z][1]; last = z; }
  };
  input.addEventListener('input', upd); upd();
})();

// 11 poll + 60-second clock
(function emergency() {
  const btns = $$('#poll button'), verdict = $('#verdict');
  const right = btns.find(b => b.dataset.ok === '1');
  btns.forEach(b => b.addEventListener('click', () => {
    btns.forEach(x => { x.classList.toggle('right', x === right); x.classList.toggle('wrong', x !== right); });
    verdict.innerHTML = b === right ? b.dataset.v : b.dataset.v + '<br><br>' + right.dataset.v;
  }));
  const fg = $('#ringFg'), secs = $('#secs'), items = $$('#seq li'), go = $('#go');
  let raf = 0, t0 = 0;
  const draw = t => {
    fg.style.strokeDashoffset = String(1 - t / 60);
    secs.textContent = Math.max(0, Math.ceil(60 - t));
    items.forEach(li => li.classList.toggle('on', t >= +li.dataset.t));
  };
  const tick = now => {
    const t = Math.min(60, (now - t0) / 1000); draw(t);
    if (t < 60) raf = requestAnimationFrame(tick); else go.textContent = 'Reset';
  };
  go.addEventListener('click', () => {
    if (raf || go.textContent === 'Reset') { cancelAnimationFrame(raf); raf = 0; draw(0); items.forEach(li => li.classList.remove('on')); go.textContent = 'Start the 60 s'; return; }
    t0 = performance.now(); go.textContent = 'Running…'; raf = requestAnimationFrame(tick);
  });
  draw(0); items.forEach(li => li.classList.remove('on'));
})();

// 12 differential tree
(function tree() {
  const Q = {
    q1: ['Disproportionate pain, blanching, livedo or dusky discoloration, or delayed capillary refill?', 'isch', 'q2', 'Ischaemia signs'],
    q2: ['Tense, expanding swelling with ecchymosis, early after injection?', 'hem', 'q3', 'Expanding swelling'],
    q3: ['Increasing pain, warmth, erythema, fluctuance or fever?', 'inf', 'q4', 'Infection signs'],
    q4: ['Firm, tender or inflamed nodule appearing days to weeks later?', 'nod', 'q5', 'Delayed nodule'],
    q5: ['Non-tender, palpable or visible bead or ridge of product?', 'irr', 'exp', 'Palpable product']
  };
  const R = {
    isch: ['Suspected ischaemia', 'Emergency. Stop, escalate and rescue per protocol. Do not delay for imaging.', true],
    hem: ['Haematoma', 'Compression and observation for expansion; urgent review if expanding or threatening the skin.'],
    inf: ['Infection / abscess', 'Examine, culture where possible, antimicrobials, drainage if indicated — with specialist input.'],
    nod: ['Inflammatory / delayed nodule', 'Characterize (ultrasound may help); consider biofilm; follow a specialist pathway.'],
    irr: ['Filler-related irregularity', 'Allow accommodation; consider conservative correction if it persists.'],
    exp: ['Expected post-procedure findings', 'Mild oedema, bruising and tenderness that are improving. Reassess and give safety-net advice.']
  };
  const tq = $('#tq'), yn = $('#yn'), res = $('#tres'), crumbs = $('#crumbs'), again = $('#treeAgain');
  let cur = 'q1';
  const show = id => {
    cur = id;
    if (Q[id]) { tq.textContent = Q[id][0]; tq.hidden = false; yn.hidden = false; res.className = 'result'; again.hidden = id === 'q1'; return; }
    const [t, d, alert] = R[id];
    $('#tresT').textContent = t; $('#tresD').textContent = d;
    tq.hidden = true; yn.hidden = true; again.hidden = false;
    res.className = 'result show' + (alert ? ' alertr' : '');
  };
  yn.addEventListener('click', e => {
    const a = e.target.closest('button'); if (!a) return;
    const q = Q[cur];
    crumbs.insertAdjacentHTML('beforeend', `<span>${q[3]}: ${a.dataset.a === 'y' ? 'yes' : 'no'}</span>`);
    show(a.dataset.a === 'y' ? q[1] : q[2]);
  });
  again.addEventListener('click', () => { crumbs.innerHTML = ''; show('q1'); });
  show('q1');
})();

/* ---------------- scroll choreography ---------------- */
const slides = $$('.slide');
slides.forEach(s => {
  $$('[data-r]', s).forEach((el, i) => el.style.setProperty('--d', Math.min(i * .09, .9).toFixed(2) + 's'));
});
const revealIO = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); revealIO.unobserve(e.target); }
}), { threshold: .14 });
slides.forEach(s => revealIO.observe(s));
requestAnimationFrame(() => slides[0].classList.add('in'));

// rail
const rail = $('#rail');
slides.filter(s => s.id !== 's17').forEach(s => {
  const a = document.createElement('a');
  a.href = '#' + s.id;
  a.innerHTML = `<span>${s.dataset.n} · ${s.dataset.title}</span>`;
  a.setAttribute('aria-label', `Slide ${s.dataset.n}: ${s.dataset.title}`);
  rail.appendChild(a);
});
const dots = $$('a', rail);

let current = 0;
const setCurrent = i => {
  current = i;
  const n = +slides[i].dataset.n - 1;
  dots.forEach((d, k) => d.classList.toggle('on', k === n));
  document.body.classList.toggle('on-dark', slides[i].hasAttribute('data-dark'));
  if (drawer.classList.contains('open')) fillNotes();
};
const curIO = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) setCurrent(slides.indexOf(e.target));
}), { rootMargin: '-50% 0px -50% 0px' });
slides.forEach(s => curIO.observe(s));

// progress + parallax
const prog = $('#prog'), par = $$('[data-par]');
let ticking = false;
const onScroll = () => {
  ticking = false;
  const h = document.documentElement.scrollHeight - innerHeight;
  prog.style.width = (h > 0 ? scrollY / h * 100 : 0) + '%';
  if (reduced) return;
  par.forEach(el => {
    const r = el.parentElement.getBoundingClientRect();
    if (r.bottom < -200 || r.top > innerHeight + 200) return;
    const p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
    el.style.translate = `0 ${(p * +el.dataset.par).toFixed(1)}px`;
  });
};
addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
addEventListener('resize', onScroll);
onScroll();

/* ---------------- presenter tools ---------------- */
const drawer = $('#drawer'), notesBtn = $('#notesBtn');
function fillNotes() {
  const s = slides[current], script = $('.script', s);
  const words = script.textContent.replace(/\[[^\]]*\]/g, '').trim().split(/\s+/).length;
  const sec = +s.dataset.sec, wpm = Math.round(words / sec * 60);
  $('#dMeta').textContent = `Slide ${s.dataset.n} · ${s.dataset.time} · ${sec} s · ${words} words`;
  $('#dTitle').innerHTML = s.dataset.title;
  const pace = $('#dPace');
  pace.textContent = wpm > 155 ? `${wpm} wpm · dense for its time` : `${wpm} wpm · rehearsable`;
  pace.className = 'pace ' + (wpm > 155 ? 'hi' : 'ok');
  $('#dBody').innerHTML = script.innerHTML;
}
const toggleNotes = force => {
  const open = force ?? !drawer.classList.contains('open');
  drawer.classList.toggle('open', open);
  notesBtn.setAttribute('aria-expanded', open);
  if (open) fillNotes();
};
notesBtn.addEventListener('click', () => toggleNotes());
$('#dClose').addEventListener('click', () => toggleNotes(false));

// talk timer
const clock = $('#clock');
let tStart = 0, tAcc = 0, tRun = false;
const fmt = ms => { const s = Math.floor(ms / 1000); return String(s / 60 | 0).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0'); };
setInterval(() => { if (tRun) clock.textContent = fmt(tAcc + performance.now() - tStart); }, 250);
const toggleClock = () => {
  if (tRun) { tAcc += performance.now() - tStart; tRun = false; }
  else { tStart = performance.now(); tRun = true; }
  clock.classList.toggle('run', tRun);
};
clock.addEventListener('click', toggleClock);

// keyboard
const go = i => { i = Math.max(0, Math.min(slides.length - 1, i)); slides[i].scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' }); };
addEventListener('keydown', e => {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const tag = e.target.tagName, onRange = e.target.type === 'range', onBtn = tag === 'BUTTON';
  switch (e.key) {
    case 'ArrowDown': case 'PageDown': if (!onRange) { e.preventDefault(); go(current + 1); } break;
    case 'ArrowUp': case 'PageUp': if (!onRange) { e.preventDefault(); go(current - 1); } break;
    case 'ArrowRight': if (!onRange) { e.preventDefault(); go(current + 1); } break;
    case 'ArrowLeft': if (!onRange) { e.preventDefault(); go(current - 1); } break;
    case ' ': if (!onBtn && !onRange) { e.preventDefault(); go(current + (e.shiftKey ? -1 : 1)); } break;
    case 'Home': e.preventDefault(); go(0); break;
    case 'End': e.preventDefault(); go(slides.length - 1); break;
    case 'n': case 'N': toggleNotes(); break;
    case 't': case 'T': tAcc = 0; tStart = performance.now(); clock.textContent = '00:00'; break;
    case 'f': case 'F': if (!document.fullscreenElement) document.documentElement.requestFullscreen?.(); else document.exitFullscreen?.(); break;
    case 'Escape': toggleNotes(false); break;
  }
});
})();
