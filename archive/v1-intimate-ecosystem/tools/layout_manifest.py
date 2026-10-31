#!/usr/bin/env python3
"""Measure the built deck in a real browser and emit a layout manifest.

The manifest is what turns the HTML deck into a native, editable PowerPoint:
every text element becomes a text box at the position the browser laid it out,
every rule and panel becomes a drawn shape, and only the bespoke illustrations
travel as raster (their editable .svg sources ship alongside).

Writes deck/build/layout.json and deck/build/img/*.png
"""

import json
import pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DECK = ROOT / "deck"
OUT = DECK / "build"
IMG = OUT / "img"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

TEXT_SEL = ", ".join([
    ".eyebrow", "h1", ".hero", ".lead", ".note", ".term",
    "footer .ref", ".chip", ".pageno",
    ".title-slide .sub", ".title-slide .name", ".title-slide .cred", ".venue",
    ".split .side li",
    ".tree .q", ".tree .branch h3", ".tree .branch .head", ".tree .branch li",
    ".pathway .nm", ".pathway .agent",
    ".pyramid .nm", ".pyramid .sb",
    ".cascade .cell", ".categories .cat b", ".categories .cat span",
    ".spectrum .cap", ".spectrum .mk .t",
    ".takehome .n", ".takehome .t",
    ".closing .name", ".closing .cred", ".closing .handles",
    ".qr .cap", ".qr .url",
])

SHAPE_SEL = ", ".join([
    "header .rule", ".tree .q", ".pathway .agent", ".pathway .node .dot",
    ".pyramid .tier .bg", ".cascade .cell", ".categories .cat",
    ".spectrum .axis", ".spectrum .mk .pin", ".spectrum .mk .stem",
    ".takehome .row", ".callout",
])

IMG_SEL = ", ".join([
    ".title-slide .plate", ".split .fig > svg", ".stack > figure > svg",
    ".premise figure > svg",
    ".tree .fork", ".pathway .rail", ".qr > svg",
])

SCRIPT = r"""
() => {
  const px = v => Math.round(v * 100) / 100;
  const S = document.querySelector('.slide.on');
  const base = document.getElementById('stage').getBoundingClientRect();
  const rect = e => { const r = e.getBoundingClientRect();
    return {x:px(r.left-base.left), y:px(r.top-base.top), w:px(r.width), h:px(r.height)}; };
  const rgb = s => { const m = s.match(/\d+/g); return m ? [(+m[0]),(+m[1]),(+m[2])] : [0,0,0]; };

  // inline runs, so bold / gold emphasis survives into PowerPoint
  const runs = el => {
    const out = [];
    const walk = (n, bold, colour) => {
      for (const c of n.childNodes) {
        if (c.nodeType === 3) {
          // the browser collapses source whitespace; PowerPoint would not
          const t = c.textContent.replace(/\s+/g, ' ');
          if (t) out.push({t, b:bold, c:colour});
        } else if (c.nodeName === 'BR') {
          out.push({t:'\n', b:bold, c:colour});
        } else {
          const cs = getComputedStyle(c);
          walk(c, +cs.fontWeight >= 600, rgb(cs.color));
        }
      }
    };
    const cs = getComputedStyle(el);
    // ::before markers (the em-dash bullets) exist only in CSS, so lift them
    const bf = getComputedStyle(el, '::before');
    const m = bf.content && bf.content.match(/^"(.*)"$/);
    if (m && m[1]) out.push({t: m[1] + '\u00a0\u00a0', b:false, c:rgb(bf.color)});
    walk(el, +cs.fontWeight >= 600, rgb(cs.color));
    return out;
  };

  const texts = [...S.querySelectorAll(TEXT_SEL)].map(e => {
    const cs = getComputedStyle(e);
    const lh = cs.lineHeight === 'normal'
      ? parseFloat(cs.fontSize) * 1.2 : parseFloat(cs.lineHeight);
    return {
      sel: e.className || e.tagName.toLowerCase(),
      box: rect(e),
      size: parseFloat(cs.fontSize),
      line: lh,
      serif: /Cormorant/.test(cs.fontFamily),
      italic: cs.fontStyle === 'italic',
      weight: +cs.fontWeight,
      colour: rgb(cs.color),
      align: cs.textAlign,
      caps: cs.textTransform === 'uppercase',
      track: cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing),
      pad: [parseFloat(cs.paddingTop), parseFloat(cs.paddingRight),
            parseFloat(cs.paddingBottom), parseFloat(cs.paddingLeft)],
      runs: runs(e),
    };
  });

  const shapes = [...S.querySelectorAll(SHAPE_SEL)].map(e => {
    const cs = getComputedStyle(e);
    return {
      sel: e.className || e.tagName.toLowerCase(),
      box: rect(e),
      fill: cs.backgroundColor === 'rgba(0, 0, 0, 0)' ? null : rgb(cs.backgroundColor),
      radius: parseFloat(cs.borderTopLeftRadius) || 0,
      clip: cs.clipPath && cs.clipPath !== 'none' ? cs.clipPath : null,
      borders: ['Top','Right','Bottom','Left'].map(s => ({
        w: parseFloat(cs['border' + s + 'Width']) || 0,
        c: rgb(cs['border' + s + 'Color']),
      })),
    };
  });

  const footer = S.querySelector('footer');
  if (footer) {
    const cs = getComputedStyle(footer);
    shapes.push({sel:'footer-rule', box: rect(footer), fill:null, radius:0, clip:null,
      borders:[{w:parseFloat(cs.borderTopWidth)||0, c:rgb(cs.borderTopColor)},
               {w:0,c:[0,0,0]},{w:0,c:[0,0,0]},{w:0,c:[0,0,0]}]});
  }

  const images = [...S.querySelectorAll(IMG_SEL)].map((e, i) => ({i, box: rect(e)}));
  const notes = S.querySelector('.notes');
  return {
    title: S.dataset.title || '',
    texts, shapes, images,
    notes: notes ? [...notes.querySelectorAll('p')].map(p => p.innerText) : [],
  };
}
"""


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    manifest = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        page = b.new_page(viewport={"width": 1920, "height": 1080},
                          device_scale_factor=3)
        page.goto((DECK / "index.html").as_uri() + "?all=1")
        page.add_style_tag(content="#help,#progress,#notes,#index{display:none!important}"
                                   "#stage{box-shadow:none}")
        page.wait_for_timeout(1200)
        page.evaluate(f"window.TEXT_SEL = {json.dumps(TEXT_SEL)};"
                      f"window.SHAPE_SEL = {json.dumps(SHAPE_SEL)};"
                      f"window.IMG_SEL = {json.dumps(IMG_SEL)};")
        n = page.evaluate("document.querySelectorAll('.slide').length")
        for i in range(1, n + 1):
            page.evaluate("i => document.querySelectorAll('.slide')"
                          ".forEach((e,k)=>e.classList.toggle('on',k===i-1))", i)
            page.wait_for_timeout(200)
            data = page.evaluate(SCRIPT.replace("TEXT_SEL", "window.TEXT_SEL")
                                       .replace("SHAPE_SEL", "window.SHAPE_SEL")
                                       .replace("IMG_SEL", "window.IMG_SEL"))
            for k, im in enumerate(data["images"]):
                name = f"s{i:02d}-{k}.png"
                page.locator(f".slide.on :is({IMG_SEL})").nth(k).screenshot(
                    path=str(IMG / name), omit_background=True)
                im["file"] = name
            data["n"] = i
            manifest.append(data)
            print(f"  slide {i:02d}  {len(data['texts'])} text  "
                  f"{len(data['shapes'])} shape  {len(data['images'])} image")
        b.close()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "layout.json").write_text(json.dumps(manifest, indent=1))
    print(f"  layout.json  {len(manifest)} slides")


if __name__ == "__main__":
    print("manifest ->", OUT)
    main()
