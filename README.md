# The Majora Code

**Beyond Volume: The Science, Precision & Safety of Labia Majora Hyaluronic Acid Augmentation**
Dr. Nadeen Kabboura — Obstetrician-Gynecologist · Functional & Aesthetic Gynecology Trainer

A 16-slide, 15-minute congress presentation for the browser. Each slide is a fixed
16:9 canvas (1920×1080) scaled to fit any screen, shown one at a time with animated
transitions. Open [`index.html`](index.html) (or the GitHub Pages site) and press `F`
for full screen.

## Presenting

| Control | |
|---|---|
| `→` `↓` `PageDown` `Space`, scroll down, swipe | next slide |
| `←` `↑` `PageUp`, scroll up, swipe back | previous slide |
| `N` | speaker notes drawer — script, time window, word count and pace for the current slide |
| click the clock / `T` | start–pause the talk timer / reset it |
| `F` | full screen |
| `Home` / `End` | first / last slide |

A presentation clicker works too (it sends `PageDown` / `PageUp`). The toolbar at the
bottom hides while you present and comes back when you move the mouse. Every slide
has its own link (`index.html#s7` opens slide 07).

On phones (and other small screens) the slides stack and scroll instead, with the
same content, animations and dropdowns at a readable size.

Interactive items are dropdowns: clicking one opens its detail directly underneath it,
and opening another closes the first.

## Slides and timing (15:00)

| # | Slide | Window | Interaction |
|---|---|---|---|
| 01 | The Majora Code | 0:00–0:30 | — |
| 02 | The Clinical Dilemma | 0:30–1:00 | five possible meanings of the request, as dropdowns |
| 03 | Anatomy Before Augmentation | 1:00–2:00 | opening a layer isolates it in the diagram |
| 04 | Why Contour Changes | 2:00–2:45 | opening a mechanism reshapes the contour |
| 05 | Patient Selection | 2:45–4:00 | — |
| 06 | The Science of HA | 4:00–5:00 | crosslink-density slider, property dropdowns |
| 07 | Choosing the Right Product | 5:00–5:45 | funnel levels open as dropdowns |
| 08 | The Procedural Map | 5:45–7:00 | 11-step workflow dropdowns |
| 09 | Precision & the Stopping Point | 7:00–8:00 | correction slider with zones |
| 10 | Complications | 8:00–9:00 | — |
| 11 | The First 60 Seconds | 9:00–10:00 | audience poll (answer opens under the choice) + 60-second clock |
| 12 | The Differential | 10:00–11:00 | yes/no decision tree |
| 13 | The Rescue Decision | 11:00–12:00 | — |
| 14 | What Does the Evidence Say? | 12:00–13:00 | — |
| 15 | The Case That Tests Your Judgment | 13:00–14:00 | audience vote + rationale |
| 16 | The Final Code + closing line | 14:00–15:00 | — |

Each slide's spoken script lives in its `<div class="script">` in `index.html`; the
notes drawer reads it from there and flags any slide whose word count is too dense
for its time (> 155 wpm). Current scripts run at 84–130 wpm, leaving room for
audience pauses.

## Design

From the design template: blush ivory `#F7EDE8`, rose `#E8B8C1` / `#DA95A8`, mauve
`#AE6E8C`, plum `#6F5771`, antique gold `#B8914A`; wine `#7E2D4B` is reserved for
complication and emergency content, and the closing slide is near-black and gold.
Typefaces: Playfair Display (headings), Lora (quotes, notes), Montserrat (body).
Watercolour washes, gold botanicals and all diagrams are original SVG generated in
[`assets/js/main.js`](assets/js/main.js); styles are in [`assets/css/style.css`](assets/css/style.css).

## Before the congress — open items

The brief forbids invented evidence, so these are deliberately left for verification
rather than filled in:

- **Slide 14** — ESOLANE (2025) cells are marked *Verify*: add sample size, selection,
  intervention, follow-up, outcomes, adverse events, limitations and COI from the
  original publication. Add a 2026 randomized study only if independently verified.
- **Slide 10** — confirm the *documented* vs *extrapolated* tag on each complication
  against the sources.
- **Slide 08** — published approaches (entry points, planes, volumes) are referred to
  an appendix that still has to be written, each with its original citation.
- **Slide 03** — specialist anatomical review of the schematic and its labels.
- Not yet produced from the brief: editable PowerPoint, appendix slides, reference
  list with DOI/PMID, source/permission register, QC checklist and rehearsal sheet.

## Also in this repo

- [`reference/socials.md`](reference/socials.md) — contact links kept from the previous version.
- [`archive/v1-intimate-ecosystem/`](archive/v1-intimate-ecosystem/) — the previous
  presentation, archived and not displayed (last commit before archiving: `221d139`).
