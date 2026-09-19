#!/usr/bin/env python3
"""Emit the eleven chapter illustrations for *The Intimate Ecosystem*.

One illustration per hub chapter, in chapter order:

    I    The Mindset                  the band of normal
    II   Normal Anatomy               the layered field
    III  Why Patients Come            three domains, one person
    IV   Clinical Assessment          what the eye must separate
    V    The Treatment Pyramid        six tiers, climbed slowly
    VI   Home Care                    the barrier and the pigment cycle
    VII  Topicals                     the pathway and its four levers
    VIII Regenerative Injectables     depletion, activation, restoration
    IX   Energy-Based Medicine        the depth map
    X    The Kabboura Protocol        five streams, one tissue
    XI   The Future                   helix, lattice, light

These are wordless plates: the diagram-with-labels work is already done by the
`images/` plate set and by `deck/illustrations/`. Here the meaning has to be
carried by form, depth and light alone, so the whole series shares one
atmosphere - ivory ground, warm translucent strata, a single gold reserved for
the mechanism that matters, muted rose for inflammation and muted brown for
pigment. Nothing else is allowed a colour.

Every file is a standalone editable SVG at 1600x900.

    python3 tools/build_chapter_art.py            # SVGs + gallery
"""

import math
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "art"

W, H = 1600, 900

# ---------------------------------------------------------------- palette --
PAPER = "#FBF7EF"
PAPER_D = "#F3ECDD"
GOLD = "#C6A24E"
GOLD_L = "#E6CF95"
GOLD_D = "#8A6A1C"
INK = "#2E2B26"
WARM = "#8A7C68"
STONE = "#B9B2A5"
COOL = "#9AA1A4"
COOL_D = "#6E757A"
ROSE = "#C0705E"
ROSE_L = "#DFA294"
PIG = "#6F5230"
PIG_L = "#A17E4E"


def fmt(v):
    """Trim floats so the markup stays readable in a vector editor."""
    return f"{v:.1f}".rstrip("0").rstrip(".")


class Defs:
    """Collects gradients, filters and clips, and hands back their ids."""

    def __init__(self, prefix):
        self.prefix = prefix
        self.items = []
        self.n = 0

    def _id(self, kind):
        self.n += 1
        return f"{self.prefix}-{kind}{self.n}"

    def lin(self, stops, x1=0, y1=0, x2=1, y2=0):
        i = self._id("l")
        s = "".join(
            f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>'
            for o, c, a in stops
        )
        self.items.append(
            f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'
        )
        return f"url(#{i})"

    def rad(self, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None):
        i = self._id("r")
        s = "".join(
            f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>'
            for o, c, a in stops
        )
        f = ""
        if fx is not None:
            f = f' fx="{fx}" fy="{fy}"'
        self.items.append(
            f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}"{f}>{s}</radialGradient>'
        )
        return f"url(#{i})"

    def mask(self, content):
        i = self._id("m")
        self.items.append(f'<mask id="{i}">{content}</mask>')
        return f"url(#{i})"

    def clip(self, shape):
        i = self._id("c")
        self.items.append(f'<clipPath id="{i}">{shape}</clipPath>')
        return f"url(#{i})"

    def render(self):
        blurs = "".join(
            f'<filter id="{self.prefix}-b{k}" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="{k}"/></filter>'
            for k in (2, 5, 10, 20, 40, 70)
        )
        return "<defs>" + blurs + "".join(self.items) + "</defs>"

    def blur(self, k):
        return f"url(#{self.prefix}-b{k})"


def write(name, defs, body, title, desc):
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-labelledby="{defs.prefix}-t">\n'
        f'<title id="{defs.prefix}-t">{title}</title>\n<desc>{desc}</desc>\n'
        f"{defs.render()}\n{body}\n</svg>\n"
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(doc)
    print(f"  {name:32s} {len(doc)/1024:6.1f} kB")


# ------------------------------------------------------------- primitives --
def wave(y, amp, phase, n=5, x0=-90, x1=1690, tilt=0.0):
    """A long horizontal cubic wave - the spine of every soft veil and stratum."""
    step = (x1 - x0) / n
    def yy(i):
        return y + amp * math.sin(phase + i * 1.07) + tilt * i * step
    out = [f"M {fmt(x0)} {fmt(yy(0))}"]
    for i in range(n):
        xa, xb = x0 + i * step, x0 + (i + 1) * step
        out.append(
            f"C {fmt(xa + step * .42)} {fmt(yy(i))} {fmt(xb - step * .42)} {fmt(yy(i + 1))} "
            f"{fmt(xb)} {fmt(yy(i + 1))}"
        )
    return " ".join(out)


def ground(d, seed=0, warm=(1150, 280), veil=True):
    """Ivory paper, one warm light source, and a few blurred silk veils."""
    g = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    g.append(
        f'<rect width="{W}" height="{H}" fill="'
        + d.rad([(0, "#FFF7E6", .9), (.55, "#FDF8EC", .5), (1, PAPER, 0)],
                cx=warm[0] / W, cy=warm[1] / H, r=.9) + '"/>'
    )
    if not veil:
        return "".join(g)
    rng = random.Random(seed)
    tones = ["#FFFFFF", "#F4EBD9", "#FFFFFF", "#EEE4CF", "#FFFDF7"]
    for i in range(5):
        y = 190 + i * 155 + rng.uniform(-45, 45)
        g.append(
            f'<path d="{wave(y, rng.uniform(34, 96), rng.uniform(0, 6.2), tilt=rng.uniform(-.02, .02))}" '
            f'fill="none" stroke="{tones[i]}" stroke-width="{fmt(rng.uniform(70, 165))}" '
            f'stroke-linecap="round" opacity="{fmt(rng.uniform(.26, .5))}" filter="{d.blur(40)}"/>'
        )
    return "".join(g)


def glow(d, cx, cy, r, color=GOLD, op=.45, k=20):
    return (f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="'
            + d.rad([(0, color, op), (.5, color, op * .4), (1, color, 0)])
            + f'" filter="{d.blur(k)}"/>')


def bead(d, cx, cy, r, color=GOLD, halo=True):
    f = d.rad([(0, "#FFF8E4", 1), (.4, color, 1), (1, GOLD_D, 1)], cx=.34, cy=.3, r=.8)
    h = (f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r * 3.1)}" fill="'
         + d.rad([(0, color, .32), (1, color, 0)]) + '"/>') if halo else ""
    return h + f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="{f}"/>'


def ring(cx, cy, r, color=GOLD, op=.45, wdt=1.1, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="none" '
            f'stroke="{color}" stroke-width="{wdt}" opacity="{op}"{da}/>')


def bead_ring(cx, cy, r, n, rr=3.0, color=GOLD, op=.55, phase=0.0):
    return "".join(
        f'<circle cx="{fmt(cx + r * math.cos(phase + i * 2 * math.pi / n))}" '
        f'cy="{fmt(cy + r * math.sin(phase + i * 2 * math.pi / n))}" '
        f'r="{rr}" fill="{color}" opacity="{op}"/>' for i in range(n)
    )


def disc(d, cx, cy, r, inner, tone=None, rim=.6, halo=.26, sheen=True):
    """A circular inset - outer glow, translucent body, hairline gold rim."""
    clip = d.clip(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}"/>')
    tone = tone or d.rad([(0, "#FFFFFF", .95), (.7, "#FCF7EB", .88), (1, "#F1E8D6", .92)],
                         cx=.36, cy=.3, r=.85)
    out = [glow(d, cx, cy, r * 1.22, GOLD, halo, 20),
           f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="{tone}"/>',
           f'<g clip-path="{clip}">{inner}</g>']
    if sheen:
        out.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="'
                   + d.rad([(0, "#FFFFFF", .34), (.55, "#FFFFFF", 0), (1, "#FFFFFF", 0)],
                           cx=.32, cy=.24, r=.6) + '"/>')
    out.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="none" '
               f'stroke="{GOLD}" stroke-width="1.5" opacity="{rim}"/>')
    return "".join(out)


def head(x, y, ang, s=12, color=GOLD, op=.85):
    pts = []
    for da, rr in ((0.0, s), (2.55, s * .82), (-2.55, s * .82)):
        pts.append(f"{fmt(x + rr * math.cos(ang + da))},{fmt(y + rr * math.sin(ang + da))}")
    return f'<polygon points="{" ".join(pts)}" fill="{color}" opacity="{op}"/>'


def arc_arrow(cx, cy, r, a0, a1, color=GOLD, op=.7, wdt=3.0, tip=True, dash=None):
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    large = 1 if abs(a1 - a0) > math.pi else 0
    sweep = 1 if a1 > a0 else 0
    da = f' stroke-dasharray="{dash}"' if dash else ""
    s = (f'<path d="M {fmt(x0)} {fmt(y0)} A {fmt(r)} {fmt(r)} 0 {large} {sweep} {fmt(x1)} {fmt(y1)}" '
         f'fill="none" stroke="{color}" stroke-width="{wdt}" stroke-linecap="round" '
         f'opacity="{op}"{da}/>')
    if tip:
        tangent = a1 + (math.pi / 2 if sweep else -math.pi / 2)
        s += head(x1, y1, tangent, 12, color, op + .12)
    return s


def strand(pts, color=GOLD, op=.6, wdt=2.0, dash=None, cap="round"):
    """Smooth polyline through points, as a Catmull-Rom-ish cubic chain."""
    if len(pts) < 2:
        return ""
    d = [f"M {fmt(pts[0][0])} {fmt(pts[0][1])}"]
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        px, py = pts[i - 1] if i else pts[i]
        nx, ny = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]
        c1 = (x0 + (x1 - px) / 6, y0 + (y1 - py) / 6)
        c2 = (x1 - (nx - x0) / 6, y1 - (ny - y0) / 6)
        d.append(f"C {fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(x1)} {fmt(y1)}")
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{" ".join(d)}" fill="none" stroke="{color}" stroke-width="{wdt}" '
            f'stroke-linecap="{cap}" opacity="{op}"{da}/>')


def fibre(rng, x0, x1, y, amp=9, n=7, color="#D8CCB2", op=.55, wdt=1.6):
    pts = [(x0 + (x1 - x0) * i / n, y + rng.uniform(-amp, amp)) for i in range(n + 1)]
    return strand(pts, color, op, wdt)


def blob(cx, cy, r, rng, wob=.28, n=9):
    """A closed irregular form - lesions, lobules, patches."""
    pts = []
    for i in range(n):
        a = i * 2 * math.pi / n
        rr = r * rng.uniform(1 - wob, 1 + wob)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * rng.uniform(.82, 1.12)))
    pts = pts + pts[:3]
    d = [f"M {fmt(pts[0][0])} {fmt(pts[0][1])}"]
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        px, py = pts[i - 1] if i else pts[-2]
        nx, ny = pts[i + 2] if i + 2 < len(pts) else pts[1]
        d.append(f"C {fmt(x0 + (x1 - px) / 6)} {fmt(y0 + (y1 - py) / 6)} "
                 f"{fmt(x1 - (nx - x0) / 6)} {fmt(y1 - (ny - y0) / 6)} {fmt(x1)} {fmt(y1)}")
    return " ".join(d) + " Z"


def specks(rng, n, box, r=(1.2, 3.4), color=GOLD, op=(.2, .6)):
    x0, y0, x1, y1 = box
    return "".join(
        f'<circle cx="{fmt(rng.uniform(x0, x1))}" cy="{fmt(rng.uniform(y0, y1))}" '
        f'r="{fmt(rng.uniform(*r))}" fill="{color}" opacity="{fmt(rng.uniform(*op))}"/>'
        for _ in range(n)
    )


def curve(fn, x0=-90, x1=1690, n=110):
    """Sample a python function into a path - lets other marks sit exactly on it."""
    pts = [(x0 + (x1 - x0) * i / n, fn(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    return "M " + " L ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)


# =====================================================================
# I - The Mindset : the band of normal
# =====================================================================
def petal(cx, cy, w, hh, wl, wr):
    """An abstract folded form - the silhouette abstracted, never illustrated."""
    outer = (
        f"M {fmt(cx)} {fmt(cy - hh)} "
        f"C {fmt(cx - w)} {fmt(cy - hh * .58)} {fmt(cx - w * 1.12)} {fmt(cy + hh * .32)} "
        f"{fmt(cx - w * .62)} {fmt(cy + hh * .78)} "
        f"C {fmt(cx - w * .34)} {fmt(cy + hh * 1.02)} {fmt(cx + w * .34)} {fmt(cy + hh * 1.02)} "
        f"{fmt(cx + w * .62)} {fmt(cy + hh * .78)} "
        f"C {fmt(cx + w * 1.12)} {fmt(cy + hh * .32)} {fmt(cx + w)} {fmt(cy - hh * .58)} "
        f"{fmt(cx)} {fmt(cy - hh)} Z"
    )

    def flap(fw, s):
        return (
            f"M {fmt(cx)} {fmt(cy - hh * .62)} "
            f"C {fmt(cx + s * fw)} {fmt(cy - hh * .3)} {fmt(cx + s * fw * 1.15)} {fmt(cy + hh * .3)} "
            f"{fmt(cx + s * fw * .5)} {fmt(cy + hh * .72)} "
            f"C {fmt(cx + s * fw * .2)} {fmt(cy + hh * .9)} {fmt(cx + s * 4)} {fmt(cy + hh * .94)} "
            f"{fmt(cx)} {fmt(cy + hh * .96)} "
            f"C {fmt(cx + s * 3)} {fmt(cy + hh * .6)} {fmt(cx + s * 8)} {fmt(cy)} "
            f"{fmt(cx + s * 5)} {fmt(cy - hh * .6)} Z"
        )

    return outer, flap(wl, -1), flap(wr, 1)


def ch1_mindset():
    d = Defs("m")
    rng = random.Random(11)
    body = [ground(d, seed=3, warm=(820, 250))]

    forms = [
        # (half-width, half-height, left flap, right flap, tone, tilt)
        (42, 104, 10, 14, "#F2EFE9", -3.5),
        (58, 140, 26, 20, "#EFE9DC", 1.5),
        (48, 120, 38, 30, "#ECE4D2", -2.0),
        (66, 158, 50, 26, "#E9DFC8", 2.8),
        (52, 126, 28, 50, "#E6D9BF", -1.4),
        (70, 166, 58, 54, "#E3D4B4", 2.0),
        (46, 112, 18, 36, "#DFCDA6", -2.6),
    ]
    n = len(forms)
    x0, span = 216, 1168
    base = 520
    band_y = 268

    # the band of normal - one unbroken gold span over every form
    arc = (f"M 150 {band_y + 20} C 470 {band_y - 26} 1130 {band_y - 26} 1450 {band_y + 20}")
    body.append(f'<path d="{arc}" fill="none" stroke="{GOLD}" stroke-width="16" '
                f'opacity=".16" filter="{d.blur(10)}"/>')
    body.append(f'<path d="{arc}" fill="none" stroke="{GOLD}" stroke-width="2.6" '
                f'opacity=".85" stroke-linecap="round"/>')
    for x, y in ((150, band_y + 20), (1450, band_y + 20)):
        body.append(f'<path d="M {x} {y - 17} L {x} {y + 17}" stroke="{GOLD}" '
                    f'stroke-width="2.6" stroke-linecap="round" opacity=".85"/>')

    for i, (w, hh, wl, wr, tone, tilt) in enumerate(forms):
        cx = x0 + span * i / (n - 1)
        cy = base - 26 * math.sin(math.pi * i / (n - 1))
        outer, fl, fr = petal(cx, cy, w, hh, wl, wr)

        body.append(ring(cx, cy + hh * .06, hh * 1.34, GOLD, .17, 1))
        body.append(glow(d, cx, cy, hh * 1.1, "#FFF3D8", .5, 20))

        shade = d.lin([(0, "#FFFFFF", .95), (.45, tone, .95), (1, "#DCD0B6", .95)],
                      x1=0, y1=0, x2=.3, y2=1)
        body.append(f'<g transform="rotate({fmt(tilt)} {fmt(cx)} {fmt(cy + hh * .8)})">')
        body.append(f'<path d="{outer}" fill="{shade}"/>')
        body.append(f'<path d="{outer}" fill="none" stroke="{WARM}" stroke-width="1.1" opacity=".3"/>')
        inner = d.lin([(0, "#FFFFFF", .6), (1, "#C4AF87", .88)], x1=0, y1=0, x2=.4, y2=1)
        body.append(f'<path d="{fl}" fill="{inner}"/><path d="{fr}" fill="{inner}"/>')
        body.append(f'<path d="{fl}" fill="none" stroke="{WARM}" stroke-width="1" opacity=".34"/>'
                    f'<path d="{fr}" fill="none" stroke="{WARM}" stroke-width="1" opacity=".34"/>')
        # the crown fold
        body.append(f'<path d="M {fmt(cx - 18)} {fmt(cy - hh * .66)} '
                    f'C {fmt(cx - 18)} {fmt(cy - hh * .94)} {fmt(cx + 18)} {fmt(cy - hh * .94)} '
                    f'{fmt(cx + 18)} {fmt(cy - hh * .66)}" fill="none" stroke="{WARM}" '
                    f'stroke-width="1.1" opacity=".38"/>')
        body.append("</g>")

        # a tick on the band above every form: all of them are inside it
        body.append(f'<path d="M {fmt(cx)} {fmt(band_y + 6 - 18 * math.sin(math.pi * i / (n - 1)) * .4)} '
                    f'L {fmt(cx)} {fmt(cy - hh * 1.32)}" stroke="{GOLD}" stroke-width="1" '
                    f'opacity=".3" stroke-dasharray="2 7"/>')
        body.append(bead(d, cx, band_y + 4 - 20 * math.sin(math.pi * i / (n - 1)) * .38, 4.6))

        # reflection
        body.append(f'<g transform="translate(0 {fmt(2 * (cy + hh * 1.02))}) scale(1 -1)" '
                    f'opacity=".13" filter="{d.blur(5)}">'
                    f'<path d="{outer}" fill="{PIG_L}"/></g>')

    body.append(specks(rng, 26, (140, 180, 1460, 760), (1, 2.8), GOLD, (.12, .34)))
    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", 0), (.62, "#FFFFFF", 0), (1, "#EFE6D2", .5)], r=.78)
                + '"/>')

    write("01-the-mindset.svg", d, "".join(body),
          "The band of normal",
          "Seven abstracted forms of differing length, width, symmetry and tone, "
          "every one of them held inside a single unbroken gold span: the "
          "physiological range has no cut-off.")




# =====================================================================
# II - Normal Anatomy : the layered field
# =====================================================================
def ch2_anatomy():
    d = Defs("a")
    rng = random.Random(22)
    body = [ground(d, seed=8, warm=(1180, 150), veil=False)]

    # the whole plate hangs off one undulating basement membrane, and the
    # epithelium above it thins from keratinised skin into mucosa
    def mem(x):
        return 404 + 26 * math.sin(x / 430 + 1.0) + 10 * math.sin(x / 150 + .4)

    def thick(x):
        t = max(0.0, min(1.0, (x + 60) / 1640))
        return 152 - 108 * t ** 1.35

    def top(x):
        return mem(x) - thick(x)

    body.append(f'<path d="{curve(mem)} L 1690 -40 L -90 -40 Z" fill="{PAPER}" opacity="0"/>')

    # --- the environment above: microbiome, and the tissue's own sentries
    for _ in range(96):
        x, y = rng.uniform(20, 1580), rng.uniform(22, 210)
        if y > top(x) - 24:
            continue
        r = rng.uniform(3, 6.5)
        c = rng.choice([GOLD, STONE, "#CDBE9C", COOL, PIG_L])
        o = fmt(rng.uniform(.2, .5))
        if rng.random() < .4:
            body.append(f'<ellipse cx="{fmt(x)}" cy="{fmt(y)}" rx="{fmt(r * 1.8)}" '
                        f'ry="{fmt(r * .78)}" fill="{c}" opacity="{o}" '
                        f'transform="rotate({fmt(rng.uniform(-45, 45))} {fmt(x)} {fmt(y)})"/>')
        else:
            body.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{c}" opacity="{o}"/>'
                        f'<circle cx="{fmt(x + r * 1.6)}" cy="{fmt(y + r * .6)}" r="{fmt(r * .82)}" '
                        f'fill="{c}" opacity="{o}"/>')
    for i in range(9):
        x = 110 + i * 172
        y = top(x) - 22
        body.append(f'<path d="M {fmt(x)} {fmt(y + 22)} L {fmt(x)} {fmt(y)} '
                    f'M {fmt(x)} {fmt(y)} l -9 -11 M {fmt(x)} {fmt(y)} l 9 -11" '
                    f'stroke="{GOLD}" stroke-width="2" opacity=".5" stroke-linecap="round"/>')

    # --- epithelium
    body.append(f'<path d="{curve(top)} L 1690 {fmt(mem(1690))} '
                + " ".join(f"L {fmt(x)} {fmt(mem(x))}"
                           for x in range(1690, -91, -40))
                + ' Z" fill="' + d.lin([(0, "#F8F2E5", .96), (1, "#FCF8EF", .96)], y2=1) + '"/>')
    # keratin lamellae, only where the epithelium is thick enough to have them
    for k in range(6):
        f = .06 + k * .05
        pts = [(x, top(x) + thick(x) * f) for x in range(-90, 1700, 60) if thick(x) > 62 + k * 9]
        if len(pts) > 2:
            body.append(strand(pts, "#E5D9BE", .5 - k * .05, 5.5 - k * .6))
    # cell rows following the membrane, flattening as they rise
    for f, ry_f, flat in ((.84, .115, 1.0), (.62, .105, 1.25), (.42, .085, 1.7), (.24, .06, 2.4)):
        x = -60
        while x < 1660:
            t = thick(x)
            ry = max(3.4, t * ry_f)
            rx = ry * flat * rng.uniform(.92, 1.12)
            cy = top(x) + t * (1 - f)
            body.append(f'<ellipse cx="{fmt(x)}" cy="{fmt(cy)}" rx="{fmt(rx)}" ry="{fmt(ry)}" '
                        f'fill="#FAF5EA" opacity=".95" stroke="#DCD0B6" stroke-width=".9"/>')
            if f > .35 and rng.random() < .9:
                body.append(f'<ellipse cx="{fmt(x)}" cy="{fmt(cy)}" rx="{fmt(rx * .3)}" '
                            f'ry="{fmt(ry * .32)}" fill="{WARM}" opacity=".32"/>')
            x += rx * 2.1
    body.append(f'<path d="{curve(top)}" fill="none" stroke="#E0D3B6" stroke-width="1.6" opacity=".7"/>')

    # --- the basement membrane: the single gold structure of the plate
    body.append(f'<path d="{curve(mem)}" fill="none" stroke="{GOLD}" stroke-width="16" '
                f'opacity=".22" filter="{d.blur(10)}"/>')
    body.append(f'<path d="{curve(mem)}" fill="none" stroke="{GOLD}" stroke-width="3.6" opacity=".95"/>')
    body.append(f'<path d="{curve(lambda x: mem(x) + 6)}" fill="none" stroke="{GOLD_L}" '
                f'stroke-width="1.3" opacity=".55"/>')

    # melanocytes on the membrane, dendrites reaching up between the cells
    for i in range(12):
        x = 70 + i * 132
        y = mem(x) - 9
        body.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="7.5" fill="{PIG}" opacity=".45"/>')
        for a in (-2.6, -2.15, -1.7, -1.25, -.8):
            ln = 20 + thick(x) * .16
            body.append(f'<path d="M {fmt(x)} {fmt(y)} Q {fmt(x + ln * .6 * math.cos(a))} '
                        f'{fmt(y + ln * .6 * math.sin(a))} {fmt(x + ln * math.cos(a))} '
                        f'{fmt(y + ln * math.sin(a))}" fill="none" stroke="{PIG}" '
                        f'stroke-width="1.3" opacity=".3" stroke-linecap="round"/>')

    # --- dermis
    body.append(f'<path d="{curve(mem)} L 1690 940 L -90 940 Z" fill="'
                + d.lin([(0, "#F6F0E2", .9), (.55, "#F3EBDA", .92), (1, "#EDE2CC", .94)], y2=1)
                + '"/>')
    for i in range(30):
        y = mem(0) + 24 + i * 11.5
        col = rng.choice(["#DDCFB1", "#D3C199", "#E4D8BE", "#C9B58A"])
        body.append(fibre(rng, -70, 1670, y, amp=6 + i * .3, n=10, color=col,
                          op=rng.uniform(.3, .6), wdt=rng.uniform(1.3, 3.4)))
    # elastin - finer, dashed, sparser
    for _ in range(46):
        x, y = rng.uniform(10, 1590), rng.uniform(mem(800) + 30, 700)
        body.append(f'<path d="M {fmt(x)} {fmt(y)} q {fmt(rng.uniform(10, 20))} '
                    f'{fmt(rng.uniform(-9, 9))} {fmt(rng.uniform(22, 44))} {fmt(rng.uniform(-6, 6))}" '
                    f'fill="none" stroke="{STONE}" stroke-width="1" opacity=".42" '
                    f'stroke-dasharray="3 5"/>')
    # fibroblasts
    for _ in range(16):
        x, y = rng.uniform(40, 1560), rng.uniform(mem(800) + 40, 720)
        a = fmt(math.degrees(rng.uniform(-.3, .3)))
        body.append(f'<g transform="rotate({a} {fmt(x)} {fmt(y)})">'
                    f'<ellipse cx="{fmt(x)}" cy="{fmt(y)}" rx="27" ry="9" fill="#F3ECDC" '
                    f'opacity=".95" stroke="#CCBEA2" stroke-width="1"/>'
                    f'<ellipse cx="{fmt(x)}" cy="{fmt(y)}" rx="8.4" ry="4.8" fill="{WARM}" opacity=".38"/>'
                    f'<path d="M {fmt(x - 27)} {fmt(y)} l -17 -6 M {fmt(x + 27)} {fmt(y)} l 17 6" '
                    f'fill="none" stroke="#CCBEA2" stroke-width="1" opacity=".75"/></g>')

    # --- vessels (the only rose in the series) and nerves (gold)
    def tree(x, y, ang, ln, wdt, color, op, depth=0, tip=None):
        x2, y2 = x + ln * math.cos(ang), y + ln * math.sin(ang)
        s = strand([(x, y), ((x + x2) / 2 + rng.uniform(-10, 10),
                             (y + y2) / 2 + rng.uniform(-10, 10)), (x2, y2)],
                   color, op - depth * .05, wdt)
        if depth >= 3:
            if tip:
                s += f'<circle cx="{fmt(x2)}" cy="{fmt(y2)}" r="4.6" fill="{tip}" opacity=".65"/>'
            return s
        s += tree(x2, y2, ang + rng.uniform(.3, .75), ln * .64, wdt * .64, color, op, depth + 1, tip)
        s += tree(x2, y2, ang - rng.uniform(.3, .75), ln * .6, wdt * .6, color, op, depth + 1, tip)
        return s

    body.append(tree(-30, 780, -.55, 175, 9.5, ROSE, .5))
    body.append(tree(560, 930, -1.3, 158, 8.5, ROSE, .5))
    body.append(tree(1640, 830, -2.45, 172, 9, ROSE, .5))
    body.append(tree(1210, 930, -1.5, 150, 5.2, GOLD, .62, tip=GOLD))
    body.append(tree(250, 930, -1.32, 142, 4.6, GOLD, .62, tip=GOLD))

    # --- fat lobules in the deepest plane
    lob = d.rad([(0, "#FFFDF6", .95), (.72, "#F7F0DF", .93), (1, "#E7DBC0", .95)], cx=.36, cy=.3, r=.82)
    for _ in range(26):
        x, y = rng.uniform(-10, 1610), rng.uniform(742, 930)
        r = rng.uniform(28, 58)
        body.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{lob}" '
                    f'stroke="#DACCAE" stroke-width="1.1" opacity=".93"/>')

    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", .12), (.58, "#FFFFFF", 0), (1, "#E8DDC5", .55)], r=.82)
                + '"/>')

    write("02-normal-anatomy.svg", d, "".join(body),
          "The layered field",
          "One cross-section of the whole ecosystem: microbiome above the surface, "
          "keratinised epithelium thinning left-to-right into mucosa, the basement "
          "membrane in gold with melanocytes ranged along it, then collagen, elastin, "
          "fibroblasts, vessels, nerves and fat.")


# =====================================================================
# III - Why Patients Come : three domains, one journey
# =====================================================================
def bloom(d, cx, cy, r, t, rng):
    """A form that opens and warms as the journey advances, in a gold-rimmed disc."""
    cool, warm = (0x9A, 0xA1, 0xA4), (0xC6, 0xA2, 0x4E)
    col = "#%02X%02X%02X" % tuple(int(cool[k] + (warm[k] - cool[k]) * t) for k in range(3))
    ins = []
    n = 5
    spread = .34 + 1.45 * t
    for i in range(n):
        a = -math.pi / 2 + (i - (n - 1) / 2) * spread / n * 2.0
        ln = r * (.40 + .42 * t)
        wdt = r * (.115 + .085 * t)
        bx, by = cx, cy + r * .32
        mx, my = bx + ln * .55 * math.cos(a), by + ln * .55 * math.sin(a)
        ins.append(f'<ellipse cx="{fmt(mx)}" cy="{fmt(my)}" rx="{fmt(ln * .58)}" '
                   f'ry="{fmt(wdt)}" transform="rotate({fmt(math.degrees(a))} {fmt(mx)} {fmt(my)})" '
                   f'fill="{col}" fill-opacity="{fmt(.17 + .3 * t)}" stroke="{col}" '
                   f'stroke-width="1.2" stroke-opacity="{fmt(.4 + .38 * t)}"/>')
    if t > .5:
        ins.append(bead_ring(cx, cy - r * .1, r * .74, 7, 2.4 + 2 * t, GOLD, .3 + .4 * t, -1.57))
    ins.append(glow(d, cx, cy + r * .1, r * (.5 + .6 * t), col, .2 + .45 * t, 10))
    ins.append(bead(d, cx, cy + r * .34, 3 + 3.4 * t, col, halo=False))
    return disc(d, cx, cy, r, "".join(ins), rim=.3 + .45 * t, halo=.1 + .32 * t)


def ch3_why():
    d = Defs("w")
    rng = random.Random(33)
    body = [ground(d, seed=5, warm=(1300, 300))]

    domains = [(452, 344, "physical"), (748, 344, "functional"), (600, 606, "psychological")]
    r = 212
    mid = (600, 430)

    for cx, cy, kind in domains:
        clip = d.clip(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>')
        tex = []
        if kind == "physical":
            tex.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PIG_L}" opacity=".13"/>')
            tex.append(specks(rng, 190, (cx - r, cy - r, cx + r, cy + r), (2.5, 9), PIG, (.14, .5)))
            for i in range(8):
                tex.append(fibre(rng, cx - r, cx + r, cy - 150 + i * 42, amp=14, n=6,
                                 color="#B49A6E", op=.5, wdt=2.8))
        elif kind == "functional":
            tex.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{COOL}" opacity=".1"/>')
            for i in range(21):
                yy = cy - r + i * 21
                tex.append(f'<path d="M {fmt(cx - r)} {fmt(yy)} L {fmt(cx + r)} {fmt(yy + 9)}" '
                           f'stroke="{COOL_D}" stroke-width="1.3" opacity=".34"/>')
            for _ in range(11):
                x, y = rng.uniform(cx - r * .8, cx + r * .8), rng.uniform(cy - r * .85, cy + r * .5)
                tex.append(strand([(x, y), (x + rng.uniform(-14, 14), y + 30),
                                   (x + rng.uniform(-18, 18), y + 62)], "#8E8674", .55, 1.9))
        else:
            tex.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD_L}" opacity=".1"/>')
            for k in range(11):
                tex.append(ring(cx, cy, 20 + k * 19, GOLD if k % 2 == 0 else "#A89C86",
                                .42 - k * .025, 1.4))
            tex.append(glow(d, cx, cy, 78, COOL_D, .22, 20))
        fill = d.rad([(0, "#FFFFFF", .8), (.7, "#FAF3E3", .62), (1, "#EADFC6", .72)],
                     cx=.36, cy=.3, r=.85)
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
                    f'<g clip-path="{clip}">{"".join(tex)}</g>'
                    f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD}" '
                    f'stroke-width="1.6" opacity=".55"/>')

    # where the three meet: one person, not three complaints
    body.append(glow(d, mid[0], mid[1], 196, GOLD, .85, 40))
    body.append(glow(d, mid[0], mid[1], 108, "#FFEFC6", .95, 20))
    body.append(glow(d, mid[0], mid[1], 46, "#FFFDF4", 1, 10))
    body.append(bead_ring(mid[0], mid[1], 58, 9, 3.4, GOLD, .6))
    body.append(ring(mid[0], mid[1], 92, GOLD, .4, 1.3, "4 9"))
    body.append(bead(d, mid[0], mid[1], 13))

    # the journey: silence, first conversation, assessment, shared plan, restoration
    stations = [(1030, 760), (1136, 662), (1256, 542), (1382, 404), (1498, 250)]
    body.append(strand(stations, GOLD, .38, 1.5, dash="3 9"))
    for i, (x, y) in enumerate(stations):
        t = i / (len(stations) - 1)
        if i:
            px, py = stations[i - 1]
            body.append(head((px + x) / 2, (py + y) / 2, math.atan2(y - py, x - px), 10, GOLD, .5))
        body.append(bloom(d, x, y, 40 + 34 * t, t, rng))
    body.append(glow(d, 1498, 250, 210, GOLD, .34, 40))

    body.append(specks(rng, 26, (930, 150, 1560, 830), (1, 3), GOLD, (.12, .35)))
    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", 0), (.62, "#FFFFFF", 0), (1, "#EDE3CE", .55)], r=.8)
                + '"/>')

    write("03-why-patients-come.svg", d, "".join(body),
          "Three domains, one journey",
          "Physical, functional and psychological concern as three translucent fields "
          "overlapping on a single luminous centre - the patient - with the journey "
          "from silent concern to restoration opening and warming beside them.")


# =====================================================================
# IV - Clinical Assessment : what the eye has to separate
# =====================================================================
def tissue_field(d, rng, box, scale=1.0, tone="#F8F2E4"):
    x0, y0, x1, y1 = box
    out = []
    y = y0
    row = 0
    while y < y1:
        x = x0 + (row % 2) * 13 * scale
        while x < x1:
            rx = rng.uniform(11, 15) * scale
            ry = rx * rng.uniform(.78, .95)
            out.append(f'<ellipse cx="{fmt(x)}" cy="{fmt(y)}" rx="{fmt(rx)}" ry="{fmt(ry)}" '
                       f'fill="{tone}" opacity=".92" stroke="#DACEB4" stroke-width=".9"/>')
            if rng.random() < .7:
                out.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(rx * .28)}" '
                           f'fill="{WARM}" opacity=".3"/>')
            x += rx * 2.1
        y += 24 * scale
        row += 1
    return "".join(out)


def ch4_assessment():
    d = Defs("c")
    rng = random.Random(44)
    body = [ground(d, seed=12, warm=(1220, 220))]

    # --- the field being read, feathered away at the right rather than cut
    fade = d.mask(
        '<rect x="-40" y="-40" width="980" height="980" fill="'
        + d.lin([(0, "#FFFFFF", 1), (.6, "#FFFFFF", 1), (1, "#000000", 1)], x2=1)
        + '"/>')
    fld = [tissue_field(d, rng, (-30, -20, 900, 930), 1.0)]
    for i in range(12):
        fld.append(fibre(rng, -40, 920, -10 + i * 84, amp=16, n=7, color="#D3C3A0", op=.45, wdt=3.2))
    fld.append(specks(rng, 90, (20, 40, 860, 880), (3, 10), PIG, (.06, .24)))
    body.append(f'<g mask="{fade}" opacity=".92">{"".join(fld)}</g>')

    # --- the lens
    lx, ly, lr = 392, 470, 208
    ang = 2.36
    hx, hy = lx + lr * math.cos(ang), ly + lr * math.sin(ang)
    body.append(f'<path d="M {fmt(hx)} {fmt(hy)} L {fmt(hx + 150 * math.cos(ang))} '
                f'{fmt(hy + 150 * math.sin(ang))}" stroke="{GOLD_D}" stroke-width="26" '
                f'stroke-linecap="round" opacity=".18" filter="{d.blur(10)}"/>')
    body.append(f'<path d="M {fmt(hx)} {fmt(hy)} L {fmt(hx + 150 * math.cos(ang))} '
                f'{fmt(hy + 150 * math.sin(ang))}" stroke="'
                + d.lin([(0, GOLD_L, 1), (.5, GOLD, 1), (1, GOLD_D, 1)], x2=1, y2=1)
                + '" stroke-width="17" stroke-linecap="round"/>')
    lens_clip = d.clip(f'<circle cx="{lx}" cy="{ly}" r="{lr - 7}"/>')
    inner = [f'<circle cx="{lx}" cy="{ly}" r="{lr}" fill="#FCF8F0"/>',
             tissue_field(d, rng, (lx - lr, ly - lr, lx + lr, ly + lr), 1.85)]
    # the three things worth seeing, magnified
    inner.append(specks(rng, 46, (lx - 120, ly - 150, lx + 60, ly + 20), (5, 15), PIG, (.12, .34)))
    inner.append(f'<path d="M {fmt(lx - 60)} {fmt(ly + 108)} C {fmt(lx + 10)} {fmt(ly + 74)} '
                 f'{fmt(lx + 90)} {fmt(ly + 122)} {fmt(lx + 168)} {fmt(ly + 92)}" '
                 f'stroke="#FFFFFF" stroke-width="34" opacity=".8" stroke-linecap="round" '
                 f'filter="{d.blur(5)}"/>')
    inner.append(f'<path d="M {fmt(lx + 44)} {fmt(ly - 96)} l 14 40 l -10 34 l 18 40" '
                 f'fill="none" stroke="{INK}" stroke-width="3.4" opacity=".55" '
                 f'stroke-linecap="round"/>')
    body.append(f'<g clip-path="{lens_clip}">{"".join(inner)}</g>')
    body.append(f'<circle cx="{lx}" cy="{ly}" r="{lr - 7}" fill="'
                + d.rad([(0, "#FFFFFF", .46), (.5, "#FFFFFF", .06), (1, "#FFFFFF", 0)],
                        cx=.32, cy=.26, r=.62) + '"/>')
    body.append(f'<circle cx="{lx}" cy="{ly}" r="{fmt(lr - 3)}" fill="none" stroke="'
                + d.lin([(0, GOLD_L, 1), (.45, GOLD, 1), (1, GOLD_D, 1)], x2=.4, y2=1)
                + '" stroke-width="11"/>')
    body.append(ring(lx, ly, lr + 16, GOLD, .22, 1, "3 10"))

    # --- the three discriminations
    vx = 1044
    cases = [(vx, 236, "pigment"), (vx, 478, "sclerosis"), (vx, 720, "lesion")]
    for cx, cy, kind in cases:
        vr = 112
        ins = [tissue_field(d, rng, (cx - vr, cy - vr, cx + vr, cy + vr), 1.15, "#FAF5EA")]
        if kind == "pigment":
            ins.append(glow(d, cx, cy, 74, PIG, .3, 10))
            ins.append(specks(rng, 90, (cx - 78, cy - 70, cx + 78, cy + 70), (3, 9), PIG, (.12, .4)))
        elif kind == "sclerosis":
            ins.append(f'<path d="M {fmt(cx - vr)} {fmt(cy + 16)} C {fmt(cx - 40)} {fmt(cy - 26)} '
                       f'{fmt(cx + 40)} {fmt(cy + 44)} {fmt(cx + vr)} {fmt(cy - 6)}" '
                       f'stroke="#FFFFFF" stroke-width="76" opacity=".92" filter="{d.blur(5)}"/>')
            ins.append(f'<path d="M {fmt(cx - vr)} {fmt(cy + 16)} C {fmt(cx - 40)} {fmt(cy - 26)} '
                       f'{fmt(cx + 40)} {fmt(cy + 44)} {fmt(cx + vr)} {fmt(cy - 6)}" '
                       f'stroke="#FFFFFF" stroke-width="30" opacity=".95" filter="{d.blur(2)}"/>')
            for i in range(13):
                xx = cx - 96 + i * 16
                ins.append(f'<path d="M {fmt(xx)} {fmt(cy - 22)} q {fmt(rng.uniform(-7, 7))} 24 '
                           f'{fmt(rng.uniform(-6, 6))} 46" fill="none" stroke="#DCD3C1" '
                           f'stroke-width="1.3" opacity=".85"/>')
            ins.append(f'<path d="M {fmt(cx - 70)} {fmt(cy - 4)} q 70 -22 140 6" fill="none" '
                       f'stroke="#FFFFFF" stroke-width="7" opacity=".9"/>')
        else:
            ins.append(glow(d, cx, cy, 86, "#3A2A18", .3, 20))
            ins.append(f'<path d="{blob(cx + 4, cy - 2, 62, rng, .44, 11)}" '
                       f'fill="#2A1C0C" opacity=".74"/>')
            ins.append(f'<path d="{blob(cx - 26, cy + 34, 26, rng, .5, 9)}" '
                       f'fill="#2A1C0C" opacity=".5"/>')
            ins.append(specks(rng, 34, (cx - 78, cy - 80, cx + 78, cy + 74), (2, 8), "#2A1C0C", (.2, .5)))
        body.append(disc(d, cx, cy, vr, "".join(ins), halo=.3 if kind == "lesion" else .2))
        a = math.atan2(cy - ly, cx - lx)
        body.append(f'<path d="M {fmt(lx + (lr + 22) * math.cos(a))} {fmt(ly + (lr + 22) * math.sin(a))} '
                    f'L {fmt(cx - (vr + 12) * math.cos(a))} {fmt(cy - (vr + 12) * math.sin(a))}" '
                    f'stroke="{GOLD}" stroke-width="1.2" opacity=".42" stroke-dasharray="2 8"/>')

    # the one that must never be missed
    body.append(ring(vx, 720, 126, GOLD, .75, 2.2))
    body.append(bead(d, vx + 126 * math.cos(-.78), 720 + 126 * math.sin(-.78), 6))

    # --- the sorting grid
    gx, gy, cell, gap = 1224, 322, 92, 13
    for r_ in range(3):
        for c_ in range(3):
            x, y = gx + c_ * (cell + gap), gy + r_ * (cell + gap)
            hot = (r_, c_) == (2, 2)
            body.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="6" '
                        f'fill="#FFFFFF" opacity="{.5 if not hot else .78}" stroke="'
                        f'{GOLD if hot else STONE}" stroke-width="{2.2 if hot else 1}" '
                        f'stroke-opacity="{.85 if hot else .45}"/>')
            cxc, cyc = x + cell / 2, y + cell / 2
            k = (r_ * 3 + c_) % 3
            if k == 0:
                body.append(specks(rng, 16, (x + 16, y + 16, x + cell - 16, y + cell - 16),
                                   (2, 5), PIG, (.2, .5)))
            elif k == 1:
                body.append(f'<path d="M {x + 18} {cyc + 10} q 22 -26 {cell - 36} 2" fill="none" '
                            f'stroke="{STONE}" stroke-width="2" opacity=".6"/>')
            else:
                body.append(f'<path d="M {cxc - 6} {y + 20} l 10 24 l -8 20 l 12 16" fill="none" '
                            f'stroke="{INK}" stroke-width="1.8" opacity=".45"/>')
            if hot:
                body.append(bead(d, cxc, cyc, 7))
    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", 0), (.6, "#FFFFFF", 0), (1, "#EDE3CE", .55)], r=.8)
                + '"/>')

    write("04-clinical-assessment.svg", d, "".join(body),
          "What the eye has to separate",
          "The same field read three ways: diffuse pigment, a sclerotic band and a "
          "fixed irregular lesion, with the one that must never be missed ringed in "
          "gold and sorted out of the grid.")


# =====================================================================
# V - The Treatment Pyramid : six tiers, climbed slowly
# =====================================================================
def ch5_pyramid():
    d = Defs("p")
    rng = random.Random(55)
    body = [ground(d, seed=7, warm=(980, 200))]

    apex_y, base_y, cx = 178, 790, 690
    hw_top, hw_base = 46, 424
    n = 6
    th = (base_y - apex_y) / n

    def hw(y):
        return hw_top + (hw_base - hw_top) * (y - apex_y) / (base_y - apex_y)

    body.append(ring(cx, 470, 400, GOLD, .16, 1, "3 12"))
    body.append(ring(cx, 470, 468, GOLD, .1, 1))
    body.append(glow(d, cx, 300, 320, GOLD, .3, 40))

    for i in range(n):  # 0 = base
        y_b = base_y - i * th - 3
        y_t = y_b - th + 6
        wb, wt = hw(y_b), hw(y_t)
        t = i / (n - 1)
        fill = d.lin([(0, "#FFFFFF", .95 - .12 * t), (.4, "#FBF4E4", .92 - .14 * t),
                      (1, "#E9DAB8", .95 - .12 * t)], x1=0, y1=0, x2=.35, y2=1)
        tint = d.lin([(0, GOLD_L, .06 + .3 * t), (1, GOLD, .1 + .34 * t)], x2=.4, y2=1)
        body.append(f'<path d="M {fmt(cx - wb)} {fmt(y_b)} L {fmt(cx + wb)} {fmt(y_b)} '
                    f'L {fmt(cx + wt)} {fmt(y_t)} L {fmt(cx - wt)} {fmt(y_t)} Z" fill="{fill}" '
                    f'stroke="{GOLD}" stroke-width="{fmt(1 + 1.6 * t)}" '
                    f'stroke-opacity="{fmt(.3 + .55 * t)}"/>')
        body.append(f'<path d="M {fmt(cx - wb)} {fmt(y_b)} L {fmt(cx + wb)} {fmt(y_b)} '
                    f'L {fmt(cx + wt)} {fmt(y_t)} L {fmt(cx - wt)} {fmt(y_t)} Z" fill="{tint}"/>')
        # a whisper of the tier's own texture
        body.append(specks(rng, int(26 - 3 * i), (cx - wb + 26, y_t + 14, cx + wb - 26, y_b - 12),
                           (1.6, 4.2), GOLD, (.1, .26 + .1 * t)))
        if i == n - 1:
            body.append(glow(d, cx, (y_b + y_t) / 2, 120, GOLD, .5, 20))
            body.append(bead(d, cx, y_t - 22, 7))

        # the ascent, marked on the left
        my = (y_b + y_t) / 2
        body.append(f'<path d="M 152 {fmt(my)} L {fmt(cx - hw(my) - 26)} {fmt(my)}" '
                    f'stroke="{GOLD}" stroke-width="1.1" opacity=".4" stroke-dasharray="2 8"/>')
        body.append(bead(d, 152, my, 4.6 + 1.6 * t, GOLD, halo=t > .5))

        # what each tier actually is, as a mark rather than a word
        mx = 1244
        body.append(f'<path d="M {fmt(cx + hw(my) + 26)} {fmt(my)} L {fmt(mx - 62)} {fmt(my)}" '
                    f'stroke="{GOLD}" stroke-width="1.1" opacity=".38" stroke-dasharray="2 8"/>')
        body.append(f'<circle cx="{fmt(mx)}" cy="{fmt(my)}" r="52" fill="#FFFFFF" opacity=".42" '
                    f'stroke="{GOLD}" stroke-width="1" stroke-opacity="{fmt(.22 + .4 * t)}"/>')
        g = []
        if i == 0:      # lifestyle - small daily steps
            for k in range(3):
                g.append(bead(d, mx - 30 + k * 30, my + 14 - k * 14, 4.6, GOLD, halo=False))
                if k:
                    g.append(f'<path d="M {fmt(mx - 30 + (k - 1) * 30 + 8)} '
                             f'{fmt(my + 14 - (k - 1) * 14 - 4)} L {fmt(mx - 30 + k * 30 - 8)} '
                             f'{fmt(my + 14 - k * 14 + 4)}" stroke="{GOLD}" stroke-width="1.4" '
                             f'opacity=".45"/>')
        elif i == 1:    # home care - a droplet over a calm surface
            g.append(f'<path d="M {fmt(mx)} {fmt(my - 22)} c 16 20 12 34 0 34 c -12 0 -16 -14 0 -34 Z" '
                     f'fill="{GOLD}" opacity=".4"/>')
            g.append(strand([(mx - 34, my + 22), (mx, my + 16), (mx + 34, my + 22)], WARM, .5, 2))
        elif i == 2:    # topicals - a molecule settling into the surface
            for k, rr in enumerate((8, 15, 22)):
                g.append(ring(mx, my, rr, GOLD, .5 - k * .12, 1.6))
            g.append(bead(d, mx, my, 4, GOLD, halo=False))
        elif i == 3:    # injectables - a fine needle and its bolus
            g.append(f'<path d="M {fmt(mx - 32)} {fmt(my - 22)} L {fmt(mx + 14)} {fmt(my + 14)}" '
                     f'stroke="{WARM}" stroke-width="2.2" opacity=".6" stroke-linecap="round"/>')
            g.append(glow(d, mx + 22, my + 20, 26, GOLD, .6, 10))
            g.append(bead(d, mx + 22, my + 20, 5))
        elif i == 4:    # energy - columns of heat
            for k in range(3):
                x = mx - 26 + k * 26
                g.append(f'<path d="M {fmt(x)} {fmt(my - 24)} L {fmt(x)} {fmt(my + 22)}" '
                         f'stroke="{GOLD}" stroke-width="3" opacity=".55" stroke-linecap="round"/>')
                g.append(glow(d, x, my + 8, 17, GOLD, .5, 5))
        else:           # surgery - one deliberate line
            g.append(f'<path d="M {fmt(mx - 34)} {fmt(my + 10)} L {fmt(mx + 34)} {fmt(my - 10)}" '
                     f'stroke="{INK}" stroke-width="2" opacity=".5" stroke-linecap="round"/>')
            g.append(bead(d, mx - 34, my + 10, 3.6, GOLD, halo=False))
            g.append(bead(d, mx + 34, my - 10, 3.6, GOLD, halo=False))
        body.append("".join(g))

    # escalate slowly: the arrow beside the ascent
    body.append(strand([(152, 768), (152, 232)], GOLD, .5, 1.8, dash="5 10"))
    body.append(head(152, 214, -math.pi / 2, 14, GOLD, .75))

    # the base is the foundation, so it is the one that reflects
    body.append(f'<g transform="translate(0 {fmt(2 * base_y + 10)}) scale(1 -1)" opacity=".1" '
                f'filter="{d.blur(10)}"><path d="M {fmt(cx - hw_base)} {fmt(base_y)} '
                f'L {fmt(cx + hw_base)} {fmt(base_y)} L {fmt(cx + hw(base_y - 200))} '
                f'{fmt(base_y - 200)} L {fmt(cx - hw(base_y - 200))} {fmt(base_y - 200)} Z" '
                f'fill="{PIG_L}"/></g>')
    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", 0), (.6, "#FFFFFF", 0), (1, "#EDE3CE", .55)], r=.8)
                + '"/>')

    write("05-treatment-pyramid.svg", d, "".join(body),
          "Six tiers, climbed slowly",
          "Lifestyle, home care, topicals, injectables, energy, surgery - each tier "
          "marked by what it actually does, the ascent dotted up the left, the apex "
          "small and bright because it is the exception and not the default.")


# =====================================================================
# VI - Home Care : the barrier, and the cycle it interrupts
# =====================================================================
def lamellae(d, rng, box, rows=9, intact=True, gold=True):
    x0, y0, x1, y1 = box
    out = []
    dy = (y1 - y0) / rows
    for r_ in range(rows):
        y = y0 + r_ * dy + dy / 2
        x = x0 + (r_ % 2) * 34
        while x < x1:
            w = rng.uniform(30, 46)
            h = dy * .38
            out.append(f'<ellipse cx="{fmt(x)}" cy="{fmt(y)}" rx="{fmt(w)}" ry="{fmt(h)}" '
                       f'fill="' + d.rad([(0, "#FFFFFF", .96), (.66, "#F9F3E6", .92),
                                          (1, "#E6D9BE", .94)], cx=.34, cy=.3, r=.85)
                       + f'" stroke="#D3C4A4" stroke-width="1.2"/>')
            x += w * 2.15
        if gold:
            out.append(f'<path d="{wave(y + dy / 2, 5, r_ * .8, n=4, x0=x0, x1=x1)}" fill="none" '
                       f'stroke="{GOLD}" stroke-width="2.4" opacity="{.62 if intact else .2}" '
                       f'{"" if intact else chr(115) + chr(116) + "roke-dasharray=" + chr(34) + "9 13" + chr(34)}/>')
    return "".join(out)


def ch6_home_care():
    d = Defs("h")
    rng = random.Random(66)
    body = [ground(d, seed=2, warm=(1160, 240))]

    # --- the barrier itself: lipid lamellae, mortar in gold
    fade = d.mask('<rect x="-80" y="100" width="880" height="680" fill="'
                  + d.rad([(0, "#FFFFFF", 1), (.5, "#FFFFFF", 1), (1, "#000000", 1)],
                          cx=.28, cy=.5, r=.78) + '"/>')
    body.append(f'<g mask="{fade}">{lamellae(d, rng, (-60, 170, 760, 640), 9)}</g>')
    for _ in range(16):
        x, y = rng.uniform(20, 660), rng.uniform(180, 630)
        r = rng.uniform(5, 13)
        body.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="'
                    + d.rad([(0, "#FFF8E2", .95), (.6, GOLD_L, .8), (1, GOLD, .55)], cx=.34, cy=.3)
                    + '"/>')
    body.append(glow(d, 300, 380, 260, "#FFF6DE", .55, 40))

    # --- the cycle that friction starts, and the barrier interrupts
    ccx, ccy, cr, vr = 1136, 402, 240, 86
    body.append(ring(ccx, ccy, cr + 84, GOLD, .12, 1))
    body.append(ring(ccx, ccy, cr, GOLD, .18, 1, "3 11"))

    seats = [(-math.pi / 2, "friction"), (0.0, "inflammation"),
             (math.pi / 2, "pigment"), (math.pi, "restored")]
    for a, kind in seats:
        x, y = ccx + cr * math.cos(a), ccy + cr * math.sin(a)
        ins = []
        if kind == "friction":
            ins.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{vr}" fill="#F6F0E2"/>')
            for i in range(9):
                ins.append(f'<path d="M {fmt(x - vr)} {fmt(y - 70 + i * 18)} '
                           f'L {fmt(x + vr)} {fmt(y - 84 + i * 18)}" stroke="{STONE}" '
                           f'stroke-width="2.4" opacity=".55"/>')
            ins.append(head(x + 50, y - 6, 0, 14, WARM, .7))
            ins.append(head(x - 50, y + 14, math.pi, 14, WARM, .7))
        elif kind == "inflammation":
            ins.append(glow(d, x, y, 76, ROSE, .62, 20))
            ins.append(specks(rng, 110, (x - vr, y - vr, x + vr, y + vr), (2.4, 8), ROSE, (.15, .5)))
            for _ in range(7):
                sx, sy = rng.uniform(x - 60, x + 60), rng.uniform(y - 60, y + 60)
                ins.append(strand([(sx, sy), (sx + 26, sy + 14), (sx + 52, sy + 4)], ROSE_L, .6, 2.4))
        elif kind == "pigment":
            ins.append(glow(d, x, y, 70, PIG, .4, 20))
            ins.append(specks(rng, 130, (x - vr, y - vr, x + vr, y + vr), (2.2, 9), PIG, (.14, .5)))
            ins.append(f'<path d="{blob(x, y, 46, rng, .38, 10)}" fill="{PIG}" opacity=".22"/>')
        else:
            ins.append(lamellae(d, rng, (x - vr, y - vr + 14, x + vr, y + vr - 14), 5))
            ins.append(glow(d, x, y, 64, GOLD, .34, 20))
        body.append(disc(d, x, y, vr, "".join(ins),
                         halo=.34 if kind != "restored" else .42))

    # the loop, and where the barrier breaks it
    for a0, a1 in ((-math.pi / 2 + .42, -.42), (.42, math.pi / 2 - .42),
                   (math.pi / 2 + .42, math.pi - .42),
                   (math.pi + .42, 3 * math.pi / 2 - .42)):
        body.append(arc_arrow(ccx, ccy, cr, a0, a1, GOLD, .72, 3.3))

    shield_w, shield_h = 52, 62
    sh = (f"M {ccx - shield_w} {ccy - shield_h} L {ccx + shield_w} {ccy - shield_h} "
          f"L {ccx + shield_w} {ccy + shield_h * .2} Q {ccx + shield_w} {ccy + shield_h * .78} "
          f"{ccx} {ccy + shield_h} Q {ccx - shield_w} {ccy + shield_h * .78} "
          f"{ccx - shield_w} {ccy + shield_h * .2} Z")
    body.append(glow(d, ccx, ccy, 150, GOLD, .55, 40))
    body.append(f'<path d="{sh}" fill="'
                + d.lin([(0, "#FFF7E2", 1), (.45, GOLD_L, 1), (1, GOLD, 1)], x2=.6, y2=1)
                + f'" stroke="{GOLD_D}" stroke-width="1.6" stroke-opacity=".55"/>')
    body.append(f'<path d="{sh}" fill="'
                + d.lin([(0, "#FFFFFF", .55), (.5, "#FFFFFF", 0)], x2=.7, y2=1) + '"/>')

    # the two arms the barrier actually blocks
    for a in (0.0, math.pi / 2):
        x1, y1 = ccx + (cr - vr - 18) * math.cos(a), ccy + (cr - vr - 18) * math.sin(a)
        x0, y0 = ccx + 78 * math.cos(a), ccy + 78 * math.sin(a)
        body.append(f'<path d="M {fmt(x0)} {fmt(y0)} L {fmt(x1)} {fmt(y1)}" stroke="{GOLD}" '
                    f'stroke-width="2.6" opacity=".7" stroke-dasharray="8 8" '
                    f'stroke-linecap="round"/>')
        px, py = math.cos(a + math.pi / 2), math.sin(a + math.pi / 2)
        body.append(f'<path d="M {fmt(x1 - 19 * px)} {fmt(y1 - 19 * py)} '
                    f'L {fmt(x1 + 19 * px)} {fmt(y1 + 19 * py)}" stroke="{GOLD}" '
                    f'stroke-width="4" opacity=".9" stroke-linecap="round"/>')
        body.append(glow(d, x1, y1, 34, GOLD, .5, 10))

    # --- the everyday: cloth, water, emollient
    weave = []
    for i in range(16):
        weave.append(f'<path d="{wave(742 + i * 11, 13, i * .5, n=5, x0=-60, x1=1000)}" '
                     f'fill="none" stroke="#E6DCC6" stroke-width="2.6" opacity=".55"/>')
    for i in range(52):
        x = -40 + i * 21
        weave.append(f'<path d="M {fmt(x)} 736 C {fmt(x + 8)} 800 {fmt(x - 8)} 850 {fmt(x)} 906" '
                     f'fill="none" stroke="#EFE7D5" stroke-width="2" opacity=".5"/>')
    cloth = d.mask('<rect x="-80" y="700" width="1180" height="240" fill="'
                   + d.rad([(0, "#FFFFFF", 1), (.52, "#FFFFFF", 1), (1, "#000000", 1)],
                           cx=.34, cy=.42, r=.72) + '"/>')
    body.append(f'<g mask="{cloth}">{"".join(weave)}</g>')
    for cxx, cyy, rr in ((372, 830, 22), (438, 856, 11), (300, 862, 8)):
        body.append(f'<circle cx="{cxx}" cy="{cyy}" r="{rr}" fill="'
                    + d.rad([(0, "#FFFFFF", .95), (.62, "#F6F1E6", .55), (1, "#FFFFFF", .8)],
                            cx=.34, cy=.3) + f'" stroke="#E2DAC8" stroke-width="1"/>')
        body.append(f'<circle cx="{fmt(cxx - rr * .3)}" cy="{fmt(cyy - rr * .34)}" '
                    f'r="{fmt(rr * .26)}" fill="#FFFFFF" opacity=".9"/>')
    swirl = ("M 1180 872 C 1180 812 1268 792 1322 822 C 1372 850 1366 906 1316 916 "
             "C 1268 926 1222 906 1204 874 C 1246 902 1300 902 1318 878 "
             "C 1336 854 1310 826 1272 828 C 1230 830 1206 850 1198 878 Z")
    body.append(f'<path d="{swirl}" fill="'
                + d.lin([(0, "#FFFFFF", .98), (.55, "#FBF5E9", .96), (1, "#EDE3CE", .96)], y2=1)
                + f'" stroke="#E4DAC4" stroke-width="1"/>')
    body.append(glow(d, 1272, 868, 120, "#FFFFFF", .5, 20))

    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", 0), (.6, "#FFFFFF", 0), (1, "#EDE3CE", .5)], r=.82)
                + '"/>')

    write("06-home-care.svg", d, "".join(body),
          "The barrier, and the cycle it interrupts",
          "Intact lipid lamellae on the left; on the right the loop that friction "
          "starts - shear, inflammation, melanocyte activation, pigment - with a gold "
          "barrier at its centre stopping two of its arms, over cloth, water and "
          "emollient.")


# =====================================================================
# VII - Topicals : the pathway, and the four places it can be held
# =====================================================================
def ch7_topicals():
    d = Defs("t")
    rng = random.Random(77)
    body = [ground(d, seed=9, warm=(880, 700))]

    y = 452
    nodes = [(196, "tyrosine"), (432, "enzyme"), (668, "dopa"),
             (904, "melanosome"), (1160, "keratinocyte"), (1408, "surface")]
    for i in range(len(nodes) - 1):
        x0 = nodes[i][0] + (52 if nodes[i][1] != "keratinocyte" else 86)
        x1 = nodes[i + 1][0] - (52 if nodes[i + 1][1] != "keratinocyte" else 86)
        body.append(f'<path d="M {fmt(x0)} {fmt(y)} L {fmt(x1 - 14)} {fmt(y)}" stroke="{GOLD}" '
                    f'stroke-width="2.2" opacity=".55"/>')
        body.append(head(x1 - 4, y, 0, 12, GOLD, .7))

    for x, kind in nodes:
        if kind == "tyrosine":
            ins = [ring(x, y, 22, WARM, .6, 2), ring(x, y, 11, WARM, .45, 1.6),
                   bead(d, x, y, 4, GOLD, halo=False)]
            body.append(disc(d, x, y, 48, "".join(ins), halo=.16))
        elif kind == "enzyme":
            ins = [f'<path d="{blob(x, y, 32, rng, .2, 9)}" fill="{GOLD}" fill-opacity=".22" '
                   f'stroke="{GOLD}" stroke-width="1.6" stroke-opacity=".7"/>',
                   f'<path d="M {fmt(x - 12)} {fmt(y - 4)} q 12 16 24 0" fill="none" '
                   f'stroke="{GOLD_D}" stroke-width="2" opacity=".6"/>',
                   glow(d, x, y, 40, GOLD, .4, 10)]
            body.append(disc(d, x, y, 48, "".join(ins), rim=.8, halo=.3))
        elif kind == "dopa":
            ins = [ring(x, y - 8, 17, WARM, .6, 2), ring(x + 15, y + 12, 13, WARM, .5, 1.8),
                   bead(d, x - 14, y + 12, 3.6, PIG_L, halo=False)]
            body.append(disc(d, x, y, 48, "".join(ins), halo=.16))
        elif kind == "melanosome":
            ins = [f'<ellipse cx="{x}" cy="{y}" rx="30" ry="20" fill="{PIG}" opacity=".55"/>',
                   specks(rng, 26, (x - 28, y - 18, x + 28, y + 18), (1.6, 4), "#3D2C16", (.3, .6))]
            body.append(disc(d, x, y, 48, "".join(ins), halo=.16))
        elif kind == "keratinocyte":
            ins = [f'<ellipse cx="{x}" cy="{y}" rx="62" ry="46" fill="#FAF4E8" opacity=".95" '
                   f'stroke="#D9CDB4" stroke-width="1.2"/>',
                   f'<ellipse cx="{x}" cy="{y}" rx="17" ry="14" fill="{WARM}" opacity=".3"/>',
                   specks(rng, 15, (x - 48, y - 34, x + 48, y + 34), (2.4, 5.6), PIG, (.25, .55))]
            body.append(disc(d, x, y, 82, "".join(ins), halo=.18))
        else:
            ins = [lamellae(d, rng, (x - 52, y - 40, x + 52, y + 40), 4, gold=False),
                   specks(rng, 28, (x - 46, y - 36, x + 46, y + 36), (2, 5.4), PIG, (.2, .5))]
            body.append(disc(d, x, y, 52, "".join(ins), halo=.18))

    # the four levers - each one holds the pathway at a different point
    levers = [(196, "signal"), (432, "enzyme"), (1032, "transfer"), (1408, "turnover")]
    for x, _ in levers:
        body.append(f'<path d="M {fmt(x)} 168 L {fmt(x)} {fmt(y - 96)}" stroke="{GOLD}" '
                    f'stroke-width="2.4" opacity=".6" stroke-dasharray="9 8" stroke-linecap="round"/>')
        body.append(f'<path d="M {fmt(x - 26)} {fmt(y - 92)} L {fmt(x + 26)} {fmt(y - 92)}" '
                    f'stroke="{GOLD}" stroke-width="4.2" opacity=".9" stroke-linecap="round"/>')
        body.append(glow(d, x, y - 92, 40, GOLD, .45, 10))
        body.append(bead(d, x, 168, 6.4))
    body.append(f'<path d="M 196 168 L 1408 168" stroke="{GOLD}" stroke-width="1.2" '
                f'opacity=".3" stroke-dasharray="2 9"/>')

    # not every agent belongs on mucosa: gentle, careful, never
    bx, by, bw, bh = 300, 716, 1000, 64
    body.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="32" fill="'
                + d.lin([(0, "#F7F1E3", .92), (.42, GOLD_L, .55), (1, "#8E4A34", .55)], x2=1)
                + f'" stroke="{GOLD}" stroke-width="1" stroke-opacity=".4"/>')
    for k in range(3):
        cx = bx + bw * (.17 + k * .33)
        body.append(f'<circle cx="{fmt(cx)}" cy="{fmt(by + bh / 2)}" r="21" fill="#FFFFFF" '
                    f'opacity="{fmt(.8 - k * .12)}" stroke="{GOLD}" stroke-width="1.2" '
                    f'stroke-opacity=".5"/>')
        if k == 0:
            body.append(f'<path d="M {fmt(cx - 9)} {fmt(by + bh / 2)} l 7 8 l 12 -15" fill="none" '
                        f'stroke="{GOLD_D}" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>')
        elif k == 1:
            body.append(f'<path d="M {fmt(cx)} {fmt(by + bh / 2 - 9)} l 0 10 M {fmt(cx)} '
                        f'{fmt(by + bh / 2 + 6)} l 0 3" stroke="{GOLD_D}" stroke-width="2.6" '
                        f'stroke-linecap="round" opacity=".8"/>')
        else:
            body.append(f'<path d="M {fmt(cx - 8)} {fmt(by + bh / 2 - 8)} l 16 16 M {fmt(cx + 8)} '
                        f'{fmt(by + bh / 2 - 8)} l -16 16" stroke="#8E4A34" stroke-width="2.6" '
                        f'stroke-linecap="round" opacity=".85"/>')
    body.append(specks(rng, 30, (160, 220, 1460, 660), (1, 3), GOLD, (.1, .3)))
    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", 0), (.62, "#FFFFFF", 0), (1, "#EDE3CE", .5)], r=.8)
                + '"/>')

    write("07-topicals.svg", d, "".join(body),
          "The pathway, and the four places it can be held",
          "Tyrosine through tyrosinase to DOPA, melanosome and transfer into the "
          "keratinocyte, with the four levers - enzyme, signal, transfer, turnover - "
          "marked as holds on the chain, over a gentle-to-never safety gradient.")


# =====================================================================
# VIII - Regenerative Injectables : depletion, activation, restoration
# =====================================================================
def ch8_injectables():
    d = Defs("g")
    rng = random.Random(88)
    body = [ground(d, seed=4, warm=(1300, 420))]

    stages = [(336, 460, 0.0), (800, 460, .5), (1264, 460, 1.0)]
    r = 194

    # the thread that runs through all three
    body.append(f'<path d="M 80 460 C 420 400 1180 520 1520 460" fill="none" stroke="{GOLD}" '
                f'stroke-width="22" opacity=".12" filter="{d.blur(20)}"/>')
    body.append(f'<path d="M 80 460 C 420 400 1180 520 1520 460" fill="none" stroke="{GOLD}" '
                f'stroke-width="1.6" opacity=".45" stroke-dasharray="3 10"/>')

    for cx, cy, t in stages:
        ins = []
        if t == 0.0:
            ins.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{COOL}" opacity=".12"/>')
            for i in range(11):
                yy = cy - 150 + i * 30
                pts = [(cx - r + k * (2 * r / 5), yy + rng.uniform(-9, 9)) for k in range(6)]
                ins.append(strand(pts[:3], COOL_D, .32, 2.2))
                ins.append(strand(pts[3:], COOL_D, .26, 1.8))
            for _ in range(7):
                x, yy = rng.uniform(cx - 130, cx + 130), rng.uniform(cy - 130, cy + 130)
                ins.append(f'<ellipse cx="{fmt(x)}" cy="{fmt(yy)}" rx="16" ry="9" fill="#EFEDE9" '
                           f'opacity=".85" stroke="{COOL}" stroke-width="1"/>')
            ins.append(specks(rng, 30, (cx - r, cy - r, cx + r, cy + r), (1.4, 3.4), COOL_D, (.1, .3)))
        elif t == .5:
            ins.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD_L}" opacity=".1"/>')
            for i in range(9):
                yy = cy - 140 + i * 35
                ins.append(fibre(rng, cx - r, cx + r, yy, amp=12, n=6,
                                 color=rng.choice([GOLD, "#C3B08A", COOL_D]),
                                 op=rng.uniform(.3, .6), wdt=rng.uniform(1.6, 3)))
            for k in range(5):
                ins.append(ring(cx, cy - 40, 28 + k * 30, GOLD, .34 - k * .05, 1.6))
            for _ in range(9):
                x, yy = rng.uniform(cx - 140, cx + 140), rng.uniform(cy - 120, cy + 140)
                a = fmt(math.degrees(rng.uniform(-.5, .5)))
                ins.append(f'<g transform="rotate({a} {fmt(x)} {fmt(yy)})">'
                           f'<ellipse cx="{fmt(x)}" cy="{fmt(yy)}" rx="26" ry="8" fill="#F8F2E4" '
                           f'opacity=".92" stroke="{GOLD}" stroke-width="1.1" stroke-opacity=".6"/>'
                           f'<path d="M {fmt(x - 26)} {fmt(yy)} l -15 -5 M {fmt(x + 26)} {fmt(yy)} '
                           f'l 15 5" stroke="{GOLD}" stroke-width="1.1" opacity=".5"/></g>')
            ins.append(glow(d, cx, cy - 40, 120, GOLD, .45, 20))
        else:
            ins.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD_L}" opacity=".16"/>')
            for i in range(15):
                yy = cy - 160 + i * 23
                ins.append(fibre(rng, cx - r, cx + r, yy, amp=9, n=8, color=GOLD,
                                 op=rng.uniform(.35, .7), wdt=rng.uniform(1.8, 3.8)))
            for i in range(5):
                xx = cx - 130 + i * 66
                ins.append(strand([(xx, cy - r), (xx + rng.uniform(-40, 40), cy - 60),
                                   (xx + rng.uniform(-50, 50), cy + 40),
                                   (xx + rng.uniform(-40, 40), cy + r)], GOLD_L, .2, 1.8))
            for _ in range(4):
                x, yy = rng.uniform(cx - 130, cx + 90), rng.uniform(cy - 120, cy + 120)
                ins.append(strand([(x, yy), (x + 46, yy + 22), (x + 96, yy + 6)], ROSE, .55, 3.4))
                ins.append(strand([(x + 46, yy + 22), (x + 72, yy + 64)], ROSE, .42, 2.2))
            ins.append(specks(rng, 46, (cx - r, cy - r, cx + r, cy + r), (2, 5.6), GOLD_L, (.2, .55)))
            ins.append(glow(d, cx, cy, 170, GOLD, .5, 40))
        body.append(disc(d, cx, cy, r, "".join(ins), rim=.4 + .4 * t, halo=.14 + .34 * t))

    # the stimulus, entering the middle
    dx, dy = 800, 168
    body.append(f'<path d="M {dx} {dy - 44} c 30 44 24 72 0 72 c -24 0 -30 -28 0 -72 Z" fill="'
                + d.lin([(0, "#FFF8E6", 1), (1, GOLD, 1)], y2=1)
                + f'" stroke="{GOLD_D}" stroke-width="1.2" stroke-opacity=".5"/>')
    body.append(glow(d, dx, dy + 10, 70, GOLD, .5, 20))
    body.append(f'<path d="M {dx} {dy + 40} L {dx} 244" stroke="{GOLD}" stroke-width="2" '
                f'opacity=".5" stroke-dasharray="6 8"/>')
    body.append(head(dx, 252, math.pi / 2, 12, GOLD, .75))

    # the two junctions
    for jx in (568, 1032):
        body.append(glow(d, jx, 460, 76, GOLD, .6, 20))
        body.append(bead(d, jx, 460, 8))
        for k in range(8):
            a = k * math.pi / 4
            body.append(f'<path d="M {fmt(jx + 16 * math.cos(a))} {fmt(460 + 16 * math.sin(a))} '
                        f'L {fmt(jx + 34 * math.cos(a))} {fmt(460 + 34 * math.sin(a))}" '
                        f'stroke="{GOLD}" stroke-width="1.4" opacity=".45"/>')
        body.append(head(jx + 54, 460, 0, 12, GOLD, .6))

    body.append(specks(rng, 34, (120, 140, 1500, 800), (1, 3.2), GOLD, (.1, .32)))
    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", 0), (.6, "#FFFFFF", 0), (1, "#EDE3CE", .52)], r=.82)
                + '"/>')

    write("08-regenerative-injectables.svg", d, "".join(body),
          "Depletion, activation, restoration",
          "A depleted matrix of broken grey fibres, the same field under a stimulus "
          "with fibroblasts activating along gold signal rings, and restored tissue - "
          "dense collagen, new microvessels, held water.")


# =====================================================================
# IX - Energy-Based Medicine : the depth map
# =====================================================================
def ch9_energy():
    d = Defs("e")
    rng = random.Random(99)
    body = [ground(d, seed=6, warm=(800, 120), veil=False)]

    epi_t, epi_b, deep = 268, 372, 900

    # the block of tissue every device has to negotiate
    body.append(f'<rect x="-20" y="{epi_t}" width="1640" height="{deep - epi_t}" fill="'
                + d.lin([(0, "#FAF5EA", .95), (.16, "#F6F0E2", .95), (1, "#EEE3CD", .95)], y2=1)
                + '"/>')
    body.append(f'<rect x="-20" y="{epi_t}" width="1640" height="{epi_b - epi_t}" fill="#FCF8F0" '
                f'opacity=".9"/>')
    body.append(f'<path d="M -20 {epi_b} L 1620 {epi_b}" stroke="{GOLD}" stroke-width="2.6" '
                f'opacity=".8"/>')
    body.append(f'<path d="M -20 {epi_t} L 1620 {epi_t}" stroke="#DCD0B6" stroke-width="1.6" '
                f'opacity=".8"/>')
    for i in range(20):
        body.append(fibre(rng, -40, 1640, epi_b + 26 + i * 27, amp=8, n=9,
                          color=rng.choice(["#DED0B2", "#D4C29B"]), op=rng.uniform(.28, .5),
                          wdt=rng.uniform(1.4, 3)))
    for _ in range(22):
        fx, fy = rng.uniform(20, 1580), rng.uniform(epi_b + 60, deep - 40)
        a = fmt(math.degrees(rng.uniform(-.3, .3)))
        body.append(f'<g transform="rotate({a} {fmt(fx)} {fmt(fy)})" opacity=".8">'
                    f'<ellipse cx="{fmt(fx)}" cy="{fmt(fy)}" rx="24" ry="8" fill="#F5EFE0" '
                    f'stroke="#CFC1A5" stroke-width="1"/>'
                    f'<ellipse cx="{fmt(fx)}" cy="{fmt(fy)}" rx="7.4" ry="4.2" fill="{WARM}" '
                    f'opacity=".34"/></g>')
    for sx in (240, 760, 1330):
        body.append(strand([(sx - 160, deep - 10), (sx - 60, deep - 110),
                            (sx + 40, deep - 90), (sx + 150, deep - 170)], ROSE, .34, 5))
    x = -10
    while x < 1620:
        body.append(f'<ellipse cx="{fmt(x)}" cy="{fmt(epi_t + 26)}" rx="17" ry="10" '
                    f'fill="#FDFAF4" stroke="#DED3BB" stroke-width=".9"/>')
        body.append(f'<ellipse cx="{fmt(x + 17)}" cy="{fmt(epi_t + 56)}" rx="17" ry="12" '
                    f'fill="#FBF6EC" stroke="#DED3BB" stroke-width=".9"/>')
        x += 35
    x = 8
    while x < 1620:
        body.append(f'<ellipse cx="{fmt(x)}" cy="{fmt(epi_b - 22)}" rx="18" ry="14" '
                    f'fill="#FAF4E9" stroke="#DED3BB" stroke-width=".9"/>')
        x += 37

    # depth scale
    for dy in (epi_b, epi_b + 170, epi_b + 340):
        body.append(f'<path d="M 40 {fmt(dy)} L 1560 {fmt(dy)}" stroke="{GOLD}" stroke-width="1" '
                    f'opacity=".2" stroke-dasharray="2 12"/>')
        body.append(bead(d, 40, dy, 4.4, GOLD, halo=False))

    zones = [(60, 500, "co2"), (600, 940, "erbium"), (1040, 1540, "rf")]
    for x0, x1, kind in zones:
        body.append(f'<rect x="{x0}" y="132" width="{x1 - x0}" height="{deep - 132}" rx="18" '
                    f'fill="#FFFFFF" opacity=".28" stroke="{GOLD}" stroke-width="1" '
                    f'stroke-opacity=".22"/>')
        n = 7 if kind != "erbium" else 9
        for i in range(n):
            cx = x0 + (x1 - x0) * (i + .5) / n
            if kind == "co2":
                depth = epi_b + 292 + rng.uniform(-30, 30)
                body.append(f'<path d="M {fmt(cx)} {fmt(epi_t + 4)} L {fmt(cx)} {fmt(depth)}" '
                            f'stroke="{GOLD}" stroke-width="16" opacity=".2" filter="{d.blur(10)}"/>')
                body.append(f'<path d="M {fmt(cx)} {fmt(epi_t + 4)} L {fmt(cx)} {fmt(depth)}" '
                            f'stroke="{GOLD}" stroke-width="5" opacity=".75" stroke-linecap="round"/>')
                body.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(depth)}" rx="15" ry="11" '
                            f'fill="{GOLD}" opacity=".3"/>')
            elif kind == "erbium":
                depth = epi_t + 34 + rng.uniform(-7, 7)
                body.append(f'<path d="M {fmt(cx)} {fmt(epi_t + 5)} L {fmt(cx)} {fmt(depth)}" '
                            f'stroke="{GOLD}" stroke-width="8" opacity=".78" stroke-linecap="round"/>')
                body.append(glow(d, cx, epi_t + 18, 26, GOLD, .55, 5))
            else:
                depth = epi_b + 288 + rng.uniform(-28, 28)
                tip = depth - 74
                body.append(f'<path d="M {fmt(cx - 7)} {fmt(epi_t - 118)} L {fmt(cx - 7)} '
                            f'{fmt(tip)} M {fmt(cx + 7)} {fmt(epi_t - 118)} L {fmt(cx + 7)} '
                            f'{fmt(tip)}" stroke="#CFC6B2" stroke-width="3.4" opacity=".8" '
                            f'stroke-linecap="round"/>')
                body.append(f'<path d="M {fmt(cx - 7)} {fmt(tip)} L {fmt(cx - 7)} {fmt(depth)} '
                            f'M {fmt(cx + 7)} {fmt(tip)} L {fmt(cx + 7)} {fmt(depth)}" '
                            f'stroke="{GOLD}" stroke-width="4.4" opacity=".85" stroke-linecap="round"/>')
                body.append(glow(d, cx, depth - 30, 54, GOLD, .6, 20))
                body.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(depth - 30)}" rx="24" ry="38" '
                            f'fill="{GOLD}" opacity=".2"/>')

        # what happens to melanin in the epidermis under each
        for i in range(14):
            mx = x0 + (x1 - x0) * (i + .5) / 14
            my = epi_b - 12
            if kind == "rf":
                body.append(f'<circle cx="{fmt(mx)}" cy="{fmt(my)}" r="5.4" fill="{PIG}" '
                            f'opacity=".42"/>')
            else:
                body.append(glow(d, mx, my, 22, ROSE, .5, 5))
                body.append(f'<circle cx="{fmt(mx)}" cy="{fmt(my)}" r="6" fill="{PIG}" '
                            f'opacity=".65"/>')
        if kind == "rf":
            body.append(f'<rect x="{x0 + 10}" y="{epi_t - 2}" width="{x1 - x0 - 20}" '
                        f'height="{epi_b - epi_t + 4}" rx="8" fill="none" stroke="{GOLD}" '
                        f'stroke-width="2.2" opacity=".75" stroke-dasharray="10 8"/>')

    body.append(specks(rng, 26, (80, 130, 1520, 200), (1, 3), GOLD, (.12, .34)))
    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", .1), (.6, "#FFFFFF", 0), (1, "#E9DFC9", .5)], r=.82)
                + '"/>')

    write("09-energy-based-medicine.svg", d, "".join(body),
          "The depth map",
          "Three ways of putting energy into the same tissue: fractional columns down "
          "into the dermis, very superficial ablation at the surface, and insulated "
          "needles that heat only at their tips - the first two lighting the epidermal "
          "melanin, the third leaving it alone.")


# =====================================================================
# X - The Kabboura Protocol : five streams, one tissue
# =====================================================================
def ch10_protocol():
    d = Defs("k")
    rng = random.Random(100)
    body = [ground(d, seed=1, warm=(1240, 430))]

    tx, ty, tr = 1236, 452, 216
    lanes = [
        (196, "#D8CDB6", 3.4),   # barrier
        (312, GOLD_D, 5.0),      # structure
        (436, GOLD, 5.6),        # regeneration
        (560, PIG_L, 4.2),       # pigment
        (684, STONE, 3.0),       # maintenance
    ]
    for i, (y0, col, wd) in enumerate(lanes):
        pts = [(88, y0), (300, y0 + (ty - y0) * .06), (560, y0 + (ty - y0) * .22),
               (820, y0 + (ty - y0) * .58), (1010, ty + (y0 - ty) * .12), (tx - tr + 10, ty)]
        body.append(strand(pts, col, .32, wd + 10))
        body.append(strand(pts, col, .72, wd))
        for k in (1, 3):
            body.append(bead(d, pts[k][0], pts[k][1], 4.4, GOLD, halo=False))
        body.append(bead(d, 88, y0, 7 + i * .2, GOLD if col == GOLD else col, halo=False))
        body.append(f'<path d="M 44 {fmt(y0)} L 74 {fmt(y0)}" stroke="{GOLD}" stroke-width="1.2" '
                    f'opacity=".4" stroke-dasharray="2 6"/>')
        # the order is the point
        for k in range(i + 1):
            body.append(f'<circle cx="{fmt(50 + k * 11)}" cy="{fmt(y0 - 26)}" r="3.4" '
                        f'fill="{GOLD}" opacity=".6"/>')

    body.append(glow(d, 1010, ty, 250, GOLD, .45, 40))
    body.append(glow(d, tx - tr + 6, ty, 110, "#FFF6DF", .9, 20))
    body.append(bead(d, tx - tr + 6, ty, 9))

    # the tissue the sequence is for
    ins = [lamellae(d, rng, (tx - tr, ty - tr + 30, tx + tr, ty - 30), 5)]
    for i in range(9):
        ins.append(fibre(rng, tx - tr, tx + tr, ty + 16 + i * 21, amp=10, n=8, color=GOLD,
                         op=rng.uniform(.3, .6), wdt=rng.uniform(1.6, 3.4)))
    ins.append(strand([(tx - 150, ty + 120), (tx - 40, ty + 150), (tx + 90, ty + 118)], ROSE, .5, 3.2))
    ins.append(specks(rng, 40, (tx - tr, ty - tr, tx + tr, ty + tr), (2, 5.4), GOLD_L, (.2, .55)))
    ins.append(glow(d, tx, ty, 190, GOLD, .4, 40))
    body.append(disc(d, tx, ty, tr, "".join(ins), rim=.8, halo=.42))
    body.append(ring(tx, ty, tr + 34, GOLD, .28, 1.2, "4 10"))
    body.append(bead_ring(tx, ty, tr + 58, 24, 2.6, GOLD, .32))

    body.append(f'<g transform="translate(0 {fmt(2 * (ty + tr) + 24)}) scale(1 -1)" '
                f'opacity=".1" filter="{d.blur(20)}">'
                f'<circle cx="{tx}" cy="{ty}" r="{tr}" fill="{PIG_L}"/></g>')
    body.append(specks(rng, 30, (120, 160, 980, 820), (1, 3), GOLD, (.1, .3)))
    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", 0), (.6, "#FFFFFF", 0), (1, "#EDE3CE", .52)], r=.82)
                + '"/>')

    write("10-the-kabboura-protocol.svg", d, "".join(body),
          "Five streams, one tissue",
          "Barrier, structure, regeneration, pigment and maintenance entering in "
          "order, braiding into a single course, and resolving into one restored "
          "field: structure before surface.")


# =====================================================================
# XI - The Future : helix, lattice, light
# =====================================================================
def ch11_future():
    d = Defs("f")
    rng = random.Random(111)
    body = [ground(d, seed=10, warm=(1320, 400))]

    # --- the helix
    hx, hy0, hy1 = 268, 168, 764
    steps = 58
    a_pts, b_pts = [], []
    for i in range(steps + 1):
        t = i / steps
        y = hy0 + (hy1 - hy0) * t
        ph = t * 17.0
        a_pts.append((hx + 92 * math.sin(ph), y))
        b_pts.append((hx + 92 * math.sin(ph + math.pi), y))
    for i in range(0, steps, 3):
        x0, y0 = a_pts[i]
        x1, y1 = b_pts[i]
        dep = abs(math.sin(i / steps * 17.0))
        body.append(f'<path d="M {fmt(x0)} {fmt(y0)} L {fmt(x1)} {fmt(y1)}" stroke="{GOLD}" '
                    f'stroke-width="1.8" opacity="{fmt(.2 + .34 * dep)}"/>')
    body.append(strand(a_pts, GOLD, .78, 3.4))
    body.append(strand(b_pts, "#C3B393", .6, 3.0))
    body.append(glow(d, hx, 466, 210, GOLD, .22, 40))

    # --- the lattice
    nodes = []
    for _ in range(30):
        nodes.append((rng.uniform(520, 980), rng.uniform(180, 760)))
    for i, (x, y) in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            x2, y2 = nodes[j]
            dist = math.hypot(x2 - x, y2 - y)
            if dist < 165:
                body.append(f'<path d="M {fmt(x)} {fmt(y)} L {fmt(x2)} {fmt(y2)}" '
                            f'stroke="{GOLD}" stroke-width="1" '
                            f'opacity="{fmt(.34 * (1 - dist / 165))}"/>')
    for x, y in nodes:
        body.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(rng.uniform(2.6, 5.4))}" '
                    f'fill="{GOLD}" opacity="{fmt(rng.uniform(.35, .75))}"/>')
    body.append(glow(d, 750, 460, 240, GOLD, .18, 70))

    # --- tissue coming back, and the light it goes into
    cx, cy = 1244, 452
    body.append(glow(d, cx, cy, 400, GOLD, .4, 70))
    body.append(glow(d, cx, cy, 230, "#FFF2CE", .62, 40))
    body.append(glow(d, cx + 120, cy - 40, 120, "#FFFDF6", .8, 20))
    for k in range(7):
        body.append(ring(cx, cy, 86 + k * 46, GOLD, .26 - k * .03, 1.2,
                         "3 10" if k % 2 else None))
    for i in range(13):
        y = cy - 190 + i * 32
        body.append(fibre(rng, cx - 200, cx + 200, y, amp=12, n=8, color=GOLD,
                          op=rng.uniform(.2, .5), wdt=rng.uniform(1.4, 3.2)))
    # a spiral of beads lifting out of it
    for i in range(30):
        t = i / 29
        a = t * 5.6
        rr = 60 + t * 320
        x = cx + rr * math.cos(a) * .92
        y = cy + rr * math.sin(a) * .5 - t * 120
        body.append(bead(d, x, y, 2.4 + 5 * t, GOLD, halo=t > .5))
    body.append(specks(rng, 60, (1020, 120, 1580, 820), (1, 3.6), GOLD, (.12, .45)))

    # the three moments, joined
    body.append(f'<path d="M 386 452 C 470 420 490 480 540 460" fill="none" stroke="{GOLD}" '
                f'stroke-width="1.6" opacity=".45" stroke-dasharray="3 9"/>')
    body.append(f'<path d="M 990 460 C 1040 440 1060 470 1100 452" fill="none" stroke="{GOLD}" '
                f'stroke-width="1.6" opacity=".45" stroke-dasharray="3 9"/>')
    body.append(bead(d, 466, 452, 5.6))
    body.append(bead(d, 1046, 452, 5.6))

    body.append(f'<rect width="{W}" height="{H}" fill="'
                + d.rad([(0, "#FFFFFF", 0), (.6, "#FFFFFF", 0), (1, "#EDE3CE", .5)], r=.84)
                + '"/>')

    write("11-the-future.svg", d, "".join(body),
          "Helix, lattice, light",
          "Genomics, machine-read data and regenerating tissue as one continuous "
          "movement - a helix resolving into a lattice, and the lattice into tissue "
          "and light.")


HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Intimate Ecosystem \u00b7 Chapter Illustrations</title>
<meta name="description" content="Eleven coordinated chapter illustrations for The Intimate Ecosystem, in chapter order.">
<style>
  @font-face { font-family:'Cormorant Garamond'; src:url('../deck/fonts/CormorantGaramond-400.ttf') format('truetype'); font-weight:400; font-display:swap; }
  @font-face { font-family:'Cormorant Garamond'; src:url('../deck/fonts/CormorantGaramond-600.ttf') format('truetype'); font-weight:600; font-display:swap; }
  @font-face { font-family:'Cormorant Garamond'; src:url('../deck/fonts/CormorantGaramond-400i.ttf') format('truetype'); font-weight:400; font-style:italic; font-display:swap; }
  @font-face { font-family:'Montserrat'; src:url('../deck/fonts/Montserrat-300.ttf') format('truetype'); font-weight:300; font-display:swap; }
  @font-face { font-family:'Montserrat'; src:url('../deck/fonts/Montserrat-500.ttf') format('truetype'); font-weight:500; font-display:swap; }

  :root {
    --paper:#FBF7EF; --ink:#2E2B26; --gold:#C6A24E; --gold-d:#8A6A1C;
    --warm:#8A7C68; --line:rgba(198,162,78,.28);
  }
  * { box-sizing:border-box; }
  html { scroll-behavior:smooth; }
  body {
    margin:0; background:var(--paper); color:var(--ink);
    font-family:'Montserrat',-apple-system,Helvetica,Arial,sans-serif; font-weight:300;
    -webkit-font-smoothing:antialiased;
  }
  header {
    padding:88px 24px 40px; text-align:center;
    background:radial-gradient(120% 90% at 70% 0%, #FFF7E6 0%, var(--paper) 62%);
  }
  .kicker {
    font-size:11px; letter-spacing:.34em; text-transform:uppercase;
    color:var(--gold-d); font-weight:500;
  }
  h1 {
    font-family:'Cormorant Garamond',Georgia,serif; font-weight:600;
    font-size:clamp(34px,5.4vw,60px); margin:14px 0 6px; letter-spacing:.01em;
  }
  .sub { font-size:14px; letter-spacing:.06em; color:var(--warm); margin:0 0 4px; }
  .rule { width:64px; height:1px; background:var(--gold); opacity:.6; margin:28px auto 0; }

  nav {
    position:sticky; top:0; z-index:5; display:flex; flex-wrap:wrap; gap:2px;
    justify-content:center; padding:12px 16px;
    background:rgba(251,247,239,.88); backdrop-filter:blur(8px);
    border-bottom:1px solid var(--line);
  }
  nav a {
    font-size:11px; letter-spacing:.16em; color:var(--warm); text-decoration:none;
    padding:6px 11px; border-radius:20px; transition:.2s;
  }
  nav a:hover { color:var(--gold-d); background:rgba(198,162,78,.1); }

  main { max-width:1240px; margin:0 auto; padding:56px 24px 120px; }
  .plate { margin:0 0 92px; scroll-margin-top:72px; }
  .meta { display:flex; align-items:baseline; gap:18px; margin-bottom:18px; }
  .num {
    font-family:'Cormorant Garamond',Georgia,serif; font-size:30px; color:var(--gold);
    min-width:52px; line-height:1;
  }
  .meta h2 {
    font-family:'Cormorant Garamond',Georgia,serif; font-weight:600;
    font-size:clamp(22px,2.6vw,30px); margin:0; letter-spacing:.01em;
  }
  .meta .t {
    margin:4px 0 0; font-size:11px; letter-spacing:.2em; text-transform:uppercase;
    color:var(--gold-d); font-weight:500;
  }
  .pair { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
  .pair.one { grid-template-columns:1fr; max-width:none; }
  .shot span {
    display:block; margin-top:9px; font-size:9.5px; letter-spacing:.24em;
    text-transform:uppercase; color:var(--warm); opacity:.8;
  }
  .plate img {
    display:block; width:100%; height:auto; border:1px solid var(--line);
    border-radius:3px; background:var(--paper);
    box-shadow:0 18px 50px -28px rgba(138,106,28,.45);
  }
  figcaption {
    max-width:64ch; margin:16px 0 0; font-size:14.5px; line-height:1.72;
    color:var(--warm);
  }
  footer {
    border-top:1px solid var(--line); padding:34px 24px 60px; text-align:center;
    font-size:11px; letter-spacing:.2em; text-transform:uppercase; color:var(--warm);
  }
  @media (max-width:640px) {
    header { padding:56px 20px 28px; }
    .meta { gap:12px; } .num { min-width:38px; font-size:24px; }
    .plate { margin-bottom:64px; }
    .pair { grid-template-columns:1fr; gap:26px; }
  }
  @media print {
    nav { display:none; } .plate { break-inside:avoid; margin-bottom:38px; }
  }
</style>
</head>
<body>
<header>
  <p class="kicker">International Masterclass &middot; Regenerative Intimate Medicine</p>
  <h1>The Intimate Ecosystem</h1>
  <p class="sub">Eleven coordinated chapter illustrations, in chapter order &middot; {{COUNT}}</p>
  <div class="rule"></div>
</header>
<nav>{{NAV}}</nav>
<main>
{{PLATES}}
</main>
<footer>The Intimate Ecosystem &middot; Dr. Nadeen Kabboura</footer>
</body>
</html>
"""


ALL = [ch1_mindset, ch2_anatomy, ch3_why, ch4_assessment, ch5_pyramid, ch6_home_care,
       ch7_topicals, ch8_injectables, ch9_energy, ch10_protocol, ch11_future]

# file, numeral, chapter, plate title, what the plate is saying, rendered plate
# (the painterly 1600x900 render, where one exists yet - None means the vector
# plate is carrying the chapter on its own for now)
SERIES = [
    ("01-the-mindset.svg", "I", "The Mindset", "The band of normal",
     "Seven forms differing in length, width, symmetry and tone - every one of them "
     "inside a single unbroken span. There is no cut-off to draw.",
     "renders/01-the-mindset.webp"),
    ("02-normal-anatomy.svg", "II", "Normal Anatomy", "The layered field",
     "Microbiome above the surface; keratinised epithelium thinning into mucosa; the "
     "basement membrane in gold with melanocytes ranged along it; collagen, elastin, "
     "fibroblasts, vessels, nerves and fat beneath.",
     "renders/02-normal-anatomy.webp"),
    ("03-why-patients-come.svg", "III", "Why Patients Come", "Three domains, one journey",
     "Physical, functional and psychological concern overlapping on one luminous "
     "centre, with the journey from silent concern to restoration opening beside them.",
     None),
    ("04-clinical-assessment.svg", "IV", "Clinical Assessment", "What the eye has to separate",
     "One field read three ways - diffuse pigment, a sclerotic band, a fixed irregular "
     "lesion - and the one that must never be missed ringed in gold.",
     "renders/04-clinical-assessment.webp"),
    ("05-treatment-pyramid.svg", "V", "The Treatment Pyramid", "Six tiers, climbed slowly",
     "Lifestyle, home care, topicals, injectables, energy, surgery. The ascent is "
     "dotted up the left; the apex is small because it is the exception.",
     None),
    ("06-home-care.svg", "VI", "Home Care", "The barrier, and the cycle it interrupts",
     "Intact lipid lamellae, and the loop friction starts - shear, inflammation, "
     "melanocyte activation, pigment - with the barrier stopping two of its arms.",
     "renders/06-home-care.webp"),
    ("07-topicals.svg", "VII", "Topicals", "The pathway, and the four places it can be held",
     "Tyrosine to melanosome to keratinocyte, with enzyme, signal, transfer and "
     "turnover marked as holds, over a gentle-to-never gradient.",
     "renders/07-topicals.webp"),
    ("08-regenerative-injectables.svg", "VIII", "Regenerative Injectables",
     "Depletion, activation, restoration",
     "A depleted grey matrix, the same field activating under a stimulus, and tissue "
     "restored - dense collagen, new microvessels, held water.",
     "renders/08-regenerative-injectables.webp"),
    ("09-energy-based-medicine.svg", "IX", "Energy-Based Medicine", "The depth map",
     "Fractional columns, superficial ablation and insulated needles in the same "
     "tissue - two of them lighting the epidermal melanin, one leaving it alone.",
     "renders/09-energy-based-medicine.webp"),
    ("10-the-kabboura-protocol.svg", "X", "The Kabboura Protocol", "Five streams, one tissue",
     "Barrier, structure, regeneration, pigment and maintenance entering in order and "
     "braiding into a single restored field. Structure before surface.",
     None),
    ("11-the-future.svg", "XI", "The Future", "Helix, lattice, light",
     "Genomics, machine-read data and regenerating tissue as one continuous movement.",
     None),
]


def gallery():
    """The series, displayed in chapter order."""
    plates = []
    for i, (f, num, chap, title, note, render) in enumerate(SERIES):
        load = "eager" if i < 2 else "lazy"
        shots = []
        if render:
            shots.append(f'''<div class="shot"><img src="{render}" alt="{title}" '''
                         f'''loading="{load}" width="1600" height="900"><span>Render</span></div>''')
        shots.append(f'''<div class="shot"><img src="{f}" alt="{title}" '''
                     f'''loading="{load}" width="1600" height="900">'''
                     f'''<span>Vector plate</span></div>''')
        plates.append(f'''    <figure class="plate" id="{num.lower()}">
      <div class="meta">
        <span class="num">{num}</span>
        <div>
          <h2>{chap}</h2>
          <p class="t">{title}</p>
        </div>
      </div>
      <div class="pair{'' if render else ' one'}">{"".join(shots)}</div>
      <figcaption>{note}</figcaption>
    </figure>''')
    nav = "".join(f'<a href="#{e[1].lower()}">{e[1]}</a>' for e in SERIES)
    have = sum(1 for e in SERIES if e[5])
    doc = (HTML.replace("{{NAV}}", nav)
               .replace("{{PLATES}}", "\n".join(plates))
               .replace("{{COUNT}}", f"{have} of {len(SERIES)} rendered"))
    (OUT / "index.html").write_text(doc)
    print(f"  {'index.html':32s} {len(doc)/1024:6.1f} kB  ({have} renders paired)")


if __name__ == "__main__":
    print("chapter illustrations")
    for fn in ALL:
        fn()
    gallery()
