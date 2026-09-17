#!/usr/bin/env python3
"""Render the deck to high-resolution PNGs and a PDF backup.

    python3 tools/export.py            2x PNGs + PDF into deck/export/
    python3 tools/export.py --scale 1  faster, screen-resolution proof

Every build step is revealed (?all=1) so the exported frames show each slide
in its final state.
"""

import argparse
import pathlib

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DECK = ROOT / "deck"
OUT = DECK / "export"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


def main(scale, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    pngs = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        page = b.new_page(viewport={"width": 1920, "height": 1080},
                          device_scale_factor=scale)
        page.goto((DECK / "index.html").as_uri() + "?all=1")
        # the presenter chrome is not part of the exported artwork
        page.add_style_tag(content="#help,#progress,#notes,#index{display:none!important}"
                                   "#stage{box-shadow:none}")
        page.wait_for_timeout(1200)
        n = page.evaluate("document.querySelectorAll('.slide').length")
        for i in range(1, n + 1):
            page.evaluate(
                "i => { const s=document.querySelectorAll('.slide');"
                "s.forEach((e,k)=>e.classList.toggle('on',k===i-1)); }", i)
            page.wait_for_timeout(180)
            f = out_dir / f"slide-{i:02d}.png"
            page.locator("#stage").screenshot(path=str(f))
            pngs.append(f)
            print(f"  {f.name}")
        b.close()

    pdf = out_dir / "Tissue-Specific-Intimate-Medicine.pdf"
    ims = [Image.open(f).convert("RGB") for f in pngs]
    # 1920 x 1080 px at 144 dpi = 13.333 x 7.5 in, the standard 16:9 slide
    ims[0].save(pdf, save_all=True, append_images=ims[1:],
                resolution=144.0 * scale)
    print(f"  {pdf.name}  ({len(ims)} pages)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    main(a.scale, pathlib.Path(a.out) if a.out else OUT)
