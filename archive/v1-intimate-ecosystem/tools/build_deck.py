#!/usr/bin/env python3
"""Assemble the self-contained conference deck.

Inputs   tools/deck.css, tools/deck.js, deck/illustrations/*.svg,
         tools/fonts/embed.css (base64 woff2 - no network at the podium)
Outputs  deck/index.html, deck/references.html, deck/qr/*.svg

deck/index.html is GENERATED. Edit the content below, or the illustration
sources, and re-run this script - do not hand-edit the built file.
"""

import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
DECK = ROOT / "deck"
ILLU = DECK / "illustrations"

# --------------------------------------------------------------------------
# speaker identity and links - the two fields most likely to need changing
# --------------------------------------------------------------------------
SPEAKER = "Dr. Nadeen Kabboura"
CREDENTIALS = "Obstetrics &amp; Gynaecology · Aesthetic and Regenerative Medicine"
INSTAGRAM = "@drnadeenkabbouraofficial"
EMAIL = "nadeenkabboura@gmail.com"
VENUE = "Conference · Session · Date"

SITE = "https://rayan-debug.github.io/nadine-"
QR_REFERENCES = SITE + "/deck/references.html"
QR_RESOURCES = SITE + "/"

DECK_TITLE = "Tissue-Specific Intimate Medicine"


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def svg(name, hooks=None, fit="xMidYMid meet"):
    """Inline an illustration, stripping the fixed width/height so that CSS
    can size it, and injecting the per-slide build hooks."""
    s = (ILLU / name).read_text()
    s = re.sub(r'\s(width|height)="\d+"', "", s, count=2)
    s = s.replace("<svg ", f'<svg preserveAspectRatio="{fit}" ', 1)
    for old, new in (hooks or {}).items():
        if old not in s:
            raise SystemExit(f"{name}: hook not found -> {old}")
        s = s.replace(old, new)
    return s


def head(eyebrow, title, gold=False, rule=True):
    cls = ' class="h1-gold"' if gold else ""
    t = f"<h1{cls}>{title}</h1>" if title else ""
    r = '<div class="rule"></div>' if rule else ""
    return f'<header><p class="eyebrow">{eyebrow}</p>{t}{r}</header>'


def foot(ref, chip, n, limited=False):
    cls = "chip limited" if limited else "chip"
    c = f'<span class="{cls}">{chip}</span>' if chip else ""
    return (f'<footer><span class="ref">{ref}</span>{c}'
            f'<span class="pageno">{n:02d}</span></footer>')


def notes(*paragraphs):
    return '<div class="notes">' + "".join(f"<p>{p}</p>" for p in paragraphs) + "</div>"


# build hooks for the inflammation-pigment cycle: node n on click n,
# the arc that follows it on click n+1, the centre line last
CYCLE_HOOKS = {}
for _k in range(1, 7):
    CYCLE_HOOKS[f'<g class="node node-{_k}">'] = \
        f'<g class="node node-{_k} step" data-step="{_k}">'
    CYCLE_HOOKS[f'class="gold-t arc arc-{_k}"'] = \
        f'class="gold-t arc arc-{_k} step" data-step="{_k + 1}"'
for _y in (452, 518):
    CYCLE_HOOKS[f'<text class="ser" x="740" y="{_y}"'] = \
        f'<text class="ser step" data-step="7" x="740" y="{_y}"'


# --------------------------------------------------------------------------
# the fourteen slides
# --------------------------------------------------------------------------
def slides():
    S = []

    # 01 -------------------------------------------------------------- TITLE
    S.append(("Title", f"""
<section class="slide title-slide" data-title="Title">
  <div class="plate">{svg("00-title-contour.svg", fit="none")}</div>
  <div class="inner">
    <p class="eyebrow kicker">Functional · Aesthetic · Regenerative Gynaecology</p>
    <h1>Tissue-Specific<br>Intimate Medicine</h1>
    <p class="sub">Indication-driven. Biologically rational.</p>
    <div class="who">
      <div class="name">{SPEAKER}</div>
      <div class="cred">{CREDENTIALS}</div>
    </div>
  </div>
  <div class="venue micro">{VENUE}</div>
  {notes(
    "Open on the single claim the whole lecture defends: <b>intimate treatment must be "
    "tissue-specific, indication-driven and biologically rational — not product- or "
    "device-driven.</b>",
    "Fourteen slides, ten minutes of core material. Signpost the five movements: premise "
    "and anatomy, pigment and inflammation, energy and hierarchy, regeneration and "
    "evidence, framework and conclusion.",
    "Timing: 20 seconds. Do not read the title.")}
</section>"""))

    # 02 ----------------------------------------------------- CLINICAL PREMISE
    S.append(("Clinical premise", f"""
<section class="slide premise" data-title="Clinical premise">
  {head("The clinical premise", "", rule=False)}
  <main>
    <p class="hero">Variation is not pathology.</p>
    <p class="lead">Treat indication — not expectation.</p>
    <figure class="step" data-step="1">{svg("01-variation-spectrum.svg")}</figure>
  </main>
  {foot("Lloyd et al. <i>BJOG</i> 2005;112:643–6 · ACOG Committee Opinion 795, 2020",
        "Established evidence", 2)}
  {notes(
    "Labial dimensions in unselected women span a wide range — Lloyd's series recorded "
    "labia minora width from a few millimetres to roughly five centimetres, with marked "
    "asymmetry common and unrelated to symptoms.",
    "The clinical consequence: an appearance outside a patient's expectation is not, by "
    "itself, an indication. ACOG Committee Opinion 795 is explicit that counselling on "
    "normal variation precedes any discussion of intervention.",
    "Say plainly: <b>we treat symptoms, function and disease. We do not treat a "
    "photograph.</b> Timing: 45 seconds.")}
</section>"""))

    # 03 --------------------------------------------------- TISSUE-SPECIFIC ANATOMY
    S.append(("Tissue-specific anatomy", f"""
<section class="slide" data-title="Tissue-specific anatomy">
  {head("Tissue-specific anatomy", "One region. Distinct tissue biology.")}
  <main>
    <div class="split">
      <div class="fig">{svg("02-hart-line-anatomy.svg", {
                            '<g class="hart">': '<g class="hart" data-step="1">'})}</div>
      <ul class="side">
        <li class="step" data-step="1">Keratinised skin <b>laterally</b></li>
        <li class="step" data-step="1">Non-keratinised mucosa <b>medially</b></li>
        <li class="step" data-step="1"><b>Hart’s line</b> is the boundary</li>
      </ul>
    </div>
  </main>
  {foot("Yeung &amp; Pauls, <i>Obstet Gynecol Clin North Am</i> 2016;43:27–44",
        "Established evidence", 3)}
  {notes(
    "Click once: Hart’s line traces in gold. Let it draw before speaking over it.",
    "Hart’s line runs along the medial aspect of the labia minora and marks the boundary "
    "between keratinised, ectodermally derived skin and the non-keratinised vestibular "
    "mucosa of urogenital-sinus origin. It is the most clinically useful landmark on the "
    "vulva and it is almost never drawn on an aesthetic consent form.",
    "Everything that follows — what you can apply, what you can inject, what energy you "
    "can deliver — changes when you cross that line. <b>Name the tissue before you name "
    "the treatment.</b> Timing: 50 seconds.")}
</section>"""))

    # 04 ------------------------------------------------ CUTANEOUS-MUCOSAL INTERFACE
    S.append(("Cutaneous–mucosal interface", f"""
<section class="slide" data-title="Cutaneous–mucosal interface">
  {head("The cutaneous–mucosal interface", "Mucosa ≠ facial skin", gold=True)}
  <main>
    <div class="stack">
      <figure class="fig">{svg("03-cutaneous-mucosal.svg")}</figure>
      <p class="note step" data-step="1">No stratum corneum · no adnexa · percutaneous
        absorption several-fold higher than forearm</p>
    </div>
  </main>
  {foot("Oriba, Bucks &amp; Maibach, <i>Br J Dermatol</i> 1996;134:229–33 · "
        "Farage &amp; Maibach, <i>Arch Gynecol Obstet</i> 2006;273:195–202",
        "Established evidence", 4)}
  {notes(
    "Left: labia majora — thick stratum corneum, deep rete ridges, follicles, sebaceous "
    "and apocrine glands, a competent barrier. Right: vestibule — non-keratinised, "
    "glycogen-rich, no corneum, no adnexa, superficial capillary loops.",
    "Oriba and Maibach measured percutaneous absorption of hydrocortisone and testosterone "
    "across vulvar versus forearm skin and found it substantially higher at the vulva. The "
    "practical reading: <b>a concentration that is well tolerated on the face is not the "
    "same exposure here</b>, and the absence of adnexa removes the reservoir and the "
    "re-epithelialisation source that facial resurfacing relies on.",
    "This is why facial protocols transplanted unchanged are the commonest source of "
    "iatrogenic injury in this field. Timing: 60 seconds.")}
</section>"""))

    # 05 ----------------------------------------------- INFLAMMATION-PIGMENT CYCLE
    S.append(("Inflammation–pigment cycle", f"""
<section class="slide" data-title="Inflammation–pigment cycle">
  {head("Mechanism", "The inflammation–pigment cycle", rule=False)}
  <main>
    <div class="split">
      <div class="fig">{svg("04-inflammation-pigment-cycle.svg", CYCLE_HOOKS)}</div>
      <div class="side">
        <p class="lead step" data-step="7">Escalation feeds<br>the cycle.</p>
        <p class="term step" data-step="7">Correct the driver first. Pigment is
          the readout, not the disease.</p>
      </div>
    </div>
  </main>
  {foot("Davis &amp; Callender, <i>J Clin Aesthet Dermatol</i> 2010;3(7):20–31",
        "Mechanism established · site extrapolated", 5)}
  {notes(
    "Build it one click at a time; seven clicks in total. Do not rush — this is the slide "
    "the room should remember.",
    "Friction and occlusion disrupt an already thin barrier. Barrier disruption drives "
    "low-grade inflammation. Inflammatory mediators — prostaglandins, leukotrienes, "
    "endothelin-1, stem cell factor — upregulate melanocyte activity. Melanin is "
    "transferred and, where the basement membrane is breached, dropped into the dermis. "
    "The visible result is post-inflammatory hyperpigmentation.",
    "The sixth node is the one we contribute: aggressive treatment aimed at the pigment "
    "re-injures the barrier and re-enters the loop at step two. <b>Every escalation taken "
    "against an inflamed field buys a darker result.</b>",
    "Timing: 90 seconds — the longest single slide.")}
</section>"""))

    # 06 ------------------------------------------------------ ASSESS BEFORE TREAT
    S.append(("Assess before treatment", f"""
<section class="slide" data-title="Assess before treatment">
  {head("Assessment", "Assess before you treat")}
  <main>
    <div class="tree">
      <p class="q">Is pathology present?</p>
      <div class="fork"><svg viewBox="0 0 1000 62" preserveAspectRatio="none">
        <path d="M 500 0 L 500 20 M 236 20 L 764 20 M 236 20 L 236 50 M 764 20 L 764 50"
              fill="none" stroke="#C6A24E" stroke-width="2" vector-effect="non-scaling-stroke"/>
        <path d="M 228 42 L 236 58 L 244 42 M 756 42 L 764 58 L 772 42"
              fill="none" stroke="#C6A24E" stroke-width="2" vector-effect="non-scaling-stroke"/>
      </svg></div>
      <div class="branches">
        <div class="branch alert step" data-step="1">
          <h3>Yes</h3>
          <p class="head">Biopsy or treat the disease</p>
          <ul>
            <li>Lichen sclerosus</li>
            <li>Differentiated VIN</li>
            <li>Vulvar melanoma</li>
            <li>Infection or dermatosis</li>
          </ul>
        </div>
        <div class="branch step" data-step="2">
          <h3>No</h3>
          <p class="head">Identify the driver</p>
          <ul>
            <li>Physiological variation</li>
            <li>Friction or mechanical trauma</li>
            <li>Post-inflammatory pigment</li>
            <li>Hormonal influence</li>
            <li>Previous procedural injury</li>
          </ul>
        </div>
      </div>
    </div>
  </main>
  {foot("Lewis et al. BAD guidelines, <i>Br J Dermatol</i> 2018;178:839–53",
        "Expert clinical framework", 6)}
  {notes(
    "Two clicks. The left arm first, deliberately — it is the arm that ends careers.",
    "Any fixed, indurated, ulcerated, eroded or changing lesion is biopsied before a single "
    "aesthetic intervention. ABCDE criteria perform poorly on mucosal melanoma; a benign "
    "clinical impression is not a substitute for histology. Lichen sclerosus and "
    "differentiated VIN both carry malignant potential and both are routinely mistaken for "
    "pigmentary or textural complaints.",
    "The right arm is where most consultations actually sit — and even there, naming the "
    "driver comes before choosing a modality. <b>If you cannot name the driver, you are not "
    "ready to treat.</b> Timing: 60 seconds.")}
</section>"""))

    # 07 ------------------------------------------------ MECHANISM-BASED PIGMENT
    chain = [
        ("Trigger", ""),
        ("Inflammatory<br>signalling", "Tranexamic acid"),
        ("Melanocyte<br>activation", ""),
        ("Tyrosinase<br>activity", "Azelaic acid|Hydroquinone*"),
        ("Melanin<br>synthesis", ""),
        ("Melanosome<br>transfer", "Niacinamide|Retinoids"),
        ("Visible<br>pigmentation", ""),
    ]
    nodes = "".join(f'<div class="node"><span class="dot"></span>'
                    f'<span class="nm">{n}</span></div>' for n, _ in chain)
    agents = ""
    for k, (_, a) in enumerate(chain):
        inner = ""
        if a:
            inner = '<span class="tick"></span>' + "".join(
                f'<span class="agent">{x}</span>' for x in a.split("|"))
        agents += f'<div class="slot step" data-step="1">{inner}</div>'
    S.append(("Mechanism-based pigment management", f"""
<section class="slide" data-title="Mechanism-based pigment management">
  {head("Pigment", "Target the mechanism, not the shade")}
  <main>
    <div class="pathway">
      <div class="chain">{nodes}</div>
      <div class="rail"><svg viewBox="0 0 1664 22" preserveAspectRatio="none"><path d="M 0 11 L 1664 11" stroke="#E4D5AC" stroke-width="1" vector-effect="non-scaling-stroke"/><path d="M 230 4 L 244 11 L 230 18" fill="none" stroke="#C6A24E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M 467 4 L 481 11 L 467 18" fill="none" stroke="#C6A24E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M 705 4 L 719 11 L 705 18" fill="none" stroke="#C6A24E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M 943 4 L 957 11 L 943 18" fill="none" stroke="#C6A24E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M 1180 4 L 1194 11 L 1180 18" fill="none" stroke="#C6A24E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M 1418 4 L 1432 11 L 1418 18" fill="none" stroke="#C6A24E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      <div class="agents">{agents}</div>
      <p class="note step" data-step="1" style="margin-top:56px">
        Dermatological evidence is established · vulvar application is
        anatomical extrapolation
      </p>
      <p class="note" style="margin-top:14px;font-size:27px">
        * prescription-only in several jurisdictions · exogenous ochronosis risk
      </p>
    </div>
  </main>
  {foot("Bala et al. <i>Dermatol Surg</i> 2018;44:814–25 · "
        "Hakozaki et al. <i>Br J Dermatol</i> 2002;147:20–31",
        "Extrapolated evidence", 7)}
  {notes(
    "One click reveals where each agent class acts. The point of the slide is that a "
    "clinician who knows the pathway can reason about any product, including the ones "
    "that do not exist yet.",
    "Tranexamic acid acts upstream, on plasmin-mediated inflammatory signalling — which is "
    "why it outperforms pure tyrosinase inhibitors where inflammation is the driver. "
    "Azelaic acid and hydroquinone inhibit tyrosinase, the rate-limiting enzyme. "
    "Niacinamide reduces melanosome transfer to keratinocytes; retinoids act on transfer "
    "and on epidermal turnover.",
    "Be explicit about the evidence class: these data come from facial melasma and "
    "post-inflammatory hyperpigmentation trials. <b>Vulvar use is extrapolation by "
    "mechanism, not by trial</b> — and on non-keratinised mucosa the irritant potential of "
    "retinoids and acids is higher. Timing: 60 seconds.")}
</section>"""))

    # 08 ------------------------------------------------------ ENERGY-TISSUE
    S.append(("Energy–tissue interaction", f"""
<section class="slide" data-title="Energy–tissue interaction">
  {head("Energy", "Select energy by tissue target")}
  <main>
    <div class="stack">
      <figure class="fig">{svg("05-energy-depth-map.svg", {
          f'<g class="zone zone-{c}">': f'<g class="zone zone-{c} step" data-step="{k}">'
          for k, c in enumerate("abc", 1)})}</figure>
      <p class="note step" data-step="3">Melanin is a competing chromophore —
        optical risk rises steeply in Fitzpatrick IV–VI</p>
    </div>
  </main>
  {foot("FDA Safety Communication, 30 July 2018 · Li et al. <i>JAMA</i> 2021;326:1381–9",
        "Evidence remains limited", 8, limited=True)}
  {notes(
    "Three clicks, one modality class at a time. Deliberately no devices, no brands — the "
    "variable that matters is depth and chromophore, not the badge on the handpiece.",
    "Optical energy deposits superficially and is absorbed by melanin as well as by water; "
    "in richly pigmented skin the epidermis competes for the energy you intended for the "
    "dermis. Fractional delivery spares intervening tissue and relies on those islands for "
    "repair. Volumetric radiofrequency heats resistively, has no chromophore dependence, "
    "and can reach dermis and submucosa while the epidermis is comparatively spared.",
    "Hold the evidence honestly: the FDA's 2018 communication warned against energy devices "
    "marketed for vaginal ‘rejuvenation’, and Li's sham-controlled trial found "
    "<b>fractional CO₂ no better than sham</b> for postmenopausal vaginal symptoms at 12 "
    "months. Local oestrogen remains better evidenced for genitourinary syndrome of "
    "menopause. Timing: 60 seconds.")}
</section>"""))

    # 09 --------------------------------------------------- THERAPEUTIC HIERARCHY
    tiers = [
        ("Foundation", "Barrier · inflammation · friction"),
        ("Correction", "Pigment · texture · hair"),
        ("Structure", "Volume · laxity · scars"),
        ("Regeneration", "Tissue quality · biostimulation"),
        ("Maintenance", "Prevention · reassessment"),
    ]
    base, apex, n = 1250, 470, 5
    tones = ["#F3EBDC", "#EFE6D4", "#EADFC8", "#E4D7BA", "#DCCBAD"]
    pyr = ""
    # drawn apex-first (maintenance) down to the base (foundation); the build
    # runs the other way, from the foundation upward
    for k, (nm, sb) in enumerate(reversed(tiers)):
        wt = apex + k * (base - apex) / n
        wb = apex + (k + 1) * (base - apex) / n
        l, r = (wb - wt) / 2 / wb * 100, (wb + wt) / 2 / wb * 100
        pyr += (f'<div class="tier step" data-step="{k+1}" style="width:{wb:.0f}px">'
                f'<div class="bg" style="background:{tones[k]};'
                f'clip-path:polygon({l:.2f}% 0,{r:.2f}% 0,100% 100%,0 100%)"></div>'
                f'<span class="nm">{nm}</span><span class="sb">{sb}</span></div>')
    S.append(("Therapeutic hierarchy", f"""
<section class="slide" data-title="Therapeutic hierarchy">
  {head("Sequence", "Therapeutic hierarchy")}
  <main>
    <div class="stack">
      <div class="pyramid">{pyr}</div>
      <p class="lead step" data-step="6" style="font-size:52px;margin-top:22px">
        An inflamed foundation cannot support escalation.</p>
    </div>
  </main>
  {foot("", "Expert clinical framework", 9)}
  {notes(
    "Six clicks, building from the base upward — the order of the build is the argument.",
    "Foundation is barrier repair, inflammation control and friction elimination: bland "
    "emollients, pH-appropriate cleansing, breathable fabrics, reconsidered hair removal. "
    "Correction addresses surface — pigment, texture, hair. Structure addresses volume, "
    "laxity and scar. Regeneration addresses tissue quality. Maintenance is prevention and "
    "scheduled reassessment, not a repeat sale.",
    "The rule that governs the whole pyramid: <b>you may not skip a tier because a patient "
    "has asked for a higher one.</b> An inflamed, friction-driven field treated with energy "
    "or injectables returns darker, not lighter. Timing: 50 seconds.")}
</section>"""))

    # 10 ------------------------------------------------------ REGENERATIVE BIOLOGY
    steps_ = ["Stimulus", "Cellular signalling", "Fibroblast activity",
              "Extracellular-matrix remodelling", "Collagen and elastin synthesis",
              "Improved tissue quality"]
    casc = "".join(f'<div class="cell step" data-step="1">{s}</div>' for s in steps_)
    cats = [("Autologous", "Platelet concentrates (PRP / PRF)"),
            ("Nucleotide", "Polynucleotides (PN / PDRN)"),
            ("Scaffold", "Hyaluronic-acid biostimulation"),
            ("Stimulator", "Collagen-stimulating injectables")]
    catrow = "".join(f'<div class="cat step" data-step="2">'
                    f'<b>{a}</b><span>{b}</span></div>' for a, b in cats)
    S.append(("Regenerative biology", f"""
<section class="slide" data-title="Regenerative biology">
  {head("Tissue regeneration · biostimulation · ECM remodelling",
        "The cascade, not the product")}
  <main>
    <div class="stack" style="gap:44px">
      <div class="cascade">{casc}</div>
      <div class="categories">{catrow}</div>
      <p class="lead step" data-step="3" style="font-size:46px">
        Evidence varies by indication and anatomical site.</p>
    </div>
  </main>
  {foot("Squadrito et al. <i>Front Pharmacol</i> 2017;8:224", "Emerging evidence", 10)}
  {notes(
    "Three clicks: the cascade, then the therapeutic categories, then the caveat.",
    "Every regenerative approach in this field claims the same pathway: a stimulus produces "
    "cellular signalling, fibroblasts are recruited and activated, the extracellular matrix "
    "is remodelled, collagen and elastin are synthesised, and tissue quality improves. "
    "Polydeoxyribonucleotide acts partly through adenosine A2A receptor agonism with "
    "anti-inflammatory and pro-angiogenic effects; platelet concentrates deliver autologous "
    "growth factors; hyaluronic-acid and collagen-stimulating injectables act as scaffold "
    "and stimulus.",
    "Present these as <b>categories with proposed mechanisms, not as products</b>. The "
    "cascade is plausible and partly demonstrated in vitro and at other sites; the "
    "site-specific clinical evidence at the vulva is thin and heterogeneous, and one "
    "indication does not license another. Timing: 60 seconds.")}
</section>"""))

    # 11 ------------------------------------------------------ EMERGING THERAPIES
    marks = [(12, "up", "Autologous platelet<br>concentrates (PRP)"),
             (32, "dn", "Polynucleotides<br>(PN / PDRN)"),
             (51, "up", "Collagen-stimulating<br>injectables"),
             (70, "dn", "Extracellular vesicles<br>/ exosomes"),
             (87, "up", "NAD⁺-related<br>interventions")]
    mk = "".join(
        f'<div class="mk {cls} step" data-step="{k+1}" style="left:{x}%">'
        + ('<div class="t">' + t + '</div><div class="stem"></div><div class="pin"></div>'
           if cls == "up" else
           '<div class="pin"></div><div class="stem"></div><div class="t">' + t + "</div>")
        + "</div>"
        for k, (x, cls, t) in enumerate(marks))
    S.append(("Emerging therapies", f"""
<section class="slide" data-title="Emerging therapies">
  {head("Evidence", "Where the evidence actually sits")}
  <main>
    <div class="stack">
      <div class="spectrum">
        <div class="axis"></div>
        <span class="cap l">More established</span>
        <span class="cap r">More experimental</span>
        {mk}
      </div>
      <p class="lead step" data-step="6" style="font-size:50px">
        Biological rationale does not equal clinical validation.</p>
    </div>
  </main>
  {foot("Goldstein et al. <i>J Am Acad Dermatol</i> 2019;80:1788–9 · "
        "FDA Public Safety Notification on exosome products, 2019",
        "Emerging · experimental", 11, limited=True)}
  {notes(
    "Five clicks place the categories, the sixth delivers the line. Resist the urge to "
    "move anything leftward for the room’s comfort.",
    "Autologous platelet concentrates have the largest genital literature and it is still "
    "small — Goldstein’s randomised, double-blind trial in vulvar lichen sclerosus "
    "found no significant benefit over placebo, which is exactly the kind of result that "
    "should temper enthusiasm. Polynucleotides have a coherent mechanism and mostly "
    "uncontrolled genital data. Collagen-stimulating injectables are extrapolated from "
    "facial and body use, and carry nodule risk if placed in the wrong plane.",
    "Extracellular vesicles and NAD⁺-related interventions are, at this site, "
    "<b>pre-clinical rationale with active marketing</b>. There is no FDA-approved exosome "
    "product and standing safety notifications exist. Naming that from the podium is part "
    "of the job. Timing: 70 seconds.")}
</section>"""))

    # 12 --------------------------------------------------------- THE FRAMEWORK
    fw = svg("06-kabboura-framework.svg", {
        f'<g class="fw fw-{k}">': f'<g class="fw fw-{k} step" data-step="{k}">'
        for k in range(1, 7)})
    S.append(("The Kabboura Clinical Framework", f"""
<section class="slide" data-title="The Kabboura Clinical Framework">
  {head("Expert clinical framework — not a validated guideline",
        "The Kabboura Clinical Framework")}
  <main>
    <div class="split">
      <div class="fig">{fw}</div>
      <div class="side" style="flex:0 0 620px">
        <p class="lead step" data-step="6">Escalate only from<br>a quiet foundation.</p>
        <p class="term step" data-step="6">Stage-gated and indication-led.
          Each stage is re-assessed before the next is entered.</p>
        <p class="term step" data-step="6" style="color:#7C7365;font-size:32px">
          An organising heuristic — not a validated protocol.</p>
      </div>
    </div>
  </main>
  {foot("", "Expert clinical framework", 12)}
  {notes(
    "Six clicks, one stage each. Let RESTORE, REBUILD, REGENERATE and REFINE carry the "
    "visual weight — those four words are the deck’s takeaway.",
    "Assess: tissue, pathology, indication. Restore: barrier and inflammation — nothing "
    "above this stage is attempted until the field is quiet. Rebuild: structure and "
    "function. Regenerate: tissue quality through biostimulation and extracellular-matrix "
    "remodelling. Refine: pigment and texture, deliberately last, because pigment is the "
    "readout of everything beneath it. Maintain: reassessment and prevention.",
    "State the epistemic status out loud: <b>this is an expert clinical framework, offered "
    "as an organising heuristic. It is not a guideline and it has not been validated "
    "prospectively.</b> Timing: 60 seconds.")}
</section>"""))

    # 13 ----------------------------------------------------------- TAKE-HOME
    th = [("Diagnose before treating"), ("Match treatment to tissue"),
          ("Escalate according to evidence")]
    rows = "".join(f'<div class="row step" data-step="{k+1}">'
                   f'<span class="n">{k+1:02d}</span><span class="t">{t}</span></div>'
                   for k, t in enumerate(th))
    S.append(("Clinical take-home", f"""
<section class="slide" data-title="Clinical take-home">
  {head("Conclusion", "Clinical take-home")}
  <main>
    <div class="stack" style="justify-content:center">
      <div class="takehome">{rows}</div>
      <p class="lead step" data-step="4" style="font-size:72px;margin-top:22px">
        Treat biology — not trends.</p>
    </div>
  </main>
  {foot("", "", 13)}
  {notes(
    "Four clicks. Say each line once and stop — do not gloss them.",
    "Diagnose before treating: the biopsy threshold is low and the cost of missing "
    "differentiated VIN or mucosal melanoma is absolute. Match treatment to tissue: Hart’s "
    "line changes what is safe on either side of it. Escalate according to evidence: name "
    "the evidence class — established, extrapolated, emerging, or expert framework — "
    "every time you offer something.",
    "Close on the final line and let it sit. Timing: 40 seconds.")}
</section>"""))

    # 14 ------------------------------------------------------------- CLOSING
    S.append(("Closing", f"""
<section class="slide closing" data-title="Closing">
  {head("Thank you", "", rule=False)}
  <main>
    <p class="name">{SPEAKER}</p>
    <p class="cred">{CREDENTIALS}</p>
    <p class="handles">{INSTAGRAM} · {EMAIL}</p>
    <div class="qrs">
      <div class="qr">{(DECK / "qr" / "references.svg").read_text()}
        <div class="cap">Full bibliography</div>
        <div class="url">{QR_REFERENCES.replace("https://", "")}</div></div>
      <div class="qr">{(DECK / "qr" / "resources.svg").read_text()}
        <div class="cap">Lecture resources</div>
        <div class="url">{QR_RESOURCES.replace("https://", "")}</div></div>
    </div>
  </main>
  {foot("", "", 14)}
  {notes(
    "Leave this slide up through questions. The left code opens the full reference list "
    "for every claim made in the lecture; the right opens the longer teaching resource.",
    "If time has run short, the three slides worth returning to in discussion are Hart’s "
    "line, the inflammation–pigment cycle and the evidence spectrum.")}
</section>"""))

    return S


# --------------------------------------------------------------------------
# references
# --------------------------------------------------------------------------
REFERENCES = [
    ("Anatomy and normal variation", [
        "Lloyd J, Crouch NS, Minto CL, Liao LM, Creighton SM. Female genital appearance: "
        "‘normality’ unfolds. <i>BJOG</i>. 2005;112(5):643–646.",
        "American College of Obstetricians and Gynecologists. Elective Female Genital "
        "Cosmetic Surgery. ACOG Committee Opinion No. 795. <i>Obstet Gynecol</i>. "
        "2020;135(1):e36–e42.",
        "Yeung J, Pauls RN. Anatomy of the vulva and the female sexual response. "
        "<i>Obstet Gynecol Clin North Am</i>. 2016;43(1):27–44.",
        "Farage M, Maibach H. Lifetime changes in the vulva and vagina. "
        "<i>Arch Gynecol Obstet</i>. 2006;273(4):195–202.",
    ]),
    ("Barrier, permeability and the mucosal interface", [
        "Oriba HA, Bucks DAW, Maibach HI. Percutaneous absorption of hydrocortisone and "
        "testosterone on the vulva and forearm: effect of the menopause and site. "
        "<i>Br J Dermatol</i>. 1996;134(2):229–233.",
        "Britz MB, Maibach HI. Human labia majora skin: transepidermal water loss in vivo. "
        "<i>Acta Derm Venereol Suppl (Stockh)</i>. 1979;59(85):23–25.",
        "Farage MA, Maibach HI. Tissue structure and physiology of the vulva. In: "
        "<i>The Vulva: Physiology and Clinical Management</i>. 2nd ed. CRC Press; 2017.",
    ]),
    ("Pigmentation: mechanism and management", [
        "Davis EC, Callender VD. Postinflammatory hyperpigmentation: a review of the "
        "epidemiology, clinical features, and treatment options in skin of color. "
        "<i>J Clin Aesthet Dermatol</i>. 2010;3(7):20–31.",
        "Bala HR, Lee S, Wong C, Pandya AG, Rodrigues M. Oral tranexamic acid for the "
        "treatment of melasma: a review. <i>Dermatol Surg</i>. 2018;44(6):814–825.",
        "Hakozaki T, Minwalla L, Zhuang J, et al. The effect of niacinamide on reducing "
        "cutaneous pigmentation and suppression of melanosome transfer. "
        "<i>Br J Dermatol</i>. 2002;147(1):20–31.",
        "Fitton A, Goa KL. Azelaic acid: a review of its pharmacological properties and "
        "therapeutic efficacy. <i>Drugs</i>. 1991;41(5):780–798.",
    ]),
    ("Vulvar dermatoses and the biopsy threshold", [
        "Lewis FM, Tatnall FM, Velangi SS, et al. British Association of Dermatologists "
        "guidelines for the management of lichen sclerosus, 2018. "
        "<i>Br J Dermatol</i>. 2018;178(4):839–853.",
        "Bigby SM, Eva LJ, Fong KL, Jones RW. The natural history of vulvar intraepithelial "
        "neoplasia, differentiated type. <i>Int J Gynecol Pathol</i>. 2016;35(6):574–584.",
        "Wohlmuth C, Wohlmuth-Wieser I. Vulvar melanoma: molecular characteristics, "
        "diagnosis, surgical management, and medical treatment. "
        "<i>Am J Clin Dermatol</i>. 2021;22(5):639–651.",
    ]),
    ("Energy-based devices", [
        "US Food and Drug Administration. FDA warns against use of energy-based devices to "
        "perform vaginal ‘rejuvenation’ or vaginal cosmetic procedures. Safety "
        "Communication, 30 July 2018.",
        "Li FG, Maheux-Lacroix S, Deans R, et al. Effect of fractional carbon dioxide laser "
        "vs sham treatment on symptom severity in women with postmenopausal vaginal "
        "symptoms: a randomized clinical trial. <i>JAMA</i>. 2021;326(14):1381–1389.",
        "Mension E, Alonso I, Anglès-Acedo S, et al. Effect of fractional carbon dioxide "
        "vs sham laser on sexual function in survivors of breast cancer receiving aromatase "
        "inhibitors for genitourinary syndrome of menopause: the LIGHT randomized clinical "
        "trial. <i>JAMA Netw Open</i>. 2023;6(2):e2255697.",
    ]),
    ("Regenerative and emerging approaches", [
        "Squadrito F, Bitto A, Irrera N, et al. Pharmacological activity and clinical use of "
        "PDRN. <i>Front Pharmacol</i>. 2017;8:224.",
        "Goldstein AT, Mitchell L, Govind V, Heller D. A randomized double-blind "
        "placebo-controlled trial of autologous platelet-rich plasma intradermal injections "
        "for the treatment of vulvar lichen sclerosus. "
        "<i>J Am Acad Dermatol</i>. 2019;80(6):1788–1789.",
        "Behnia-Willison F, Pour NR, Mohamadi B, et al. Use of platelet-rich plasma for "
        "vulvovaginal autoimmune conditions like lichen sclerosus. "
        "<i>Plast Reconstr Surg Glob Open</i>. 2016;4(11):e1124.",
        "US Food and Drug Administration. Public safety notification on exosome products. "
        "December 2019.",
        "Covarrubias AJ, Perrone R, Grozio A, Verdin E. NAD⁺ metabolism and its roles in "
        "cellular processes during ageing. "
        "<i>Nat Rev Mol Cell Biol</i>. 2021;22(2):119–141.",
    ]),
]


def build_references():
    secs = ""
    for title, items in REFERENCES:
        lis = "".join(f"<li>{x}</li>" for x in items)
        secs += f"<section><h2>{title}</h2><ol>{lis}</ol></section>"
    css = """
    :root{--paper:#FBF7EE;--ink:#2E2B26;--muted:#7C7365;--gold:#C6A24E;--gold-deep:#8A6A1C;--line:#E4D5AC}
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:var(--paper);color:var(--ink);font-family:'Montserrat',Helvetica,Arial,sans-serif;
         font-weight:300;line-height:1.6;padding:64px 24px 120px}
    .wrap{max-width:820px;margin:0 auto}
    .eyebrow{font-size:12px;font-weight:600;letter-spacing:.3em;text-transform:uppercase;color:var(--gold-deep)}
    h1{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;font-size:44px;line-height:1.1;margin:14px 0 6px}
    .sub{color:var(--muted);font-size:15px}
    .rule{width:72px;height:1px;background:var(--gold);margin:34px 0 10px}
    section{margin-top:44px}
    h2{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;font-size:26px;color:var(--gold-deep);
       border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:18px}
    ol{list-style:none;counter-reset:r}
    li{counter-increment:r;position:relative;padding:12px 0 12px 44px;font-size:15px;border-bottom:1px solid #EFE6D5}
    li::before{content:counter(r);position:absolute;left:0;top:12px;font-family:'Cormorant Garamond',Georgia,serif;
       color:var(--gold);font-size:19px}
    li i{font-style:italic;color:#5C5548}
    footer{margin-top:56px;font-size:13px;color:var(--muted)}
    @media(max-width:600px){h1{font-size:34px}body{padding:40px 18px 80px}}
    """
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>References — {DECK_TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Montserrat:wght@300;600&display=swap" rel="stylesheet">
<style>{css}</style></head>
<body><div class="wrap">
<p class="eyebrow">Functional · Aesthetic · Regenerative Gynaecology</p>
<h1>{DECK_TITLE}</h1>
<p class="sub">Full reference list · {SPEAKER}</p>
<div class="rule"></div>
<p class="sub">Evidence classes are stated on each slide as established, extrapolated,
emerging, or expert clinical framework. Where a claim rests on extrapolation from
another anatomical site, the slide says so.</p>
{secs}
<footer>{SPEAKER} · {INSTAGRAM} · {EMAIL}</footer>
</div></body></html>
"""
    (DECK / "references.html").write_text(doc)
    print(f"  references.html   {len(doc)/1024:.1f} kB")


# --------------------------------------------------------------------------
# assembly
# --------------------------------------------------------------------------
def build_deck():
    fonts = (TOOLS / "fonts" / "embed.css").read_text()
    css = (TOOLS / "deck.css").read_text()
    js = (TOOLS / "deck.js").read_text()
    S = slides()
    body = "".join(h for _, h in S)
    idx = "".join(f'<li data-go="{k}"><span>{k+1:02d}</span>{html.escape(t)}</li>'
                  for k, (t, _) in enumerate(S))
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{DECK_TITLE} — {SPEAKER}</title>
<meta name="description" content="Conference lecture on tissue-specific, indication-driven
functional, aesthetic and regenerative gynaecology.">
<style>{fonts}</style>
<style>{css}
.notes{{display:none}}
.h1-gold{{color:var(--gold-deep)}}
</style></head>
<body>
<div id="stage">{body}</div>
<div id="progress"></div>
<aside id="notes"><div class="hd"></div><div class="bd"></div></aside>
<div id="index"><h2>{DECK_TITLE}</h2><ol>{idx}</ol></div>
<div id="help">← → advance · N notes · O index · F fullscreen</div>
<script>{js}</script>
</body></html>
"""
    (DECK / "index.html").write_text(doc)
    print(f"  index.html        {len(doc)/1024:.1f} kB  ({len(S)} slides)")


if __name__ == "__main__":
    DECK.mkdir(exist_ok=True)
    print("deck ->", DECK)
    build_references()
    build_deck()
