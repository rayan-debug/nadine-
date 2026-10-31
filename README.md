# nadine-

Starting fresh: a new presentation, with a new design and new content, is coming.
Nothing is published from this repo at the moment.

## What's here

- **[`reference/socials.md`](reference/socials.md)** — the social links and contact
  details from the end of the previous version, kept to reuse in the new one.
- **[`archive/v1-intimate-ecosystem/`](archive/v1-intimate-ecosystem/)** — the whole
  previous version, kept for reference and not displayed.

## The previous version (archived)

Archived on 2026-10-31. It is also tagged in git as **`v1-intimate-ecosystem`**, so
`git checkout v1-intimate-ecosystem` restores it exactly as it was.

| Folder in the archive | What it was |
|---|---|
| `index.html` | *The Intimate Ecosystem* — the scroll-driven web experience that was the live site: a film intro, a hub of twelve chapters, and a closing "Thank You" screen with the social QR codes. |
| `art/` | Eleven wordless chapter illustrations (SVG plates at 1600×900) and their painterly renders, with a gallery page. See its `README.md`. |
| `deck/` | *Tissue-Specific Intimate Medicine* — the 14-slide conference lecture: HTML deck, editable PowerPoint, PDF, slide PNGs, vector illustrations, references page, QR codes and fonts (Cormorant Garamond, Montserrat). See its `README.md`. |
| `docs/` | The source content text the site and deck were written from. |
| `images/` | The labelled chapter plates used on the site. |
| `media/` | Film stills, the chapter video clips, the PRP film and the two conference photos. |
| `tools/` | The Python build scripts for the deck, PPTX, illustrations, QR codes and exports. |
| `README.md` | The previous top-level README. |

Notes:

- Everything moved together, so links between files inside the archive still work.
- The build scripts in `tools/` expect to sit at the repo root; to rebuild the old
  deck, check out the `v1-intimate-ecosystem` tag rather than running them from the archive.
- The old deck's printed QR codes pointed to `rayan-debug.github.io/nadine-/` and
  `.../deck/references.html`. Those addresses no longer show the old pages (the
  archived copies sit under `/archive/v1-intimate-ecosystem/`).
