# Chapter illustrations

Eleven coordinated plates, one per hub chapter, displayed in chapter order in
[`index.html`](index.html).

Eleven plates over twelve chapters: chapter IX, *The Injectable Protocol*, was
split out of VIII after this series was drawn and has no plate of its own yet.
Every other chapter has both a **vector plate** here and a **render** in
[`renders/`](renders/) — the painterly version of the same composition, at 3200×1800 (2× the canvas).
The gallery shows them side by side.

| # | Chapter | Vector plate | Render |
|---|---|---|---|
| I | The Mindset | [`01-the-mindset.svg`](01-the-mindset.svg) | [`renders/01-the-mindset.webp`](renders/01-the-mindset.webp) |
| II | Normal Anatomy | [`02-normal-anatomy.svg`](02-normal-anatomy.svg) | [`renders/02-normal-anatomy.webp`](renders/02-normal-anatomy.webp) |
| III | Why Patients Come | [`03-why-patients-come.svg`](03-why-patients-come.svg) | [`renders/03-why-patients-come.webp`](renders/03-why-patients-come.webp) |
| IV | Clinical Assessment | [`04-clinical-assessment.svg`](04-clinical-assessment.svg) | [`renders/04-clinical-assessment.webp`](renders/04-clinical-assessment.webp) |
| V | The Treatment Pyramid | [`05-treatment-pyramid.svg`](05-treatment-pyramid.svg) | [`renders/05-treatment-pyramid.webp`](renders/05-treatment-pyramid.webp) |
| VI | Home Care | [`06-home-care.svg`](06-home-care.svg) | [`renders/06-home-care.webp`](renders/06-home-care.webp) |
| VII | Topicals | [`07-topicals.svg`](07-topicals.svg) | [`renders/07-topicals.webp`](renders/07-topicals.webp) |
| VIII | Regenerative Injectables | [`08-regenerative-injectables.svg`](08-regenerative-injectables.svg) | [`renders/08-regenerative-injectables.webp`](renders/08-regenerative-injectables.webp) |
| X | Energy-Based Medicine | [`09-energy-based-medicine.svg`](09-energy-based-medicine.svg) | [`renders/09-energy-based-medicine.webp`](renders/09-energy-based-medicine.webp) |
| XI | The Kabboura Protocol | [`10-the-kabboura-protocol.svg`](10-the-kabboura-protocol.svg) | [`renders/10-the-kabboura-protocol.webp`](renders/10-the-kabboura-protocol.webp) |
| XII | The Future | [`11-the-future.svg`](11-the-future.svg) | [`renders/11-the-future.webp`](renders/11-the-future.webp) |

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

Every vector file is standalone and editable at 1600×900 — gradients, masks and
groups survive into Illustrator, Affinity and Figma. The renders are WebP at the
same 16:9 canvas at 2× (3200×1800), so the two are drop-in interchangeable in a slide or on
the page.

## Rebuilding

```sh
python3 tools/build_chapter_art.py        # all eleven SVGs + index.html
```

The renders are authored outside this repo and dropped into `renders/`; the
`SERIES` table in the generator is what pairs each one with its chapter.

The generator is `tools/build_chapter_art.py`; each chapter is one function, and
the shared primitives (`ground`, `disc`, `glow`, `bead`, `strand`, `lamellae`,
`blob`, `arc_arrow`) are what keep the eleven looking like one series. Edit a
figure function and rebuild — do not hand-edit the SVGs unless you are exporting
a one-off for print.
