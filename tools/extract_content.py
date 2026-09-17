#!/usr/bin/env python3
"""Extract every word of the Intimate Ecosystem hub out of index.html.

Evaluates the BEATS and CH data structures in the page with node, then writes
docs/intimate-ecosystem-content.md - the full text of the intro sequence, all
twelve chapters and thirty-five cards, and the closing.
"""

import json
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "docs" / "intimate-ecosystem-content.md"


def js_array(name):
    """Pull a top-level `const NAME = [ ... ];` out of the page and evaluate it."""
    text = SRC.read_text()
    m = re.search(r"const\s+" + name + r"\s*=\s*\[", text)
    depth, i = 0, text.index("[", m.start())
    for j in range(i, len(text)):
        if text[j] == "[":
            depth += 1
        elif text[j] == "]":
            depth -= 1
            if depth == 0:
                body = text[i:j + 1]
                break
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(f"console.log(JSON.stringify({body}))")
        path = f.name
    return json.loads(subprocess.run(["node", path], capture_output=True,
                                     text=True, check=True).stdout)


def md(s):
    """HTML emphasis -> markdown, everything else left exactly as written."""
    s = re.sub(r"</?b>", "**", s or "")
    return s.replace("<br>", " ")


def main():
    beats = js_array("BEATS")
    chapters = js_array("CH")
    socials = js_array("SOCIALS")
    images = json.loads(subprocess.run(
        ["node", "-e", "console.log(JSON.stringify(" + re.search(
            r"const IMAGES = (\{.*?\n  \});", SRC.read_text(), re.S).group(1) + "))"],
        capture_output=True, text=True, check=True).stdout)

    L = []
    w = L.append

    w("# The Intimate Ecosystem — full text\n")
    w("Every word in the hub, extracted from `index.html`. "
      "Twelve chapters, thirty-five cards.\n")
    w("- **Lecture:** The Intimate Ecosystem — From Normal Anatomy to "
      "Regenerative Aesthetics")
    w("- **Context:** International Masterclass · Regenerative Intimate Medicine")
    w("- **Speaker:** Dr. Nadeen Kabboura\n")
    w("---\n")

    # ---- intro ---------------------------------------------------------
    w("## Opening sequence\n")
    w("Six scroll-driven beats before the hub.\n")
    w("### 1 · Cover\n")
    w("> International Masterclass · Regenerative Intimate Medicine\n")
    w("> # The Intimate Ecosystem\n")
    w("> From Normal Anatomy to Regenerative Aesthetics\n")
    w("> Dr. Kabboura\n")
    for n, b in enumerate(beats[1:], 2):
        if b["type"] == "phil":
            w("### 4 · My Philosophy\n")
            w("> I **educate** before I treat.  ")
            w("> I **preserve** before I remove.  ")
            w("> I **regenerate** before I replace.  ")
            w("> I restore **confidence** — not perfection.\n")
            continue
        w(f"### {n} · {b.get('h', '')}\n")
        if b.get("big"):
            w(f"> **{md(b['big'])}**\n")
        if b.get("sub"):
            w(f"> {md(b['sub'])}\n")
        if b.get("layers"):
            w(f"> {md(b['layers'])}\n")
        if b.get("muted"):
            w(f"> {md(b['muted'])}\n")

    w("---\n")

    # ---- the hub -------------------------------------------------------
    w("## The hub — twelve chapters\n")
    w("Hub label: **The Journey** · *Twelve chapters · select a numeral*\n")
    w("| # | Chapter | Cards |")
    w("|---|---|---|")
    for c in chapters:
        w(f"| {c['r']} | {c['t']} | {len(c['cards'])} |")
    w("")

    for c in chapters:
        w(f"\n---\n\n## {c['r']} · {c['t']}\n")
        for card in c["cards"]:
            w(f"### {card['id']} — {md(card['title'])}\n")
            if card.get("lead"):
                w(f"> *{md(card['lead'])}*\n")
            for blk in card.get("blocks", []):
                h = md(blk.get("h", "")).strip()
                body = md(blk.get("b", ""))
                w(f"**{h}** — {body}\n" if h else f"{body}\n")

            media = card.get("media")
            briefs = ([(m["key"], m.get("brief", "")) for m in media] if media
                      else [(card["id"], card.get("brief", ""))])
            for key, brief in briefs:
                if not brief:
                    continue
                have = images.get(key)
                state = f"`{have}`" if have else "*no image yet — placeholder*"
                w(f"<sub>Plate `{key}` {state} · art brief: {md(brief)}</sub>\n")

    # ---- closing -------------------------------------------------------
    w("\n---\n")
    w("## Closing — Thank You\n")
    w("> With Gratitude\n")
    w("> # Thank You\n")
    w("> Dr. Nadeen Kabboura — Regenerative Intimate Medicine\n")
    w("> Scan a code, or tap a card to connect.\n")
    w("| Channel | Handle | Link |")
    w("|---|---|---|")
    for s in socials:
        w(f"| {s['label']} | {s['val']} | {s['url']} |")
    w("\nTwo conference photographs sit above the sign-off "
      "(`media/conf-1.webp`, `media/conf-2.webp`).\n")

    w("\n---\n")
    w("## Interface strings\n")
    w("| Where | Text |")
    w("|---|---|")
    for a, b in [("Loader", "The Intimate Ecosystem"),
                 ("Scroll hint", "Scroll to begin"),
                 ("Hub label", "The Journey"),
                 ("Hub sublabel", "Twelve chapters · select a numeral"),
                 ("Return hint", "Scroll up to return"),
                 ("Hub progress", "0 / 12 explored"),
                 ("Finish button", "Finish · Thank You →"),
                 ("Viewer exit", "Hub ✕"),
                 ("Thank-you back", "↑ Return to the hub"),
                 ("Plate viewer", "Close ✕")]:
        w(f"| {a} | {b} |")
    w("")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(L))
    cards = sum(len(c["cards"]) for c in chapters)
    blocks = sum(len(k.get("blocks", [])) for c in chapters for k in c["cards"])
    print(f"  {OUT.relative_to(ROOT)}  {len(chapters)} chapters, {cards} cards, "
          f"{blocks} text blocks, {OUT.stat().st_size/1024:.1f} kB")


if __name__ == "__main__":
    main()
