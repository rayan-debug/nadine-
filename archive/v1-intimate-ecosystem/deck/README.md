# Tissue-Specific Intimate Medicine

A 10–15 minute conference lecture for a physician audience on contemporary
functional, aesthetic and regenerative gynaecology.

**One message, defended across fourteen slides:** intimate treatment must be
tissue-specific, indication-driven and biologically rational — not product- or
device-driven.

---

## Deliverables

| File | What it is |
|---|---|
| `index.html` | The deck. Self-contained, fonts embedded, **works with no network**. Open it and press `F`. |
| `Tissue-Specific-Intimate-Medicine.pptx` | Editable PowerPoint. Real text boxes, real shapes, presenter notes in the notes pane. |
| `export/Tissue-Specific-Intimate-Medicine.pdf` | PDF backup, 14 pages, 16:9. |
| `export/slide-NN.png` | 3840 × 2160 PNG of every slide. |
| `illustrations/*.svg` | The six commissioned illustrations plus the title plate, as editable vector. |
| `references.html` | The full bibliography the closing QR code points at. |
| `qr/*.svg` | The two closing QR codes, as vector. |
| `fonts/*.ttf` | Cormorant Garamond and Montserrat, for the PowerPoint file. |
| `build/` | Intermediate layout manifest and figure rasters used to build the PPTX. |

## Presenting

Open `index.html` in any modern browser.

| Key | |
|---|---|
| `→` `Space` `click` | advance one build step, then one slide |
| `←` | back |
| `↑` `↓` | previous / next slide, skipping builds |
| `N` | presenter notes drawer |
| `O` | slide index — click any line to jump |
| `F` | fullscreen |

Nothing animates on a timer. Every build advances on click, and there is at most
one build sequence per slide:

- **03** Hart's line traces in gold, with its label.
- **05** the inflammation–pigment cycle assembles one node at a time and closes.
- **06** the two arms of the decision tree.
- **08** the three energy classes, one at a time.
- **09** the therapeutic pyramid, built from the foundation upward.
- **12** the framework, one stage at a time.

`index.html?all=1` reveals every build step at once and disables animation —
that is what the PNG and PDF exports are rendered from.

## Before the conference — four things to confirm

These are the only placeholders in the deck. All four live at the top of
`tools/build_deck.py`.

1. **`CREDENTIALS`** — currently *“Obstetrics & Gynaecology · Aesthetic and
   Regenerative Medicine”*. Replace with the exact post-nominals you want shown
   on slides 1 and 14.
2. **`VENUE`** — currently *“Conference · Session · Date”* on the title slide.
3. **`SITE`** — the QR codes point at `rayan-debug.github.io/nadine-`. **This
   URL has not been verified from here.** Publish GitHub Pages for this
   repository (Settings → Pages → deploy from `main`), then scan both codes
   before you travel. Both URLs are also printed in plain text under the codes,
   so a failed scan is not a failed slide.
4. **Slide 11** places five therapy classes along an evidence spectrum. The
   ordering is a defensible clinical reading, not a published ranking — confirm
   you are happy to defend each position from the podium.

## Design system

Warm ivory ground `#FBF7EE`, charcoal type and anatomical line `#2E2B26`, muted
beige tissue `#E8DCC6`/`#DCCBAD`, restrained gold `#C6A24E` / `#8A6A1C`, and a
single burgundy `#6E2639` reserved for the two “evidence is limited” chips.

Cormorant Garamond for display, Montserrat for everything else. Slide titles
38–42 pt, body 28–30 pt, figure annotation smaller by design.

Gold is never decorative. On every slide it marks exactly one thing: the key
structure, the mechanism, or the conclusion.

## Scientific integrity

Every slide that makes an empirical claim carries an evidence chip and one or
two abbreviated references in the footer:

- **Established evidence** — anatomy, histology, permeability, the melanogenesis
  pathway.
- **Extrapolated evidence** — dermatological data applied to vulvar tissue.
- **Emerging evidence** — regenerative categories with real but thin literature.
- **Evidence remains limited** — energy devices, and the experimental end of the
  spectrum. Rendered in burgundy.
- **Expert clinical framework** — the assessment tree, the therapeutic pyramid
  and the Kabboura framework, each labelled on the slide as a framework and not
  a guideline.

No claim on a slide is stronger than its chip. The full bibliography is in
`references.html` and behind the closing QR code.

## Rebuilding

```
python3 tools/build_all.py          # everything
python3 tools/build_all.py --fast   # skip the slow 2x raster export
```

`index.html` is **generated**. Edit the slide content in `tools/build_deck.py`,
the drawings in `tools/build_illustrations.py`, and the visual system in
`tools/deck.css`, then rebuild — hand edits to `index.html` are overwritten.

The PowerPoint is built by measuring the real browser layout
(`tools/layout_manifest.py`) and rebuilding it natively
(`tools/build_pptx.py`), so the two stay in step.

Requires `playwright` (Chromium), `python-pptx`, `pillow` and `segno`.

## Known limitations

- **The PowerPoint is editable, not fully vector.** Titles, statements, lists,
  references, chips, page numbers, the pyramid, the pathway, the decision tree,
  the cascade and the evidence spectrum are all native PowerPoint objects. The
  six bespoke anatomical illustrations are placed as 3× rasters; their editable
  `.svg` sources sit in `illustrations/` for a designer to re-place as vector.
- **Install the fonts before opening the PPTX.** `fonts/*.ttf` are the exact
  cuts used. Without them PowerPoint substitutes and the layout drifts. The HTML
  deck has them embedded and needs nothing installed.
- **LibreOffice Impress renders Cormorant's “Th” with a gap** (“Th e cascade”).
  This is a LibreOffice text-shaping artefact, not a defect in the file —
  PowerPoint and Keynote are unaffected. Present from the HTML deck or the PDF.
- The deck has not been tested on a conference projector. Do that: 16:9, and
  check the gold reads at the back of the room before the ivory does.

## Timing

| Section | Slides | Minutes |
|---|---|---|
| Premise and anatomy | 1–4 | 3 |
| Pigment and inflammation | 5–7 | 3–4 |
| Energy and therapeutic hierarchy | 8–9 | 2 |
| Regeneration and emerging evidence | 10–11 | 2–3 |
| Framework and conclusion | 12–14 | 2–3 |

The speaker notes carry a per-slide timing cue. The core runs to ten minutes;
the rest is margin for the introduction and for questions.
