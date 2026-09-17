#!/usr/bin/env python3
"""Generate the two closing-slide QR codes as charcoal-on-transparent SVG."""

import pathlib
import segno

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "deck" / "qr"

TARGETS = {
    "references": "https://rayan-debug.github.io/nadine-/deck/references.html",
    "resources": "https://rayan-debug.github.io/nadine-/",
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print("qr ->", OUT)
    for name, url in TARGETS.items():
        qr = segno.make(url, error="m")
        p = OUT / f"{name}.svg"
        qr.save(str(p), kind="svg", dark="#2E2B26", light=None, border=2,
                omitsize=True, xmldecl=False, svgclass=None, lineclass=None)
        print(f"  {name+'.svg':20s} {qr.designator:>6s}  {url}")
