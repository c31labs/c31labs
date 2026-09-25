#!/usr/bin/env python3
"""Draws the profile banner (light and dark) and the product marks.

Text is set in Company31 Sans and Mono and converted to outlines, because
GitHub serves SVGs as images and an image cannot load a web font.

    pip install fonttools
    python3 assets/build-assets.py --fonts <folder with Company31Sans-*.ttf>
"""
import argparse
import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).resolve().parent

THEMES = {
    "light": dict(ground="#FAFBFF", ink="#0A1633", muted="#4A5575", accent="#1C4FD8",
                  strong="#12339E", grad_a="#12339E", grad_b="#3B8AF7",
                  grid="#12339E", grid_o=0.06, grid5_o=0.12, line_o=0.30),
    "dark": dict(ground="#0A1633", ink="#E9F0FC", muted="#A7B5D3", accent="#3B8AF7",
                 strong="#8FB8FF", grad_a="#3B8AF7", grad_b="#A9CCFB",
                 grid="#3B8AF7", grid_o=0.07, grid5_o=0.14, line_o=0.40),
}


class Face:
    def __init__(self, path):
        self.font = TTFont(path)
        self.glyphs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upm = self.font["head"].unitsPerEm

    def width(self, text, size, tracking=0.0):
        s = size / self.upm
        return sum(self.glyphs[self.cmap[ord(c)]].width * s + tracking for c in text) - tracking

    def path(self, text, x, y, size, tracking=0.0, anchor="start"):
        s = size / self.upm
        if anchor == "end":
            x -= self.width(text, size, tracking)
        elif anchor == "middle":
            x -= self.width(text, size, tracking) / 2
        out = []
        for c in text:
            g = self.glyphs[self.cmap[ord(c)]]
            pen = SVGPathPen(self.glyphs, ntos=lambda n: ("%.1f" % n).rstrip("0").rstrip("."))
            g.draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
            d = pen.getCommands()
            if d:
                out.append(d)
            x += g.width * s + tracking
        return " ".join(out)


def banner(t, sans, sans_b, mono):
    W, H = 1280, 400
    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'role="img" aria-label="Company31. Close to the work. Built to be used. '
      f'An independent think tank and engineering workbench in Sydney, by Manuel Re.">')
    a(f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0" stop-color="{t["grad_a"]}"/><stop offset="1" stop-color="{t["grad_b"]}"/>'
      f'</linearGradient>'
      f'<pattern id="m" width="26" height="26" patternUnits="userSpaceOnUse">'
      f'<path d="M26 0H0V26" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_o"]}"/></pattern>'
      f'<pattern id="M" width="130" height="130" patternUnits="userSpaceOnUse">'
      f'<path d="M130 0H0V130" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid5_o"]}"/></pattern>'
      f'</defs>')
    a(f'<rect width="{W}" height="{H}" fill="{t["ground"]}"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#m)"/><rect width="{W}" height="{H}" fill="url(#M)"/>')

    # Sheet frame with a drafting scale along the top edge.
    lo = t["line_o"]
    a(f'<rect x="20.5" y="20.5" width="{W-41}" height="{H-41}" fill="none" stroke="{t["strong"]}" stroke-opacity="{lo}"/>')
    ticks = []
    for i, x in enumerate(range(40, W - 39, 13)):
        h = 10 if i % 10 == 0 else 6 if i % 5 == 0 else 3
        ticks.append(f"M{x+.5} 21V{21+h}")
    a(f'<path d="{" ".join(ticks)}" stroke="{t["strong"]}" stroke-opacity="{lo}"/>')

    # Left: eyebrow, headline, standfirst.
    X = 72
    a(f'<path d="{mono.path("FIG. 1  ·  COMPANY31  ·  C31LABS", X, 96, 15, 1.6)}" fill="{t["accent"]}"/>')
    a(f'<path d="{sans_b.path("Close to the work.", X, 170, 62, -0.6)}" fill="{t["ink"]}"/>')
    a(f'<path d="{sans_b.path("Built to be used.", X, 240, 62, -0.6)}" fill="url(#g)"/>')
    a(f'<path d="{sans.path("An independent think tank and engineering workbench.", X, 292, 22)}" fill="{t["muted"]}"/>')
    a(f'<path d="{sans.path("Apps I ship, tools I test in the field, essays on what I learn.", X, 322, 22)}" fill="{t["muted"]}"/>')

    # Right: the monogram, constructed. Guide circles in the golden ratio.
    cx, cy = 1010, 180
    r1, r2 = 47 * 1.62, 76 * 1.62
    a(f'<g fill="none" stroke="{t["strong"]}" stroke-opacity="{lo+.15}">'
      f'<circle cx="{cx}" cy="{cy}" r="{r2:.1f}" stroke-dasharray="4 5"/>'
      f'<circle cx="{cx}" cy="{cy}" r="{r1:.1f}"/>'
      f'<path d="M{cx-r2-22} {cy}H{cx+r2+22}M{cx} {cy-r2-22}V{cy+r2+22}" stroke-dasharray="1 4"/>'
      f'<path d="M{cx} {cy}L{cx+r1*.707:.1f} {cy-r1*.707:.1f}M{cx} {cy}L{cx-r2*.866:.1f} {cy+r2*.5:.1f}"/>'
      f'</g>')
    a(f'<path d="{mono.path("R 47", cx+r1*.707+8, cy-r1*.707-6, 13, 1)}" fill="{t["accent"]}"/>')
    a(f'<path d="{mono.path("R 76", cx-r2*.866-12, cy+r2*.5+20, 13, 1, "end")}" fill="{t["accent"]}"/>')
    a(f'<path d="{mono.path("1.000 : 1.618", cx+74, cy+r2+2, 12, 1.2)}" fill="{t["muted"]}"/>')
    a(f'<path d="{sans_b.path("31", cx+2, cy+36, 104, -4, "middle")}" fill="url(#g)"/>')

    # Title block, where a footer would be.
    bx, by, bw, bh = W - 21 - 520, H - 21 - 34, 520, 34
    a(f'<g fill="none" stroke="{t["strong"]}" stroke-opacity="{lo}">'
      f'<rect x="{bx+.5}" y="{by+.5}" width="{bw}" height="{bh}"/>'
      + "".join(f'<path d="M{bx+c+.5} {by}V{by+bh}"/>' for c in (150, 290, 400)) + "</g>")
    for c, label in ((0, "DRAWN  M. RE"), (150, "SYDNEY  AU"), (290, "SCALE  1:1"), (400, "SHEET  1/2")):
        a(f'<path d="{mono.path(label, bx+c+14, by+22, 11.5, 1.3)}" fill="{t["muted"]}"/>')
    a("</svg>")
    return "".join(p)


MARKS = {
    # Slotello: a week of slots, one of them taken.
    "slotello": lambda c: (
        f'<rect x="22" y="28" width="52" height="46" fill="none" stroke="{c}" stroke-width="3"/>'
        f'<path d="M22 40H74M34 20V32M62 20V32" stroke="{c}" stroke-width="3" fill="none"/>'
        f'<path d="M30 50h8M44 50h8M58 50h8M30 62h8M58 62h8" stroke="{c}" stroke-width="3" stroke-opacity=".45"/>'
        f'<rect x="43" y="57" width="10" height="10" fill="{c}"/>'),
    # CyberSafe: a shield with a tick.
    "cybersafe": lambda c: (
        f'<path d="M48 16L74 26V48C74 64 62 76 48 82C34 76 22 64 22 48V26Z" fill="none" stroke="{c}" stroke-width="3"/>'
        f'<path d="M36 49L45 58L61 40" fill="none" stroke="{c}" stroke-width="4"/>'),
    # Proofline: an obligation, and the evidence behind it.
    "proofline": lambda c: (
        f'<path d="M28 16H58L70 28V80H28Z M58 16V28H70" fill="none" stroke="{c}" stroke-width="3"/>'
        f'<path d="M36 44L40 48L47 40M36 60L40 64L47 56" fill="none" stroke="{c}" stroke-width="3"/>'
        f'<path d="M52 44H62M52 60H62" stroke="{c}" stroke-width="3" stroke-opacity=".45"/>'),
}


def mark(name):
    # Drawn on ice so the mark reads on GitHub's light and dark themes alike.
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96" '
            f'role="img" aria-label="{name.capitalize()} mark">'
            f'<rect width="96" height="96" rx="22" fill="#EAF1FD"/>'
            f'<rect x=".75" y=".75" width="94.5" height="94.5" rx="21.25" fill="none" stroke="#12339E" stroke-opacity=".25" stroke-width="1.5"/>'
            f'{MARKS[name]("#12339E")}</svg>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True, type=pathlib.Path)
    f = ap.parse_args().fonts
    sans = Face(f / "Company31Sans-Regular.ttf")
    sans_b = Face(f / "Company31Sans-SemiBold.ttf")
    mono = Face(f / "Company31Mono-Regular.ttf")
    for name, t in THEMES.items():
        (HERE / f"banner-{name}.svg").write_text(banner(t, sans, sans_b, mono))
    for name in MARKS:
        (HERE / "icons" / f"{name}.svg").write_text(mark(name))


if __name__ == "__main__":
    main()
