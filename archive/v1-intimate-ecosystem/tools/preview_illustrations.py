#!/usr/bin/env python3
"""Render each illustration to PNG so the drawing can be eyeballed."""
import pathlib
import sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "deck" / "illustrations"
OUT = pathlib.Path("/tmp/claude-0/-home-user-nadine-/c8f0c78e-f640-5f06-8469-6747cfe2e544/scratchpad/preview")
OUT.mkdir(parents=True, exist_ok=True)

files = sorted(SRC.glob("*.svg"))
if len(sys.argv) > 1:
    files = [f for f in files if any(a in f.name for a in sys.argv[1:])]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    for f in files:
        svg = f.read_text()
        page = b.new_page(viewport={"width": 1600, "height": 1200}, device_scale_factor=1)
        page.set_content(
            "<html><body style='margin:0;background:#FBF7EE;display:inline-block'>"
            f"<div id='w' style='display:inline-block'>{svg}</div></body></html>"
        )
        page.wait_for_timeout(250)
        page.locator("#w").screenshot(path=str(OUT / (f.stem + ".png")))
        page.close()
        print("rendered", f.stem)
    b.close()
