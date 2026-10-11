#!/usr/bin/env python3
"""Deepavali ang bao sheets, v2 (revision b).

Three sizes (small / medium / large), a domed top, a plain flap with a gold
lotus and a gold edge rule, the design's own body pattern with a fine brocade
overlay, a bottom border band, and on the front a "Happy Deepavali" cartouche.

Outputs under OUT:
  mockups/<slug>.svg          presentation sheet: all sizes, front + back, detail callouts
  print/<slug>-<size>.svg     A4 landscape die-line, front + back at 1:1 mm
"""
import math
import os

OUT = "/home/user/suite/angbao/v2"
FONT = "Georgia, 'DejaVu Serif', 'Times New Roman', serif"
GAP = 20.0        # mm between front and back on print sheets
MOCK_S = 2.0      # mockup units per mm
ZOOM = 6.0        # callout zoom, units per mm
CREAM = "#F6EEDC"
BAND = 0.085      # bottom border height as a fraction of packet height

SIZES = {"small": (85.0, 125.0), "medium": (105.0, 165.0), "large": (115.0, 185.0)}
SIZE_NAMES = {"small": "Small Size", "medium": "Medium Size", "large": "Large Size"}


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{fill}"{extra}/>'


def circle(cx, cy, r, fill, extra=""):
    return f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" fill="{fill}"{extra}/>'


def line(x1, y1, x2, y2, stroke, sw):
    return (f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" '
            f'stroke="{stroke}" stroke-width="{fmt(sw)}"/>')


# ---------- motifs -------------------------------------------------------

def flower(cx, cy, r, petal, centre, rot=0):
    parts = []
    for k in range(6):
        a = rot + 60 * k
        parts.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy - r * 0.55)}" rx="{fmt(r * 0.28)}" '
                     f'ry="{fmt(r * 0.55)}" fill="{petal}" transform="rotate({fmt(a)} {fmt(cx)} {fmt(cy)})"/>')
    parts.append(circle(cx, cy, r * 0.26, centre))
    return "".join(parts)


def marigold(cx, cy, r, petal, centre):
    parts = [circle(cx + r * 0.6 * math.cos(math.radians(a)),
                    cy + r * 0.6 * math.sin(math.radians(a)), r * 0.45, petal)
             for a in range(0, 360, 45)]
    parts.append(circle(cx, cy, r * 0.5, petal))
    parts.append(circle(cx, cy, r * 0.3, centre))
    return "".join(parts)


def arch(cx, cy, w, h, fill):
    r = w / 2
    top, bot = cy - h / 2, cy + h / 2
    d = (f"M{fmt(cx - r)},{fmt(bot)} V{fmt(top + r)} "
         f"A{fmt(r)},{fmt(r)} 0 0 1 {fmt(cx + r)},{fmt(top + r)} V{fmt(bot)} Z")
    return f'<path d="{d}" fill="{fill}"/>'


def kolam(cx, cy, s, col):
    """Four interlocking loops around a centre dot."""
    sw = fmt(s * 0.14)
    out = []
    for dx, dy, rx, ry in [(0, -0.9, 0.42, 0.8), (0, 0.9, 0.42, 0.8),
                           (-0.9, 0, 0.8, 0.42), (0.9, 0, 0.8, 0.42)]:
        out.append(f'<ellipse cx="{fmt(cx + dx * s)}" cy="{fmt(cy + dy * s)}" '
                   f'rx="{fmt(rx * s)}" ry="{fmt(ry * s)}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
    out.append(circle(cx, cy, s * 0.16, col))
    return "".join(out)


def butta(cx, cy, s, fill, core, rot=0):
    d = "M0,-1 C0.8,-0.5 0.7,0.6 0,1 C-0.7,0.6 -0.8,-0.5 0,-1 Z"
    return (f'<g transform="translate({fmt(cx)} {fmt(cy)}) rotate({fmt(rot)}) scale({fmt(s)})">'
            f'<path d="{d}" fill="{fill}"/>'
            f'<circle cx="0" cy="-0.05" r="0.28" fill="{core}"/></g>')


def elephant(cx, cy, s, body, accent, flip=1):
    """Caparisoned elephant facing right, drawn in unit space then scaled."""
    return (f'<g transform="translate({fmt(cx)} {fmt(cy)}) scale({fmt(s * flip)} {fmt(s)})">'
            f'<path d="M-0.9,-0.1 Q-1.2,0.05 -1.05,0.45" fill="none" stroke="{body}" '
            f'stroke-width="0.12" stroke-linecap="round"/>'
            f'<rect x="-0.8" y="0.2" width="0.28" height="0.62" rx="0.12" fill="{body}"/>'
            f'<rect x="-0.35" y="0.2" width="0.28" height="0.62" rx="0.12" fill="{body}"/>'
            f'<rect x="0.22" y="0.2" width="0.28" height="0.62" rx="0.12" fill="{body}"/>'
            f'<rect x="0.6" y="0.2" width="0.28" height="0.62" rx="0.12" fill="{body}"/>'
            f'<ellipse cx="0" cy="0" rx="0.95" ry="0.58" fill="{body}"/>'
            f'<rect x="-0.55" y="-0.8" width="0.95" height="0.34" rx="0.1" fill="{accent}"/>'
            f'<circle cx="0.85" cy="-0.38" r="0.42" fill="{body}"/>'
            f'<ellipse cx="0.5" cy="-0.34" rx="0.3" ry="0.4" fill="#000" opacity="0.15"/>'
            f'<path d="M1.2,-0.2 Q1.6,0.2 1.42,0.72" fill="none" stroke="{body}" '
            f'stroke-width="0.17" stroke-linecap="round"/>'
            '</g>')


def peacock(cx, cy, s, body, fan, eye, accent, flip=1):
    """Peacock with a fanned tail, facing right, drawn in unit space then scaled."""
    fans, eyes = [], []
    for a in (-60, -30, 0, 30, 60):
        rad = math.radians(a)
        fans.append(f'<ellipse cx="-0.4" cy="-0.75" rx="0.17" ry="0.85" fill="{fan}" '
                    f'transform="rotate({a} -0.4 0.1)"/>')
        eyes.append(circle(-0.4 + 1.6 * math.sin(rad), 0.1 - 1.6 * math.cos(rad), 0.13, eye))
    return (f'<g transform="translate({fmt(cx)} {fmt(cy)}) scale({fmt(s * flip)} {fmt(s)})">'
            + "".join(fans) + "".join(eyes) +
            f'<path d="M-0.1,0.33 L-0.16,0.72 M0.12,0.33 L0.14,0.72" stroke="{body}" '
            f'stroke-width="0.08" stroke-linecap="round"/>'
            f'<ellipse cx="0" cy="0" rx="0.5" ry="0.36" fill="{body}"/>'
            f'<path d="M0.3,-0.2 Q0.62,-0.5 0.62,-0.8" fill="none" stroke="{body}" '
            f'stroke-width="0.18" stroke-linecap="round"/>'
            f'<path d="M0.66,-1.0 L0.58,-1.3" stroke="{body}" stroke-width="0.07" stroke-linecap="round"/>'
            f'<circle cx="0.7" cy="-0.92" r="0.17" fill="{body}"/>'
            f'<path d="M0.84,-0.96 L1.0,-0.9 L0.84,-0.84 Z" fill="{accent}"/>'
            '</g>')


def lotus(cx, cy, r, gold, dark):
    """Gold lotus: five teardrop petals fanned from a base, with a base ellipse."""
    base = "M0,0 C0.42,-0.12 0.32,-0.78 0,-1 C-0.32,-0.78 -0.42,-0.12 0,0 Z"
    parts = [f'<g transform="translate({fmt(cx)} {fmt(cy)}) scale({fmt(r)})">']
    for ang, k in ((-70, 0.7), (70, 0.7), (-35, 0.9), (35, 0.9), (0, 1.0)):
        parts.append(f'<path d="{base}" fill="{gold}" stroke="{dark}" stroke-width="0.06" '
                     f'transform="rotate({ang}) scale({k})"/>')
    parts.append(f'<ellipse cx="0" cy="0.12" rx="0.55" ry="0.14" fill="{gold}"/>')
    parts.append('</g>')
    return "".join(parts)


# ---------- body patterns (own pattern per design, tiled over W x H) -----

def band_top(H):
    """Top edge of the bottom border band. Pattern rows are aligned to it."""
    return H - BAND * H


def d1_body(side, W, H):
    """Jharokha tile: emerald ground, gold jali lattice, six-petal flowers."""
    emerald, deep, gold, petal = "#0E5A47", "#0A4636", "#C9A24A", "#E2C06E"
    cell = 16.0
    ox = 0.0 if side == "front" else cell / 2
    oy = band_top(H) % cell              # a tile-grid line sits exactly on the band
    parts = [rect(0, 0, W, H, emerald)]
    for i in range(-1, int(W // cell) + 2):
        for j in range(-1, int(H // cell) + 2):
            x, y = i * cell + ox, j * cell + oy
            if (i + j) % 2 == 0:
                parts.append(rect(x, y, cell, cell, deep))
            parts.append(flower(x + cell / 2, y + cell / 2, 4.4, petal, deep,
                                rot=0 if (i + j) % 2 == 0 else 30))
            parts.append(circle(x, y, 0.8, gold))
    for i in range(-1, int(W // cell) + 3):
        parts.append(line(i * cell + ox, -2, i * cell + ox, H + 2, gold, 0.45))
    for j in range(-1, int(H // cell) + 3):
        parts.append(line(-2, j * cell + oy, W + 2, j * cell + oy, gold, 0.45))
    return "".join(parts)


def d2_body(side, W, H):
    """Rajasthan arch: teal ground, cream arched niches, marigold blooms."""
    teal, cream, sage, mari, red, centre = "#5E9AA2", "#F5ECD8", "#8FA889", "#E9772A", "#B5282E", "#F2C14E"
    cw, ch = 19.0, 24.0
    ox = 0.0 if side == "front" else cw / 2
    oy = band_top(H) % ch                # row boundary sits exactly on the band
    parts = [rect(0, 0, W, H, teal)]
    for i in range(-1, int(W // cw) + 2):
        for j in range(-1, int(H // ch) + 2):
            x, y = i * cw + ox, j * ch + oy
            cx, cy = x + cw / 2, y + ch / 2
            parts.append(arch(cx, cy, 11, 16, cream))
            parts.append(arch(cx, cy + 1.2, 7.2, 10.5, sage))
            parts.append(marigold(cx, cy + 2.4, 2.4, mari, centre))
            parts.append(circle(x, y, 0.9, red))
    return "".join(parts)


def d3_body(side, W, H):
    """Kolam loops: cream ground, maroon dot grid, interlocking loop crosses."""
    cream, maroon, red = "#F3E8D4", "#7A2D1D", "#B5282E"
    step = 6.5
    o = 0.0 if side == "front" else step
    parts = [rect(0, 0, W, H, cream)]
    for i in range(-1, int(W // step) + 2):
        for j in range(-1, int(H // step) + 2):
            parts.append(circle(i * step + o, j * step + o, 0.42, maroon, ' opacity="0.55"'))
    for i in range(-1, int(W // (2 * step)) + 2):
        for j in range(-1, int(H // (2 * step)) + 2):
            cx, cy = i * 2 * step + o, j * 2 * step + o
            parts.append(kolam(cx, cy, 3.2, maroon))
            parts.append(circle(cx + step, cy + step, 1.3, red))
    return "".join(parts)


def d4_body(side, W, H):
    """Kanjivaram silk: mint ground, magenta/orange/green/gold stripes, gold buttas."""
    mint, magenta, orange, green, gold, core = "#A9CDBB", "#D81E5B", "#F07A22", "#1F7A4D", "#E0AE3E", "#8E1B3A"
    band = 24.0
    o = 0.0 if side == "front" else band / 2
    parts = [rect(0, 0, W, H, mint)]
    for k in range(-1, int(W // band) + 2):
        x0 = k * band + o
        parts.append(rect(x0, 0, 3.4, H, magenta))
        parts.append(rect(x0 + 4.0, 0, 1.2, H, orange))
        parts.append(rect(x0 + 5.6, 0, 0.5, H, gold))
        parts.append(rect(x0 + 6.5, 0, 2.2, H, green))
        bx = x0 + 12.3
        for r in range(-1, int(H // 9) + 2):
            y = r * 9.0 + (4.5 if r % 2 else 0)
            rot = 15 if r % 2 else -15
            parts.append(butta(bx, y, 3.2, gold, core, rot))
            parts.append(circle(bx + 6.0, y + 4.5, 0.7, gold))
    return "".join(parts)


def d5_body(side, W, H):
    """Elephant & peacock tiles: navy ground, pink-ruled tiles alternating motifs."""
    navy, pink, yellow, teal = "#1C2F74", "#E8246E", "#F2E65A", "#2BB38A"
    cell = 19.0
    par = 0 if side == "front" else 1
    o = 0.0 if side == "front" else cell / 2
    parts = [rect(0, 0, W, H, navy)]
    for i in range(-1, int(W // cell) + 2):
        for j in range(-1, int(H // cell) + 2):
            x, y = i * cell + o, j * cell + o
            cx, cy = x + cell / 2, y + cell / 2
            parts.append(f'<rect x="{fmt(x + 1.2)}" y="{fmt(y + 1.2)}" width="{fmt(cell - 2.4)}" '
                         f'height="{fmt(cell - 2.4)}" fill="none" stroke="{pink}" stroke-width="0.7"/>')
            flip = 1 if i % 2 == 0 else -1
            if (i + j + par) % 2 == 0:
                parts.append(elephant(cx, cy, 5.2, pink, yellow, flip))
            else:
                parts.append(peacock(cx, cy, 4.6, yellow, teal, navy, pink, flip))
            parts.append(circle(x, y, 1.0, teal))
    return "".join(parts)


DESIGNS = [
    dict(slug="01-jharokha-tile", title="Design 1 · Jharokha Tile", body=d1_body,
         cap="#0A4636", rule="#C9A24A", ink="#E6C873", motif="#D9B45A",
         box="#0A4636", border_bg="#0A4636", strip="#B5282E"),
    dict(slug="02-rajasthan-arch", title="Design 2 · Rajasthan Arch", body=d2_body,
         cap="#B5282E", rule="#F2C14E", ink="#F2C14E", motif="#F2C14E",
         box="#B5282E", border_bg="#B5282E", strip="#5E9AA2"),
    dict(slug="03-kolam-loops", title="Design 3 · Kolam Loops", body=d3_body,
         cap="#7A2D1D", rule="#C9A24A", ink="#F3E8D4", motif="#D9B45A",
         box="#7A2D1D", border_bg="#7A2D1D", strip="#B5282E"),
    dict(slug="04-silk-buttas", title="Design 4 · Silk Buttas", body=d4_body,
         cap="#D81E5B", rule="#E0AE3E", ink="#FFF0C2", motif="#E0AE3E",
         box="#D81E5B", border_bg="#8E1B3A", strip="#1F7A4D"),
    dict(slug="05-elephant-peacock", title="Design 5 · Elephant &amp; Peacock", body=d5_body,
         cap="#16245E", rule="#E8246E", ink="#F2E65A", motif="#E0B349",
         box="#16245E", border_bg="#16245E", strip="#E8246E"),
]


# ---------- packet geometry and parts ------------------------------------

def geom(W, H):
    D = 0.20 * W              # dome height: the top of the packet is a half-ellipse
    F0 = D + 0.06 * W         # flap bottom at the edges
    F1 = F0 + 0.07 * W        # flap bottom sags to F1 at the centre
    return {"D": D, "F0": F0, "F1": F1, "FM": (F0 + F1) / 2, "bh": BAND * H}


def outline(W, H):
    D = 0.20 * W
    return f"M0,{fmt(H)} V{fmt(D)} A{fmt(W / 2)},{fmt(D)} 0 0 1 {fmt(W)},{fmt(D)} V{fmt(H)} Z"


def brocade_def(d):
    """Fine diamond brocade, used as a vector overlay on the body."""
    return ('<pattern id="brocade" width="4.5" height="4.5" patternUnits="userSpaceOnUse">'
            f'<path d="M2.25,0 L4.5,2.25 L2.25,4.5 L0,2.25 Z" fill="{d["motif"]}" opacity="0.16"/>'
            f'<circle cx="2.25" cy="2.25" r="0.45" fill="{d["ink"]}" opacity="0.5"/></pattern>')


def border(d, W, H, g):
    """Bottom band: gold temple arches on the border colour, over a strip of flowers."""
    bh = g["bh"]
    y0 = H - bh
    strip = bh * 0.28
    mid = y0 + (bh - strip) / 2
    aw = bh * 0.8
    parts = [rect(0, y0, W, bh, d["border_bg"]), line(0, y0 + 0.2, W, y0 + 0.2, d["motif"], 0.4)]
    # whole motifs only, centred with equal margins at both ends
    n_arch = max(1, round(W / aw))
    pitch = W / n_arch
    for k in range(n_arch):
        cx = (k + 0.5) * pitch
        parts.append(arch(cx, mid, aw * 0.56, (bh - strip) * 0.82, d["motif"]))
        parts.append(arch(cx, mid + 0.4, aw * 0.26, (bh - strip) * 0.4, d["border_bg"]))
    parts.append(rect(0, H - strip, W, strip, d["strip"]))
    n_dot = max(1, round(W / (aw / 2)))
    if n_dot % 2 == 0:
        n_dot += 1                       # odd count: a flower at both ends
    pitch_dot = W / n_dot
    for k in range(n_dot):
        cx = (k + 0.5) * pitch_dot
        if k % 2 == 0:
            parts.append(flower(cx, H - strip / 2, strip * 0.36, d["motif"], d["strip"]))
        else:
            parts.append(circle(cx, H - strip / 2, strip * 0.14, d["motif"]))
    return "".join(parts)


def cartouche(d, W, H, g):
    """'Happy Deepavali' box on the front, centred in the body area."""
    bw, bh_ = 0.68 * W, 0.22 * H
    yc = (g["FM"] + (H - g["bh"])) / 2
    x0, y0 = (W - bw) / 2, yc - bh_ / 2
    cx = W / 2
    parts = [
        rect(x0, y0, bw, bh_, d["box"], f' rx="1.5" stroke="{d["rule"]}" stroke-width="0.5"'),
        rect(x0 + 1.6, y0 + 1.6, bw - 3.2, bh_ - 3.2, "none", f' rx="1" stroke="{d["rule"]}" stroke-width="0.2"'),
    ]
    for yy in (y0 + 3.2, y0 + bh_ - 3.2):
        parts.append(line(cx - 14, yy, cx - 3.5, yy, d["rule"], 0.3))
        parts.append(line(cx + 3.5, yy, cx + 14, yy, d["rule"], 0.3))
        parts.append(f'<path d="M{fmt(cx)},{fmt(yy - 1.3)} L{fmt(cx + 1.3)},{fmt(yy)} '
                     f'L{fmt(cx)},{fmt(yy + 1.3)} L{fmt(cx - 1.3)},{fmt(yy)} Z" fill="{d["rule"]}"/>')
    f1, f2 = 0.055 * W, 0.078 * W
    parts.append(f'<text x="{fmt(cx)}" y="{fmt(yc - 2.4)}" text-anchor="middle" font-family="{FONT}" '
                 f'font-size="{fmt(f1)}" fill="{d["ink"]}">Happy</text>')
    parts.append(f'<text x="{fmt(cx)}" y="{fmt(yc + f2 * 0.72)}" text-anchor="middle" font-family="{FONT}" '
                 f'font-style="italic" font-size="{fmt(f2)}" fill="{d["ink"]}">Deepavali</text>')
    return "".join(parts)


def flap_edge(W, F0, F1, colour):
    """Gold rule traced exactly along the flap's bottom curve, edge to edge."""
    pts = []
    for k in range(41):
        t = k / 40
        # quadratic from (0, F0) via (W/2, F1) to (W, F0): x = W*t, y = F0 + 2t(1-t)(F1-F0)
        pts.append(f"{fmt(W * t)},{fmt(F0 + 2 * t * (1 - t) * (F1 - F0))}")
    return (f'<path d="M{pts[0]}' + "".join(f" L{p}" for p in pts[1:]) +
            f'" fill="none" stroke="{colour}" stroke-width="0.5"/>')


def flap(d, W, H, g):
    """Plain domed flap in the theme colour, with a gold lotus and a gold edge rule."""
    D, F0, F1, FM = g["D"], g["F0"], g["F1"], g["FM"]
    cap_d = (f"M0,{fmt(D)} A{fmt(W / 2)},{fmt(D)} 0 0 1 {fmt(W)},{fmt(D)} "
             f"L{fmt(W)},{fmt(F0)} Q{fmt(W / 2)},{fmt(F1)} 0,{fmt(F0)} Z")
    cy = FM / 2 + 1
    return (f'<path d="{cap_d}" fill="{d["cap"]}"/>'
            + flap_edge(W, F0, F1, d["motif"])
            + lotus(W / 2, cy, 0.075 * W, d["motif"], d["cap"]))


def packet(d, size, side):
    W, H = SIZES[size]
    g = geom(W, H)
    inner = [d["body"](side, W, H),
             f'<rect width="{fmt(W)}" height="{fmt(H)}" fill="url(#brocade)"/>',
             border(d, W, H, g)]
    if side == "front":
        inner.append(cartouche(d, W, H, g))
    return (f'<g clip-path="url(#outline-{size})">' + "".join(inner) + "</g>"
            + flap(d, W, H, g)
            + f'<path d="{outline(W, H)}" fill="none" stroke="#222" stroke-width="0.25"/>')


def clip_paths(sizes):
    return "".join(f'<clipPath id="outline-{s}"><path d="{outline(*SIZES[s])}"/></clipPath>' for s in sizes)


# ---------- print die-line: one size, front + back, A4 landscape ---------

def print_sheet(d, size):
    W, H = SIZES[size]
    x0 = (297 - (2 * W + GAP)) / 2
    y0 = 10  # keeps the FRONT/BACK captions clear of the printer margin
    head = (f'<text x="148.5" y="7" text-anchor="middle" font-family="{FONT}" font-size="4.2" fill="#222">'
            f'Deepavali Ang Bao · {d["title"]} · {SIZE_NAMES[size]} '
            f'({fmt(W / 10)} × {fmt(H / 10)} cm) · print at 100%, cut along the black outline</text>')
    labels = (f'<text x="{fmt(x0 + W / 2)}" y="{fmt(y0 + H + 5)}" text-anchor="middle" font-family="{FONT}" '
              f'font-size="3.5" fill="#555">FRONT</text>'
              f'<text x="{fmt(x0 + W + GAP + W / 2)}" y="{fmt(y0 + H + 5)}" text-anchor="middle" '
              f'font-family="{FONT}" font-size="3.5" fill="#555">BACK</text>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="210mm" viewBox="0 0 297 210">'
            f'<defs>{clip_paths([size])}{brocade_def(d)}</defs>'
            '<rect width="297" height="210" fill="#ffffff"/>' + head
            + f'<g transform="translate({fmt(x0)} {fmt(y0)})">{packet(d, size, "front")}</g>'
            + f'<g transform="translate({fmt(x0 + W + GAP)} {fmt(y0)})">{packet(d, size, "back")}</g>'
            + labels + "</svg>")


# ---------- presentation mockup: all sizes, detail callouts --------------

def mockup(d):
    CW, CH = 1600, 1000
    sizes = ["small", "medium", "large"]
    pair_w = {s: 2 * SIZES[s][0] * MOCK_S + 16 for s in sizes}
    x = (CW - (sum(pair_w.values()) + 2 * 70)) / 2
    base_y = 640
    mw, mh = SIZES["medium"]
    callouts = [
        ("Plain colour flap with gold motif", "front", mw / 2, 16),
        ("Traditional checked design", "back", mw / 2, 70),
        ("Traditional border detail (bottom)", "front", mw / 2, mh - 16),
        ("Premium textured finish", "front", 0.22 * mw, 0.33 * mh),
    ]
    clips, parts = [], []
    for i in range(len(callouts)):
        clips.append(f'<clipPath id="zc{i}"><circle cx="{200 + 400 * i}" cy="800" r="92"/></clipPath>')

    parts.append(rect(0, 0, CW, CH, CREAM))
    parts.append(f'<text x="800" y="88" text-anchor="middle" font-family="{FONT}" font-size="44" '
                 f'fill="#4A1A10">Deepavali Ang Bao · {d["title"]}</text>')
    parts.append(f'<text x="800" y="128" text-anchor="middle" font-family="{FONT}" font-size="22" '
                 f'fill="#6B4A3A">Front and back at three sizes · plain domed flap with gold motif · '
                 f'checked body · bottom border</text>')

    for s in sizes:
        W, H = SIZES[s]
        cx = x + pair_w[s] / 2
        parts.append(f'<text x="{fmt(cx)}" y="190" text-anchor="middle" font-family="{FONT}" '
                     f'font-size="30" fill="#5A1F14">{SIZE_NAMES[s]}</text>')
        parts.append(f'<text x="{fmt(cx)}" y="224" text-anchor="middle" font-family="{FONT}" '
                     f'font-size="18" fill="#5A1F14">({fmt(W / 10)} cm W x {fmt(H / 10)} cm H)</text>')
        parts.append(line(cx - 70, 240, cx - 14, 240, d["rule"], 1))
        parts.append(line(cx + 14, 240, cx + 70, 240, d["rule"], 1))
        parts.append(f'<path d="M{fmt(cx)},237 L{fmt(cx + 3)},240 L{fmt(cx)},243 L{fmt(cx - 3)},240 Z" '
                     f'fill="{d["rule"]}"/>')
        fy = base_y - H * MOCK_S
        for side, fx in (("front", x), ("back", x + W * MOCK_S + 16)):
            parts.append(f'<g filter="url(#sh)"><g transform="translate({fmt(fx)} {fmt(fy)}) '
                         f'scale({MOCK_S})">{packet(d, s, side)}</g></g>')
            parts.append(f'<text x="{fmt(fx + W * MOCK_S / 2)}" y="{base_y + 34}" text-anchor="middle" '
                         f'font-family="{FONT}" font-size="20" fill="#4A1A10">'
                         f'{"Front" if side == "front" else "Back"}</text>')
        x += pair_w[s] + 70

    cy, r = 800, 92
    for i, (caption, side, fx, fy) in enumerate(callouts):
        cx = 200 + 400 * i
        parts.append(f'<g clip-path="url(#zc{i})"><rect x="{fmt(cx - r)}" y="{fmt(cy - r)}" '
                     f'width="{2 * r}" height="{2 * r}" fill="{CREAM}"/>'
                     f'<g transform="translate({fmt(cx - fx * ZOOM)} {fmt(cy - fy * ZOOM)}) scale({ZOOM})">'
                     f'{packet(d, "medium", side)}</g></g>')
        parts.append(circle(cx, cy, r, "none", ' stroke="#B08A3E" stroke-width="3"'))
        parts.append(f'<text x="{cx}" y="935" text-anchor="middle" font-family="{FONT}" '
                     f'font-size="22" fill="#4A1A10">{caption}</text>')

    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000">'
            '<defs>'
            + clip_paths(sizes) + "".join(clips) + brocade_def(d)
            + '<filter id="sh" x="-20%" y="-20%" width="140%" height="140%">'
              '<feDropShadow dx="2.5" dy="4" stdDeviation="3.5" flood-color="#3a2410" flood-opacity="0.28"/>'
              '</filter>'
            + '</defs>' + "".join(parts) + "</svg>")


def main():
    os.makedirs(os.path.join(OUT, "mockups"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "print"), exist_ok=True)
    for d in DESIGNS:
        p = os.path.join(OUT, "mockups", f'{d["slug"]}.svg')
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(mockup(d))
        print(p, os.path.getsize(p))
        for size in SIZES:
            p = os.path.join(OUT, "print", f'{d["slug"]}-{size}.svg')
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(print_sheet(d, size))
            print(p, os.path.getsize(p))


if __name__ == "__main__":
    main()
