#!/usr/bin/env python3
"""Generate five Deepavali ang bao die-line sheets (SVG, millimetres).

Each sheet is A4 landscape: front and back panels at 95 x 165 mm (medium
packet, fits a flat SGD 50 note), a plain-colour arched top cap that follows
the design's theme colour, and a patterned body that covers the whole packet.
"""
import math
import os

W, H = 95.0, 165.0  # finished packet size, mm
OUT = "/home/user/suite/angbao"
FONT = "Georgia, 'DejaVu Serif', 'Times New Roman', serif"


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
    """Four interlocking loops around a centre dot (kolam-style cross)."""
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
    """Caparisoned elephant, facing right. Drawn in unit space, then scaled."""
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
    """Peacock with a fanned tail, facing right. Drawn in unit space, then scaled."""
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


# ---------- the five body patterns (front / back use different offsets) --

def d1_body(side):
    """Jharokha tile: emerald ground, gold jali lattice, six-petal flowers."""
    emerald, deep, gold, petal = "#0E5A47", "#0A4636", "#C9A24A", "#E2C06E"
    cell = 16.0
    o = 0.0 if side == "front" else cell / 2
    parts = [rect(0, 0, W, H, emerald)]
    for i in range(-1, 8):
        for j in range(-1, 12):
            x, y = i * cell + o, j * cell + o
            if (i + j) % 2 == 0:
                parts.append(rect(x, y, cell, cell, deep))
            parts.append(flower(x + cell / 2, y + cell / 2, 4.4, petal, deep,
                                rot=0 if (i + j) % 2 == 0 else 30))
            parts.append(circle(x, y, 0.8, gold))
    for i in range(-1, 8):
        parts.append(line(i * cell + o, -2, i * cell + o, H + 2, gold, 0.45))
    for j in range(-1, 12):
        parts.append(line(-2, j * cell + o, W + 2, j * cell + o, gold, 0.45))
    return "".join(parts)


def d2_body(side):
    """Rajasthan arch: teal ground, cream arched niches, marigold blooms."""
    teal, cream, sage, marigold_c, red, centre = "#5E9AA2", "#F5ECD8", "#8FA889", "#E9772A", "#B5282E", "#F2C14E"
    cw, ch = 19.0, 24.0
    o = (0.0, 0.0) if side == "front" else (cw / 2, ch / 2)
    parts = [rect(0, 0, W, H, teal)]
    for i in range(-1, 7):
        for j in range(-1, 9):
            x, y = i * cw + o[0], j * ch + o[1]
            cx, cy = x + cw / 2, y + ch / 2
            parts.append(arch(cx, cy, 11, 16, cream))
            parts.append(arch(cx, cy + 1.2, 7.2, 10.5, sage))
            parts.append(marigold(cx, cy + 2.4, 2.4, marigold_c, centre))
            parts.append(circle(x, y, 0.9, red))
    return "".join(parts)


def d3_body(side):
    """Kolam loops: cream ground, maroon dot grid, interlocking loop crosses."""
    cream, maroon, red = "#F3E8D4", "#7A2D1D", "#B5282E"
    step = 6.5
    o = 0.0 if side == "front" else step
    parts = [rect(0, 0, W, H, cream)]
    for i in range(-1, 17):
        for j in range(-1, 28):
            parts.append(circle(i * step + o, j * step + o, 0.42, maroon, ' opacity="0.55"'))
    for i in range(-1, 9):
        for j in range(-1, 15):
            cx, cy = i * 2 * step + o, j * 2 * step + o
            parts.append(kolam(cx, cy, 3.2, maroon))
            parts.append(circle(cx + step, cy + step, 1.3, red))
    return "".join(parts)


def d4_body(side):
    """Kanjivaram silk: mint ground, magenta/orange/green/gold stripes, gold buttas."""
    mint, magenta, orange, green, gold, core = "#A9CDBB", "#D81E5B", "#F07A22", "#1F7A4D", "#E0AE3E", "#8E1B3A"
    band = 24.0
    o = 0.0 if side == "front" else band / 2
    parts = [rect(0, 0, W, H, mint)]
    for k in range(-1, 6):
        x0 = k * band + o
        parts.append(rect(x0, 0, 3.4, H, magenta))
        parts.append(rect(x0 + 4.0, 0, 1.2, H, orange))
        parts.append(rect(x0 + 5.6, 0, 0.5, H, gold))
        parts.append(rect(x0 + 6.5, 0, 2.2, H, green))
        bx = x0 + 12.3
        for r in range(-1, 19):
            y = r * 9.0 + (4.5 if r % 2 else 0)
            rot = 15 if r % 2 else -15
            parts.append(butta(bx, y, 3.2, gold, core, rot))
            parts.append(circle(bx + 6.0, y + 4.5, 0.7, gold))
    return "".join(parts)


def d5_body(side):
    """Elephant & peacock tiles: navy ground, pink-ruled tiles alternating motifs."""
    navy, pink, yellow, teal = "#1C2F74", "#E8246E", "#F2E65A", "#2BB38A"
    cell = 19.0
    par = 0 if side == "front" else 1
    o = 0.0 if side == "front" else cell / 2
    parts = [rect(0, 0, W, H, navy)]
    for i in range(-1, 7):
        for j in range(-1, 10):
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
         cap="#0A4636", ink="#E6C873", rule="#C9A24A"),
    dict(slug="02-rajasthan-arch", title="Design 2 · Rajasthan Arch", body=d2_body,
         cap="#B5282E", ink="#F2C14E", rule="#F2C14E"),
    dict(slug="03-kolam-loops", title="Design 3 · Kolam Loops", body=d3_body,
         cap="#7A2D1D", ink="#F3E8D4", rule="#C9A24A"),
    dict(slug="04-silk-buttas", title="Design 4 · Silk Buttas", body=d4_body,
         cap="#D81E5B", ink="#FFF0C2", rule="#E0AE3E"),
    dict(slug="05-elephant-peacock", title="Design 5 · Elephant &amp; Peacock", body=d5_body,
         cap="#16245E", ink="#F2E65A", rule="#E8246E"),
]

FRONT_TEXT = "Happy Deepavali"
BACK_TEXT = "Light &amp; Prosperity"


def panel(d, side):
    text, fs = (FRONT_TEXT, 6.8) if side == "front" else (BACK_TEXT, 5.8)
    return "".join([
        f'<g clip-path="url(#pkt)">{d["body"](side)}</g>',
        f'<rect x="2.5" y="2.5" width="{fmt(W - 5)}" height="{fmt(H - 5)}" rx="1" fill="none" '
        f'stroke="{d["rule"]}" stroke-width="0.5"/>',
        # plain top cap: follows the theme colour, curved lower edge
        f'<path d="M0,0 H{fmt(W)} V30 Q{fmt(W / 2)},46 0,30 Z" fill="{d["cap"]}"/>',
        f'<path d="M3,28.2 Q{fmt(W / 2)},44.4 {fmt(W - 3)},28.2" fill="none" '
        f'stroke="{d["rule"]}" stroke-width="0.5"/>',
        f'<text x="{fmt(W / 2)}" y="19.5" text-anchor="middle" font-family="{FONT}" '
        f'font-style="italic" font-size="{fs}" fill="{d["ink"]}">{text}</text>',
        # cut line
        f'<rect x="0" y="0" width="{fmt(W)}" height="{fmt(H)}" rx="2" fill="none" stroke="#222" stroke-width="0.25"/>',
    ])


def sheet(d):
    head = (f'<text x="148.5" y="11" text-anchor="middle" font-family="{FONT}" font-size="5.5" fill="#222">'
            f'Deepavali Ang Bao · {d["title"]}</text>'
            f'<text x="148.5" y="17" text-anchor="middle" font-family="{FONT}" font-size="2.9" fill="#555">'
            'Medium packet 95 × 165 mm, fits a flat SGD 50 note · print at 100% on A4 landscape · '
            'cut along the black outline</text>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="210mm" viewBox="0 0 297 210">'
        f'<defs><clipPath id="pkt"><rect width="{fmt(W)}" height="{fmt(H)}" rx="2"/></clipPath></defs>'
        '<rect width="297" height="210" fill="#ffffff"/>'
        + head
        + f'<g transform="translate(43.5 24)">{panel(d, "front")}</g>'
        + f'<g transform="translate(158.5 24)">{panel(d, "back")}</g>'
        + f'<text x="91" y="197" text-anchor="middle" font-family="{FONT}" font-size="3.5" fill="#555">FRONT</text>'
        + f'<text x="206" y="197" text-anchor="middle" font-family="{FONT}" font-size="3.5" fill="#555">BACK</text>'
        + '</svg>'
    )


def main():
    os.makedirs(OUT, exist_ok=True)
    for d in DESIGNS:
        path = os.path.join(OUT, f'{d["slug"]}.svg')
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(sheet(d))
        print(path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
