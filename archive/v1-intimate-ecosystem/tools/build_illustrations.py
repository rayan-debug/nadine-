#!/usr/bin/env python3
"""Emit the bespoke vector illustrations for the conference deck.

One consistent visual system across every figure:
  fine charcoal anatomical line - muted warm-beige tissue - translucent layers -
  gold reserved for the single key structure or mechanism of the slide.

Each file is a standalone, editable SVG (Illustrator / Affinity / Figma).
The deck inlines the same markup so that build animations can address
individual elements by class.
"""

import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "deck" / "illustrations"

PAPER = "#FBF7EE"

STYLE = """<style>
  .ln    { fill:none; stroke:#2E2B26; stroke-width:1.9; stroke-linecap:round; stroke-linejoin:round; }
  .ln-m  { fill:none; stroke:#2E2B26; stroke-width:1.3; stroke-linecap:round; stroke-linejoin:round; opacity:.62; }
  .ln-f  { fill:none; stroke:#2E2B26; stroke-width:.9;  stroke-linecap:round; stroke-linejoin:round; opacity:.32; }
  .f1    { fill:#F3EBDC; } .f2 { fill:#E8DCC6; } .f3 { fill:#DCCBAD; } .f4 { fill:#CDB995; }
  .muc   { fill:#F0E1D3; }
  .gold  { fill:none; stroke:#C6A24E; stroke-width:3.6; stroke-linecap:round; stroke-linejoin:round; }
  .gold-t{ fill:none; stroke:#C6A24E; stroke-width:2.2; stroke-linecap:round; }
  .goldf { fill:#C6A24E; } .goldd { fill:#8A6A1C; }
  .halo  { fill:none; stroke:#FBF7EE; stroke-width:7; stroke-linecap:round; opacity:.92; }
  .lead  { fill:none; stroke:#8A7C68; stroke-width:1.2; }
  .lab   { font-family:'Montserrat',Helvetica,Arial,sans-serif; font-size:35px; font-weight:400; fill:#453F35; letter-spacing:.03em; }
  .lab-k { font-family:'Montserrat',Helvetica,Arial,sans-serif; font-size:35px; font-weight:600; fill:#8A6A1C; letter-spacing:.09em; }
  .lab-s { font-family:'Montserrat',Helvetica,Arial,sans-serif; font-size:29px; font-weight:400; fill:#7C7365; letter-spacing:.04em; }
  .lab-b { font-family:'Montserrat',Helvetica,Arial,sans-serif; font-size:26px; font-weight:500; fill:#6B6053; letter-spacing:.15em; }
  .lab-c { font-family:'Montserrat',Helvetica,Arial,sans-serif; font-size:28px; font-weight:600; fill:#8A6A1C; letter-spacing:.17em; }
  .num   { font-family:'Montserrat',Helvetica,Arial,sans-serif; font-size:34px; font-weight:600; fill:#8A6A1C; }
  .ser   { font-family:'Cormorant Garamond',Georgia,serif; fill:#8A6A1C; }
</style>"""


def svg(name, w, h, body, title):
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="{title}">\n'
        f"<title>{title}</title>\n{STYLE}\n{body}\n</svg>\n"
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(doc)
    print(f"  {name:34s} {w}x{h}  {len(doc)/1024:.1f} kB")


def mirror(d, axis):
    """Mirror a path string of absolute commands about a vertical axis."""
    toks, out, take_x = d.split(), [], True
    for t in toks:
        if t[0].isalpha():
            out.append(t)
            take_x = True
            continue
        v = float(t)
        out.append(f"{(2*axis - v):.0f}" if take_x else f"{v:.0f}")
        take_x = not take_x
    return " ".join(out)


def leader(pts, gold=False):
    """Thin leader line with an ivory halo, ending in a dot on the structure."""
    s = " ".join(f"{x},{y}" for x, y in pts)
    ex, ey = pts[-1]
    dot = (f'<circle cx="{ex}" cy="{ey}" r="5" class="goldf"/>' if gold
           else f'<circle cx="{ex}" cy="{ey}" r="4" fill="#8A7C68"/>')
    return (f'<polyline class="halo" points="{s}"/>'
            f'<polyline class="lead" points="{s}" opacity="{0.95 if gold else 0.8}" '
            f'stroke="{"#C6A24E" if gold else "#8A7C68"}"/>{dot}')


# --------------------------------------------------------------------------
# 0. title - abstract layered tissue contour
# --------------------------------------------------------------------------
def title_contour():
    w, h = 1400, 560
    curves, tones = [], ["#F5EFE3", "#F1E9DA", "#EDE3D0", "#E9DDC8", "#E4D7BE",
                         "#DFD0B3", "#D9C8A7", "#D3C09C"]
    for i in range(9):
        y = 84 + i * 56
        a, b = 24 + (i % 3) * 11, 18 + ((i + 1) % 3) * 13
        curves.append(
            f"M -30 {y} C 250 {y - a} 470 {y + b} 700 {y + 4} "
            f"C 940 {y - b} 1180 {y + a} 1430 {y - 8}"
        )
    bands = "".join(f'<path d="{curves[i]} L 1430 {h} L -30 {h} Z" fill="{tones[i]}"/>'
                    for i in range(8))
    lines = "".join(f'<path class="ln-f" d="{d}"/>' for d in curves)
    body = (
        '<defs><linearGradient id="tc-fade" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".34" stop-color="#fff" stop-opacity=".85"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>'
        '<mask id="tc-mask"><rect width="1400" height="560" fill="url(#tc-fade)"/></mask></defs>'
        f'<rect width="{w}" height="{h}" fill="{PAPER}"/>'
        f'<g mask="url(#tc-mask)">{bands}{lines}'
        f'<path class="gold" d="{curves[4]}" opacity=".9"/></g>'
    )
    svg("00-title-contour.svg", w, h, body, "Abstract layered tissue contour")


# --------------------------------------------------------------------------
# 1. spectrum of anatomical variation
# --------------------------------------------------------------------------
def variation_spectrum():
    w, h = 1560, 440
    top = 16
    parts = []
    # (left flap width, right flap width) - the fourth is deliberately asymmetric
    forms = [(15, 15), (30, 27), (46, 44), (64, 33), (78, 74)]
    for i, (wl, wr) in enumerate(forms):
        cx = 196 + i * 292
        outer = (
            f"M {cx} {top} C {cx-86} {top+30} {cx-98} {top+134} {cx-60} {top+216} "
            f"C {cx-36} {top+266} {cx+36} {top+266} {cx+60} {top+216} "
            f"C {cx+98} {top+134} {cx+86} {top+30} {cx} {top} Z"
        )
        gap = 9

        def flap(width, sign):
            s = sign
            return (
                f"M {cx} {top+58} "
                f"C {cx + s*width} {top+92} {cx + s*(width+8)} {top+160} "
                f"{cx + int(s*width*0.45)} {top+210} "
                f"C {cx + int(s*width*0.2)} {top+228} {cx + s*6} {top+234} {cx} {top+238} "
                f"C {cx + s*4} {top+210} {cx + s*gap} {top+150} {cx + int(s*gap*0.6)} {top+90} Z"
            )
        hood = f"M {cx-22} {top+52} C {cx-22} {top+20} {cx+22} {top+20} {cx+22} {top+52}"
        parts.append(
            f'<g class="form form-{i+1}">'
            f'<path d="{outer}" class="f2" opacity=".5"/><path d="{outer}" class="ln-m"/>'
            f'<path d="{flap(wl,-1)}" class="f3" opacity=".8"/><path d="{flap(wl,-1)}" class="ln"/>'
            f'<path d="{flap(wr,1)}" class="f3" opacity=".8"/><path d="{flap(wr,1)}" class="ln"/>'
            f'<path d="{hood}" class="ln-m"/>'
            f"</g>"
        )
    bar_y = 340
    parts.append(
        f'<path class="gold" d="M 84 {bar_y} L 1476 {bar_y}"/>'
        f'<path class="gold" d="M 84 {bar_y-13} L 84 {bar_y+13}"/>'
        f'<path class="gold" d="M 1476 {bar_y-13} L 1476 {bar_y+13}"/>'
        f'<text class="lab-c" x="780" y="{bar_y+54}" text-anchor="middle">'
        f"PHYSIOLOGICAL RANGE</text>"
    )
    svg("01-variation-spectrum.svg", w, h, "".join(parts),
        "Spectrum of physiological anatomical variation")


# --------------------------------------------------------------------------
# 2. Hart's line and external anatomy
# --------------------------------------------------------------------------
def hart_line():
    w, h = 1200, 860
    cx = 590

    # labia majora: two crescents that leave an open pudendal cleft between them
    majora_l = ("M 586 106 C 470 118 380 204 358 336 C 338 458 360 610 414 706 "
                "C 456 778 522 800 578 806 C 540 756 506 684 492 588 "
                "C 476 480 480 356 502 268 C 518 202 548 144 586 106 Z")
    majora_r = mirror(majora_l, cx)
    cleft = ("M 586 106 C 548 144 518 202 502 268 C 480 356 476 480 492 588 "
             "C 506 684 540 756 578 806 L 602 806 C 640 756 674 684 688 588 "
             "C 704 480 700 356 678 268 C 662 202 632 144 594 106 Z")

    # labia minora: substantial flaps whose medial border is Hart's line
    # the anterior labia minora run up alongside the glans and form the prepuce
    minora_l = ("M 576 212 C 548 238 522 300 510 378 C 500 462 512 560 540 618 "
                "C 556 650 572 668 590 678 C 570 612 552 530 552 448 "
                "C 552 372 560 288 576 212 Z")
    minora_r = mirror(minora_l, cx)

    vestibule = ("M 576 216 C 560 290 552 372 552 448 C 552 530 570 612 590 678 "
                 "C 610 612 628 530 628 448 C 628 372 620 290 604 216 "
                 "C 596 210 584 210 576 216 Z")

    # prepuce: continuous with the anterior labia minora, not a separate disc
    hood = ("M 566 258 C 550 244 546 212 552 186 C 558 156 572 144 590 144 "
            "C 608 144 622 156 628 186 C 634 212 630 244 614 258 "
            "C 606 246 598 240 590 240 C 582 240 574 246 566 258 Z")

    hart_l = "M 566 286 C 557 334 552 386 552 448 C 552 530 570 612 590 678"
    hart_r = mirror(hart_l, cx)

    body = [
        f'<path d="{cleft}" class="f1"/>',
        f'<path d="{majora_l}" class="f2"/><path d="{majora_r}" class="f2"/>',
        f'<path d="{vestibule}" class="muc"/>',
        f'<path d="{minora_l}" class="f3"/><path d="{minora_r}" class="f3"/>',
        # glans, then prepuce drawn over it
        '<ellipse cx="590" cy="264" rx="13" ry="16" class="f4"/>'
        '<ellipse cx="590" cy="264" rx="13" ry="16" class="ln-m"/>',
        f'<path d="{hood}" class="f3"/>',
        # external urethral meatus
        '<ellipse cx="590" cy="352" rx="12" ry="8" class="f4"/>'
        '<ellipse cx="590" cy="352" rx="12" ry="8" class="ln-m"/>',
        # introitus
        '<ellipse cx="590" cy="520" rx="30" ry="62" fill="#BCA47B" opacity=".5"/>'
        '<ellipse cx="590" cy="520" rx="30" ry="62" class="ln-m"/>',
        # fourchette and perineal raphe
        '<path class="ln-f" d="M 590 682 L 590 792"/>',
        f'<path class="ln" d="{majora_l}"/><path class="ln" d="{majora_r}"/>',
        f'<path class="ln" d="{minora_l}"/><path class="ln" d="{minora_r}"/>',
        f'<path class="ln" d="{hood}"/>',
    ]

    labels = [
        ("Labia majora", "lab", "end", 318, 320, [(332, 320), (356, 320), (400, 306)], False),
        ("Labia minora", "lab", "end", 318, 480, [(332, 480), (466, 480), (508, 458)], False),
        ("Perineum", "lab", "end", 318, 776, [(332, 776), (494, 776), (584, 744)], False),
        ("Clitoral hood", "lab", "start", 882, 186, [(868, 186), (724, 186), (626, 198)], False),
        ("Vestibule", "lab", "start", 882, 322, [(868, 322), (716, 322), (606, 312)], False),
        ("Hart’s line", "lab-k", "start", 882, 474, [(868, 474), (716, 474), (628, 452)], True),
        ("Introitus", "lab", "start", 882, 620, [(868, 620), (716, 620), (614, 562)], False),
    ]
    for text, cls, anchor, tx, ty, pts, gold in labels:
        if not gold:
            body.append(leader(pts))

    # the gold group is emitted last so that Hart's line reads unbroken over
    # every other leader - and so the deck can reveal line and label together
    hart_g = ['<g class="hart">', f'<path class="gold hart-trace" d="{hart_l}"/>',
              f'<path class="gold hart-trace" d="{hart_r}"/>']
    for text, cls, anchor, tx, ty, pts, gold in labels:
        if gold:
            hart_g.append(leader(pts, gold=True))
            hart_g.append(f'<text class="{cls}" x="{tx}" y="{ty + 11}" '
                          f'text-anchor="{anchor}">{text}</text>')
    hart_g.append("</g>")
    body += hart_g

    for text, cls, anchor, tx, ty, pts, gold in labels:
        if not gold:
            body.append(f'<text class="{cls}" x="{tx}" y="{ty + 11}" '
                        f'text-anchor="{anchor}">{text}</text>')

    svg("02-hart-line-anatomy.svg", w, h, "".join(body),
        "External genital anatomy with Hart’s line")


# --------------------------------------------------------------------------
# 3. cutaneous vs mucosal histology
# --------------------------------------------------------------------------
def cutaneous_mucosal():
    w, h = 1560, 610
    pw = 700
    top, bot = 96, 512
    out = []
    CORNEUM, EPI, DERM = "#D7C39C", "#E9DCC3", "#F4EDE0"

    def band(x, y, text):
        return f'<text class="lab-b" x="{x+20}" y="{y}">{text}</text>'

    # ---- left: keratinised, hair-bearing skin -----------------------------
    x0 = 40
    g = [f'<text class="lab-k" x="{x0}" y="46">KERATINISED SKIN</text>',
         f'<text class="lab-s" x="{x0}" y="84">Labia majora · ectodermal origin</text>',
         f'<rect x="{x0}" y="{top}" width="{pw}" height="{bot-top}" fill="{DERM}"/>']
    # thick stratum corneum, flaking at the surface
    sc = [f"M {x0} {top+14}"]
    for i in range(15):
        sc.append(f"L {x0 + i*(pw/14):.0f} {top + (4 if i % 2 else 18)}")
    sc.append(f"L {x0+pw} {top+76} L {x0} {top+76} Z")
    g.append(f'<path d="{" ".join(sc)}" fill="{CORNEUM}"/>')
    for i in range(5):
        g.append(f'<path class="ln-f" d="M {x0+10} {top+30+i*10} L {x0+pw-10} {top+30+i*10}"/>')
    # viable epidermis with deep rete ridges
    rete = [f"M {x0} {top+76} L {x0+pw} {top+76} L {x0+pw} {top+156}"]
    for i in range(7):
        xx = x0 + pw - i * (pw / 7)
        rete.append(f"C {xx-20:.0f} {top+218} {xx-pw/7+20:.0f} {top+218} {xx-pw/7:.0f} {top+156}")
    rete.append(f"L {x0} {top+76} Z")
    g.append(f'<path d="{" ".join(rete)}" fill="{EPI}"/><path d="{" ".join(rete)}" class="ln-m"/>')
    # melanocytes along the basal layer
    for i in range(8):
        g.append(f'<circle cx="{x0+50+i*86}" cy="{top+190}" r="7" fill="#6E5A3A" opacity=".8"/>')
    # collagen texture in the dermis
    for i in range(11):
        cxp = x0 + 26 + i * 62
        g.append(f'<path class="ln-f" d="M {cxp} {top+286} C {cxp+30} {top+310} {cxp+8} {top+342} {cxp+38} {top+368}"/>')
    # pilosebaceous unit and an eccrine coil, held inside the panel
    g.append(
        f'<path class="ln" d="M {x0+372} {top+16} C {x0+388} {top+124} {x0+414} {top+230} {x0+434} {top+298}"/>'
        f'<path class="ln" d="M {x0+414} {top+16} C {x0+430} {top+124} {x0+454} {top+230} {x0+474} {top+298}"/>'
        f'<ellipse cx="{x0+458}" cy="{top+320}" rx="32" ry="27" class="f3"/>'
        f'<ellipse cx="{x0+458}" cy="{top+320}" rx="32" ry="27" class="ln"/>'
    )
    for dx, dy, r in ((-22, 182, 25), (-50, 212, 19), (-12, 220, 16)):
        g.append(f'<circle cx="{x0+394+dx}" cy="{top+dy}" r="{r}" class="f3"/>'
                 f'<circle cx="{x0+394+dx}" cy="{top+dy}" r="{r}" class="ln-m"/>')
    g.append(
        f'<path class="ln" d="M {x0+606} {top+16} C {x0+612} {top+124} {x0+618} {top+220} {x0+624} {top+280}"/>'
        f'<path class="ln" d="M {x0+636} {top+286} C {x0+660} {top+294} {x0+662} {top+320} {x0+640} {top+328}'
        f' C {x0+616} {top+336} {x0+614} {top+360} {x0+638} {top+366}"/>'
    )
    g += [band(x0, top + 50, "STRATUM CORNEUM"),
          band(x0, top + 120, "VIABLE EPIDERMIS"),
          band(x0, top + 264, "DERMIS"),
          f'<rect x="{x0}" y="{top}" width="{pw}" height="{bot-top}" class="ln-m"/>',
          f'<text class="lab-s" x="{x0}" y="{bot+46}">Thick barrier · adnexa · low permeability</text>']
    out.append("".join(g))

    # ---- right: non-keratinised vestibular mucosa -------------------------
    x0 = 820
    g = [f'<text class="lab-k" x="{x0}" y="46">NON-KERATINISED MUCOSA</text>',
         f'<text class="lab-s" x="{x0}" y="84">Vestibule · endodermal origin</text>',
         f'<rect x="{x0}" y="{top}" width="{pw}" height="{bot-top}" fill="{DERM}"/>',
         f'<rect x="{x0}" y="{top+8}" width="{pw}" height="142" fill="{EPI}"/>']
    flat = [f"M {x0} {top+150}"]
    for i in range(8):
        xx = x0 + (i + 1) * (pw / 8)
        flat.append(f"C {xx-pw/16-14:.0f} {top+164} {xx-pw/16+14:.0f} {top+164} {xx:.0f} {top+150}")
    g.append(f'<path d="{" ".join(flat)}" class="ln-m"/>')
    g.append(f'<path class="ln-m" d="M {x0} {top+8} L {x0+pw} {top+8}"/>')
    # glycogen-rich superficial cells
    for r_i in range(2):
        for c_i in range(11):
            g.append(f'<circle cx="{x0+36+c_i*62}" cy="{top+44+r_i*38}" r="14" fill="{DERM}"/>'
                     f'<circle cx="{x0+36+c_i*62}" cy="{top+44+r_i*38}" r="14" class="ln-f"/>')
    # superficial capillary loops, close to the surface
    for vx, vy in ((160, 210), (350, 228), (520, 206), (640, 234)):
        g.append(f'<path class="ln-m" d="M {x0+vx-58} {top+vy} C {x0+vx-20} {top+vy-30} '
                 f'{x0+vx+20} {top+vy+30} {x0+vx+58} {top+vy}"/>')
    for i in range(11):
        cxp = x0 + 26 + i * 62
        g.append(f'<path class="ln-f" d="M {cxp} {top+296} C {cxp+30} {top+320} {cxp+8} {top+352} {cxp+38} {top+378}"/>')
    g += [f'<text class="lab-b" x="{x0+20}" y="{top+126}">NON-KERATINISED EPITHELIUM</text>',
          band(x0, top + 196, "LAMINA PROPRIA"),
          f'<rect x="{x0}" y="{top}" width="{pw}" height="{bot-top}" class="ln-m"/>',
          f'<text class="lab-s" x="{x0}" y="{bot+46}">No corneum · no adnexa · high permeability</text>']
    out.append("".join(g))

    out.append(f'<path class="gold" d="M 780 {top} L 780 {bot}" opacity=".5" stroke-dasharray="2 15"/>')
    svg("03-cutaneous-mucosal.svg", w, h, "".join(out),
        "Comparative histology: keratinised skin versus vestibular mucosa")


# --------------------------------------------------------------------------
# 4. the inflammation-pigment cycle
# --------------------------------------------------------------------------
def inflammation_cycle():
    w, h = 1400, 920
    cx, cy, R = 740, 456, 306
    nodes = [["Friction"], ["Barrier", "disruption"], ["Inflammation"],
             ["Melanocyte", "activation"], ["Post-inflammatory", "hyperpigmentation"],
             ["Aggressive", "treatment"]]
    out = ['<defs><marker id="cyc-arrow" viewBox="0 0 12 12" refX="9" refY="6" '
           'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M 0 1 L 11 6 L 0 11 z" fill="#C6A24E"/></marker></defs>',
           f'<circle cx="{cx}" cy="{cy}" r="{R}" class="ln-f"/>']

    angs = [math.radians(-90 + i * 60) for i in range(6)]
    for i, a in enumerate(angs):
        pad = math.radians(13)
        s, e = a + pad, angs[(i + 1) % 6] - pad
        x1, y1 = cx + R * math.cos(s), cy + R * math.sin(s)
        x2, y2 = cx + R * math.cos(e), cy + R * math.sin(e)
        out.append(f'<path class="gold-t arc arc-{i+1}" marker-end="url(#cyc-arrow)" '
                   f'd="M {x1:.1f} {y1:.1f} A {R} {R} 0 0 1 {x2:.1f} {y2:.1f}"/>')

    for i, lines in enumerate(nodes):
        a = angs[i]
        nx, ny = cx + R * math.cos(a), cy + R * math.sin(a)
        lx, ly = cx + (R + 76) * math.cos(a), cy + (R + 76) * math.sin(a)
        c, s = math.cos(a), math.sin(a)
        anchor = "middle" if abs(c) < 0.3 else ("start" if c > 0 else "end")
        block = 42 * (len(lines) - 1)
        y0 = ly - block / 2 + (12 if abs(c) >= 0.3 else (34 if s > 0 else -10))
        tspans = "".join(f'<tspan x="{lx:.0f}" dy="{0 if k == 0 else 42}">{ln}</tspan>'
                         for k, ln in enumerate(lines))
        out.append(
            f'<g class="node node-{i+1}">'
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="42" fill="{PAPER}"/>'
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="42" class="gold" stroke-width="2.8"/>'
            f'<text class="num" x="{nx:.1f}" y="{ny+12:.1f}" text-anchor="middle">{i+1}</text>'
            f'<text class="lab" x="{lx:.0f}" y="{y0:.0f}" text-anchor="{anchor}">{tspans}</text></g>'
        )

    out.append(
        f'<text class="ser" x="{cx}" y="{cy-4}" font-size="62" font-style="italic" '
        f'text-anchor="middle">The cycle</text>'
        f'<text class="ser" x="{cx}" y="{cy+62}" font-size="62" font-style="italic" '
        f'text-anchor="middle">closes itself.</text>'
    )
    svg("04-inflammation-pigment-cycle.svg", w, h, "".join(out),
        "The inflammation–pigment cycle")


# --------------------------------------------------------------------------
# 5. energy-tissue depth map
# --------------------------------------------------------------------------
def energy_depth():
    w, h = 1620, 700
    x0, x1 = 372, 1580
    layers = [("Epidermis", "0 – 0.1 mm", 40, 104, "f1"),
              ("Dermis", "0.1 – 2 mm", 104, 332, "f2"),
              ("Submucosa", "2 – 4 mm", 332, 468, "f3"),
              ("Connective tissue", "4 – 8 mm", 468, 576, "f4")]
    out = ['<defs>'
           '<linearGradient id="opt" x1="0" y1="0" x2="0" y2="1">'
           '<stop offset="0" stop-color="#C6A24E" stop-opacity=".8"/>'
           '<stop offset="1" stop-color="#C6A24E" stop-opacity="0"/></linearGradient>'
           '<radialGradient id="rf"><stop offset="0" stop-color="#C6A24E" stop-opacity=".6"/>'
           '<stop offset="1" stop-color="#C6A24E" stop-opacity="0"/></radialGradient></defs>']
    for name, depth, ya, yb, cls in layers:
        out.append(f'<rect x="{x0}" y="{ya}" width="{x1-x0}" height="{yb-ya}" class="{cls}"/>')
        out.append(f'<path class="ln-f" d="M {x0} {yb} L {x1} {yb}"/>')
        out.append(f'<text class="lab" x="{x0-26}" y="{(ya+yb)/2+2}" text-anchor="end">{name}</text>')
        out.append(f'<text class="lab-s" x="{x0-26}" y="{(ya+yb)/2+34}" text-anchor="end">{depth}</text>')
    for i in range(24):
        cxp = x0 + 20 + i * 50
        out.append(f'<path class="ln-f" d="M {cxp} 162 C {cxp+28} 186 {cxp+8} 222 {cxp+36} 250"/>')

    zones = [(396, 736), (796, 1136), (1196, 1560)]
    for zx in (766, 1166):
        out.append(f'<path class="ln-f" d="M {zx} 40 L {zx} 576" stroke-dasharray="2 12"/>')

    # A - optical energy: superficial, and melanin competes for it
    za, zb = zones[0]
    out.append(f'<g class="zone zone-a"><rect x="{za}" y="40" width="{zb-za}" height="146" fill="url(#opt)"/>')
    for i in range(9):
        out.append(f'<circle cx="{za+22+i*38}" cy="94" r="7" fill="#6E5A3A" opacity=".85"/>')
    out.append(f'<text class="lab-c" x="{(za+zb)//2}" y="628" text-anchor="middle">OPTICAL</text>'
               f'<text class="lab-s" x="{(za+zb)//2}" y="666" text-anchor="middle">'
               f'Melanin competes</text></g>')

    # B - fractional columns, with untreated tissue between
    za, zb = zones[1]
    out.append('<g class="zone zone-b">')
    for i in range(7):
        fx = za + 18 + i * 44
        out.append(f'<rect x="{fx}" y="46" width="13" height="252" rx="6" fill="#C6A24E" opacity=".72"/>'
                   f'<rect x="{fx}" y="46" width="13" height="252" rx="6" class="ln-f"/>')
    out.append(f'<text class="lab-c" x="{(za+zb)//2}" y="628" text-anchor="middle">FRACTIONAL COLUMNS</text>'
               f'<text class="lab-s" x="{(za+zb)//2}" y="666" text-anchor="middle">'
               f'Spared tissue between</text></g>')

    # C - volumetric RF, epidermis spared by insulated delivery
    za, zb = zones[2]
    out.append(f'<g class="zone zone-c"><ellipse cx="{(za+zb)//2}" cy="282" rx="188" ry="148" fill="url(#rf)"/>')
    for i in range(5):
        nx = za + 46 + i * 68
        out.append(f'<path class="ln" d="M {nx} 108 L {nx} 298"/>'
                   f'<path class="ln" d="M {nx-8} 298 L {nx} 320 L {nx+8} 298"/>'
                   f'<path class="ln-f" d="M {nx} 46 L {nx} 108"/>')
    out.append(f'<text class="lab-c" x="{(za+zb)//2}" y="628" text-anchor="middle">VOLUMETRIC RF</text>'
               f'<text class="lab-s" x="{(za+zb)//2}" y="666" text-anchor="middle">'
               f'No chromophore</text></g>')
    out.append(f'<rect x="{x0}" y="40" width="{x1-x0}" height="536" class="ln-m"/>')
    svg("05-energy-depth-map.svg", w, h, "".join(out),
        "Energy–tissue interaction by depth")


# --------------------------------------------------------------------------
# 6. the Kabboura clinical framework
# --------------------------------------------------------------------------
def framework():
    w, h = 820, 870
    spine = 150
    rows = [("ASSESS", "Tissue · Pathology · Indication", False, 54),
            ("RESTORE", "Barrier · Inflammation", True, 194),
            ("REBUILD", "Structure · Function", True, 338),
            ("REGENERATE", "Tissue quality · Biostimulation", True, 482),
            ("REFINE", "Pigment · Texture", True, 626),
            ("MAINTAIN", "Reassessment · Prevention", False, 776)]
    out = [f'<path class="gold" d="M {spine} 54 L {spine} 776" opacity=".45"/>']
    for i, (word, sub, dominant, y) in enumerate(rows):
        r = 17 if dominant else 11
        out.append(f'<g class="fw fw-{i+1}">'
                   f'<circle cx="{spine}" cy="{y}" r="{r}" fill="{PAPER}"/>'
                   f'<circle cx="{spine}" cy="{y}" r="{r}" class="gold" stroke-width="3"/>')
        if dominant:
            out.append(f'<circle cx="{spine}" cy="{y}" r="6" class="goldf"/>'
                       f'<text class="ser" x="228" y="{y+26}" font-size="82" font-weight="600">{word}</text>'
                       f'<text class="lab" x="232" y="{y+74}">{sub}</text>')
        else:
            out.append(f'<text class="lab-c" x="228" y="{y+2}" font-size="34">{word}</text>'
                       f'<text class="lab-s" x="232" y="{y+44}">{sub}</text>')
        out.append("</g>")
        if i < len(rows) - 1:
            mid = (y + rows[i + 1][3]) / 2 + 10
            out.append(f'<path class="gold" d="M {spine-11} {mid-11} L {spine} {mid} L {spine+11} {mid-11}" '
                       f'stroke-width="2.6" opacity=".85"/>')
    svg("06-kabboura-framework.svg", w, h, "".join(out), "The Kabboura clinical framework")


if __name__ == "__main__":
    print("illustrations ->", OUT)
    title_contour()
    variation_spectrum()
    hart_line()
    cutaneous_mucosal()
    inflammation_cycle()
    energy_depth()
    framework()
