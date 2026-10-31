#!/usr/bin/env python3
"""Rebuild every deck artefact, in dependency order.

    python3 tools/build_all.py              full rebuild (2x PNG + PDF + PPTX)
    python3 tools/build_all.py --fast       skip the slow 2x raster export
"""

import argparse
import runpy
import subprocess
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def step(name, *cmd):
    print(f"\n── {name}")
    r = subprocess.run([sys.executable, *cmd], cwd=ROOT)
    if r.returncode:
        sys.exit(f"failed: {name}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()

    step("illustrations", "tools/build_illustrations.py")
    step("qr codes", "tools/build_qr.py")
    step("deck + references", "tools/build_deck.py")
    step("layout manifest", "tools/layout_manifest.py")
    step("powerpoint", "tools/build_pptx.py")
    if not a.fast:
        step("png + pdf export", "tools/export.py", "--scale", "2")
    print("\ndone.")
