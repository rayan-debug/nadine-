# Chapter illustrations

Eleven coordinated plates, one per hub chapter, displayed in chapter order in
[`index.html`](index.html).

| # | Chapter | File |
|---|---|---|
| I | The Mindset | [`01-the-mindset.svg`](01-the-mindset.svg) |
| II | Normal Anatomy | [`02-normal-anatomy.svg`](02-normal-anatomy.svg) |
| III | Why Patients Come | [`03-why-patients-come.svg`](03-why-patients-come.svg) |
| IV | Clinical Assessment | [`04-clinical-assessment.svg`](04-clinical-assessment.svg) |
| V | The Treatment Pyramid | [`05-treatment-pyramid.svg`](05-treatment-pyramid.svg) |
| VI | Home Care | [`06-home-care.svg`](06-home-care.svg) |
| VII | Topicals | [`07-topicals.svg`](07-topicals.svg) |
| VIII | Regenerative Injectables | [`08-regenerative-injectables.svg`](08-regenerative-injectables.svg) |
| IX | Energy-Based Medicine | [`09-energy-based-medicine.svg`](09-energy-based-medicine.svg) |
| X | The Kabboura Protocol | [`10-the-kabboura-protocol.svg`](10-the-kabboura-protocol.svg) |
| XI | The Future | [`11-the-future.svg`](11-the-future.svg) |

## The system

These are **wordless** plates. The labelled diagram work is already done by the
`images/` plate set and by `deck/illustrations/`; here the meaning is carried by
form, depth and light, so the plates can sit behind text, open a chapter, or run
full-bleed without competing with a caption.

One atmosphere across all eleven:

- **Ground** `#FBF7EF` ivory, one warm light source per plate, blurred silk veils.
- **Gold** `#C6A24E` (deep `#8A6A1C`, light `#E6CF95`) — reserved for the single
  mechanism that matters in that plate, never decoration.
- **Muted rose** `#C0705E` for inflammation and vasculature, **muted brown**
  `#6F5230` for pigment, **cool grey** `#9AA1A4` for depleted or inert tissue.
  Nothing else is allowed a colour.
- Recurring marks: the circular inset with a hairline gold rim, the dotted
  orbit, the gold bead, the dashed line ending in a stop-bar for anything held
  or inhibited.

Every file is a standalone, editable SVG at 1600×900 — gradients, masks and
groups survive into Illustrator, Affinity and Figma.

## Rebuilding

```sh
python3 tools/build_chapter_art.py        # all eleven SVGs + index.html
```

The generator is `tools/build_chapter_art.py`; each chapter is one function, and
the shared primitives (`ground`, `disc`, `glow`, `bead`, `strand`, `lamellae`,
`blob`, `arc_arrow`) are what keep the eleven looking like one series. Edit a
figure function and rebuild — do not hand-edit the SVGs unless you are exporting
a one-off for print.
