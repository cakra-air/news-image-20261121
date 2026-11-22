"""Render the front page for 21 November 2026 from layout/frame.md.

All drawings are original vector shapes made here; the map uses the bundled
Natural Earth GeoJSON. Run: python render.py  -> entry.png
"""

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

from stories import (
    STORIES, REGION_NAMES, REGION_COLORS, STATS, DECK,
    DATE_LINE_1, DATE_LINE_2, SOURCE_LINE,
)

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join("C:", os.sep, "Windows", "Fonts")

PAPER = "#F7F2E7"
INK = "#181818"
RED = "#9E1F1F"
LINE = "#CBBB9C"
MUTED = "#6C6459"
CARD = "#FDFBF4"
PANEL = "#FFFDF7"
BUTTON = "#F6F0E2"
OCEAN = "#D8E8F1"
LAND = "#EADCB9"
COAST = "#B8A175"
GRAT = "#C6DEEA"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lighten(h, f):
    r, g, b = rgb(h)
    return tuple(int(v + (255 - v) * f) for v in (r, g, b))


def face(name, size):
    path = os.path.join(FONT_DIR, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F = {
    "mast": face("georgiab.ttf", 66),
    "deck": face("georgia.ttf", 15),
    "stat": face("georgiab.ttf", 30),
    "cap": face("arial.ttf", 7),
    "rgn": face("arialbd.ttf", 9),
    "mk": face("arialbd.ttf", 9),
    "ms": face("arial.ttf", 7),
    "mh": face("georgiab.ttf", 18),
    "mb": face("arial.ttf", 10),
    "sk": face("arialbd.ttf", 8),
    "ss": face("arial.ttf", 7),
    "sh": face("georgiab.ttf", 11),
    "sb": face("arial.ttf", 9),
    "num": face("arialbd.ttf", 8),
    "lh": face("arial.ttf", 8),
    "ls": face("arial.ttf", 7),
    "leg": face("arial.ttf", 7),
    "idx": face("arialbd.ttf", 8),
    "lab": face("arialbd.ttf", 9),
    "date": face("arial.ttf", 8),
    "src": face("arial.ttf", 9),
    "art_l": face("arialbd.ttf", 9),
    "art_s": face("arialbd.ttf", 9),
}


def txt(d, xy, s, f, fill, anchor=None):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def wrap(d, s, f, maxw):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def fit(d, s, f, maxw):
    if d.textlength(s, font=f) <= maxw:
        return s
    s = s.rstrip()
    while s and d.textlength(s + "…", font=f) > maxw:
        s = s[:-1]
    return s + "…"


def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def chip(d, x, y, label, color="#2E7D4F"):
    w = int(d.textlength(label, font=F["cap"])) + 10
    rrect(d, (x, y, x + w, y + 13), 2, fill=color)
    txt(d, (x + w / 2, y + 6.5), label, F["cap"], "#FFFFFF", "mm")


# --------------------------------------------------------------------------
# Original vector illustrations. Every artwork carries three things inside it:
# WHEN (a clock pill), WHERE (place label) and WHAT (the event, drawn + tagged).
# --------------------------------------------------------------------------
def pill(d, x, y, text, font=None, bg=INK, fg="#FFFFFF"):
    """Contrasting label drawn inside the artwork, so the picture explains itself."""
    f = font or F["art_s"]
    w = d.textlength(text, font=f)
    d.rounded_rectangle((x, y, x + w + 8, y + f.size + 4), radius=2, fill=rgb(bg))
    d.text((x + 4, y + 1), text, font=f, fill=fg)
    return x + w + 8


def tag(d, x, y, text, bg="#9E1F1F", font=None, fg="#FFFFFF"):
    return pill(d, x, y, text, font or F["art_s"], bg, fg)


def clock(d, x, y, r, hour, minute):
    d.ellipse((x - r, y - r, x + r, y + r), fill="#FFFFFF", outline=INK)
    for k in range(12):
        a = math.pi / 2 - k * math.pi / 6
        d.line((x + (r - 3) * math.cos(a), y - (r - 3) * math.sin(a),
                x + r * math.cos(a), y - r * math.sin(a)), fill=INK)
    a = math.pi / 2 - (hour % 12 + minute / 60) * math.pi / 6
    d.line((x, y, x + (r - 5) * math.cos(a), y - (r - 5) * math.sin(a)), fill=RED, width=2)
    a = math.pi / 2 - minute * math.pi / 30
    d.line((x, y, x + (r - 2) * math.cos(a), y - (r - 2) * math.sin(a)), fill=INK)


def _ship(d, x, y, s=1.0, fire=False):
    d.polygon([(x - 18 * s, y), (x + 18 * s, y), (x + 14 * s, y + 8 * s),
               (x - 14 * s, y + 8 * s)], fill=INK)
    d.rectangle((x - 12 * s, y - 6 * s, x + 10 * s, y), fill="#CFCBC0")
    for i in range(3):
        d.rectangle((x - 10 * s + i * 7 * s, y - 4 * s, x - 5 * s + i * 7 * s, y - 1 * s),
                    fill=["#2E5B9A", "#B4674A", "#F2C14E"][i])
    d.rectangle((x + 10 * s, y - 10 * s, x + 16 * s, y), fill="#E9E4D8")
    d.rectangle((x + 11 * s, y - 9 * s, x + 15 * s, y - 6 * s), fill="#4A6E8A")
    d.line((x + 13 * s, y - 10 * s, x + 13 * s, y - 18 * s), fill=INK, width=1)
    if fire:
        d.polygon([(x - 8 * s, y - 6 * s), (x - 4 * s, y - 20 * s), (x, y - 8 * s)], fill="#E2672A")
        d.polygon([(x - 1 * s, y - 6 * s), (x + 3 * s, y - 16 * s), (x + 6 * s, y - 6 * s)], fill="#F2C14E")
        for k in range(4):
            d.ellipse((x + 6 * s + k * 4 * s, y - 20 * s - k * 3 * s,
                       x + 12 * s + k * 4 * s, y - 14 * s - k * 3 * s), fill="#9A958C")


def _flag(d, x, y, w, h, bands, vertical=False):
    for i, c in enumerate(bands):
        if vertical:
            d.rectangle((x + i * w / len(bands), y, x + (i + 1) * w / len(bands), y + h), fill=c)
        else:
            d.rectangle((x, y + i * h / len(bands), x + w, y + (i + 1) * h / len(bands)), fill=c)


def _person(d, x, y, s, shirt):
    d.ellipse((x - 2 * s, y - 9 * s, x + 2 * s, y - 5 * s), fill="#C9A982")
    d.rectangle((x - 3 * s, y - 5 * s, x + 3 * s, y + 3 * s), fill=shirt)
    d.line((x - 2 * s, y + 3 * s, x - 3 * s, y + 9 * s), fill=INK, width=2)
    d.line((x + 2 * s, y + 3 * s, x + 3 * s, y + 9 * s), fill=INK, width=2)


def s_gulf(d, w, h):
    """Bahrain / Hormuz, 05:00 UTC — Iran strikes Bahrain and fires on two tankers."""
    d.rectangle((0, 0, w, h), fill=rgb(OCEAN))
    d.polygon([(0, 0), (w * .18, 0), (w * .14, h * .62), (0, h)], fill=rgb(LAND))
    d.polygon([(w * .86, 0), (w, 0), (w, h), (w * .90, h * .72)], fill=rgb(LAND))
    d.line((w * .18, 0, w * .14, h * .62, 0, h), fill=rgb(COAST))
    d.line((w * .86, 0, w, h, w * .90, h * .72), fill=rgb(COAST))
    # Bahrain island: an industrial plant with a fresh explosion
    ix, iy = w * .22, h * .60
    d.ellipse((ix - 24, iy - 15, ix + 24, iy + 15), fill=rgb(LAND), outline=rgb(COAST))
    d.rectangle((ix - 16, iy - 3, ix - 5, iy + 8), fill="#8A857B")
    d.rectangle((ix - 3, iy - 7, ix + 9, iy + 8), fill="#9A958C")
    d.rectangle((ix + 4, iy - 17, ix + 8, iy - 7), fill="#8A857B")
    for k in range(3):
        d.ellipse((ix + 5 + k * 3, iy - 24 - k * 4, ix + 11 + k * 3, iy - 17 - k * 4), fill="#9A958C")
    bx, by = ix + 2, iy - 10
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line((bx, by, bx + 11 * math.cos(a), by + 11 * math.sin(a)), fill=RED, width=2)
    d.ellipse((bx - 5, by - 5, bx + 5, by + 5), fill="#F2C14E")
    txt(d, (ix - 20, iy + 10), "BAHRAIN", F["art_s"], INK)
    # Iranian launch site: three arrowed missiles — one at Bahrain, two at the tankers
    lx, ly = w * .88, h * .24
    d.ellipse((lx - 4, ly - 4, lx + 4, ly + 4), fill=RED)
    for tx, ty in ((bx, by), (w * .50, h * .58), (w * .70, h * .66)):
        d.line((lx, ly, tx, ty), fill=RED, width=2)
        a = math.atan2(ty - ly, tx - lx)
        for k in (-0.6, 0.6):
            d.line((tx, ty, tx - 6 * math.cos(a + k), ty - 6 * math.sin(a + k)), fill=RED, width=2)
    _ship(d, w * .50, h * .66, 1.0, True)
    _ship(d, w * .70, h * .74, .85, False)
    for cx, cy in ((w * .50, h * .58), (w * .70, h * .66)):
        d.ellipse((cx - 9, cy - 7, cx + 9, cy + 7), outline=RED, width=2)
    txt(d, (w * .04, h * .16 + 4), "SAUDI ARABIA", F["art_s"], MUTED)
    pill(d, 4, 3, "05:00 UTC · STRAIT OF HORMUZ", F["art_l"])
    tag(d, w * .66, 5, "IRAN FIRES")
    tag(d, 4, h - 16, "BAHRAIN + 2 TANKERS HIT")
    tag(d, w * .86, h - 16, "IRAN")


def s_cop(d, w, h):
    """Antalya 22:10 UTC — day 13 clock past midnight, delegates still split."""
    d.rectangle((0, 0, w, h), fill="#E8EFE3")
    for i in range(13):
        x = 6 + i * 23
        d.rectangle((x, 15, x + 18, 29), fill=RED if i == 12 else "#DDE7D6", outline=MUTED)
        txt(d, (x + 9, 22), str(9 + i), F["art_s"], "#FFFFFF" if i == 12 else INK, "mm")
    clock(d, w - 28, 50, 13, 22, 10)
    txt(d, (w - 44, 68), "22:10 UTC", F["art_s"], INK)
    d.ellipse((w * .30, h * .52, w * .72, h * .90), fill="#CFCBC0", outline=MUTED)
    for i in range(5):
        _person(d, w * .34 + i * w * .075, h * .60, 1.0,
                ["#3F6EA8", "#7D4C9E", "#3F8F4F", "#9E1F1F", "#B4674A"][i])
    d.rectangle((w * .04, h * .60, w * .25, h * .84), fill="#FFFFFF", outline=MUTED)
    d.line((w * .06, h * .66, w * .23, h * .66), fill=MUTED)
    d.line((w * .06, h * .72, w * .19, h * .72), fill=MUTED)
    pill(d, 4, 3, "22:10 UTC · ANTALYA", F["art_s"])
    tag(d, 4, h - 15, "NO TEXT · SUN 05:00 GMT")


def s_quake(d, w, h):
    """Lima 00:09 UTC — M6.7 at 108 km, epicentre ring and shaking skyline."""
    d.rectangle((0, 0, w, h * .40), fill="#DCE7EF")
    d.rectangle((0, h * .40, w, h), fill="#D9C9A7")
    d.polygon([(0, h * .42), (w * .20, h * .14), (w * .40, h * .42)], fill="#A9966F")
    d.polygon([(w * .44, h * .42), (w * .66, h * .18), (w * .84, h * .42)], fill="#A9966F")
    for i in range(6):
        x = w * .55 + i * 14
        hh = 14 + (i % 3) * 5
        d.polygon([(x, h * .50 - hh), (x + 10, h * .50 - hh + 3),
                   (x + 10, h * .50 + 2), (x, h * .50)], fill="#7A7A7A")
    ex, ey = w * .30, h * .68
    d.ellipse((ex - 3, ey - 3, ex + 3, ey + 3), fill=RED)
    for r in (10, 20, 32):
        d.arc((ex - r, ey - r, ex + r, ey + r), 210, 330, fill=RED, width=2)
    d.line((ex, ey, ex, h * .38), fill=RED)
    pill(d, ex + 16, h * .30, "108 KM", F["art_s"], "#FFFFFF", RED)
    pill(d, 4, 3, "00:09 UTC · LIMA, PERU", F["art_l"])
    tag(d, w - 88, h - 16, "USGS M6.7")
    txt(d, (4, h - 12), "NO TSUNAMI", F["art_s"], INK)


def s_ship(d, w, h):
    """Gulf of Finland 06:50 UTC — drones set the Sparta II ablaze."""
    d.rectangle((0, 0, w, h), fill="#1E3A4C")
    d.polygon([(0, h), (0, h - 16), (w * .20, h - 28), (w * .32, h)], fill="#3B4A46")
    for i in range(4):
        x = 8 + i * 12
        d.polygon([(x, h - 24), (x + 5, h - 40), (x + 10, h - 24)], fill="#2E4A3A")
    _ship(d, w * .50, h * .60, 1.15, True)
    for dx, dy in ((w * .74, h * .26), (w * .86, h * .44)):
        d.line((dx - 7, dy, dx + 7, dy), fill=INK, width=2)
        d.ellipse((dx - 2, dy - 2, dx + 2, dy + 2), fill="#D9D5CA")
        d.line((dx, dy + 2, w * .50, h * .50), fill=RED, width=1)
    pill(d, 3, 3, "06:50 UTC · GULF OF FINLAND", F["art_s"])
    tag(d, 3, h - 15, "DRONE STRIKE · 16 SAFE")


def s_capture(d, w, h):
    """Guasave 02:00 UTC — soldiers cuff El Chapo Isidro, 11 dead in exchanges."""
    d.rectangle((0, 0, w, h), fill="#263C2A")
    for i in range(10):
        d.ellipse((i * 26 - 10, -12, i * 26 + 28, 30), fill="#355239")
    _flag(d, w - 40, 5, 30, 18, ["#CE1126", "#FFFFFF", "#CE1126"])
    d.rectangle((w * .06, h * .52, w * .30, h * .78), fill="#8A857B")
    d.rectangle((w * .10, h * .56, w * .26, h * .64), fill="#4A6E8A")
    d.ellipse((w * .10, h * .74, w * .16, h * .80), fill=INK)
    d.ellipse((w * .22, h * .74, w * .28, h * .80), fill=INK)
    for sx in (w * .42, w * .52, w * .70, w * .80):
        _person(d, sx, h * .76, 1.15, "#6B705C")
    _person(d, w * .60, h * .72, 1.3, "#1F2933")
    d.line((w * .57, h * .74, w * .63, h * .74), fill="#E8B23A", width=2)
    pill(d, 3, 3, "02:00 UTC · GUASAVE, SINALOA", F["art_s"])
    tag(d, 3, h - 15, "ARREST · 11 DEAD")


def s_robot(d, w, h):
    """Geneva, 128 states — a humanoid killer robot under a red ban sign."""
    d.rectangle((0, 0, w, h), fill="#E9EEF4")
    for i in range(6):
        _flag(d, 8 + i * 15, 18, 12, 8, ["#2E5B9A"])
    d.rectangle((w * .12, h * .34, w * .50, h * .88), fill="#FFFFFF", outline=MUTED)
    for j in range(4):
        d.line((w * .15, h * .44 + j * 8, w * .47, h * .44 + j * 8), fill=MUTED)
    d.ellipse((w * .16, h * .60, w * .30, h * .80), outline=RED, width=2)
    txt(d, (w * .23, h * .70), "128", F["art_s"], RED, "mm")
    # Unmistakably a robot: antenna, head with two eyes, neck, chest panel,
    # jointed arms and jointed legs with feet.
    cx, cy, s = w * .74, h * .59, .85
    d.line((cx, cy - 22 * s, cx, cy - 32 * s), fill=INK, width=2)
    d.ellipse((cx - 2 * s, cy - 36 * s, cx + 2 * s, cy - 32 * s), fill=RED)
    d.rounded_rectangle((cx - 11 * s, cy - 22 * s, cx + 11 * s, cy - 6 * s),
                        radius=3, fill="#6C8EBF", outline=INK)
    for ex in (cx - 5 * s, cx + 5 * s):
        d.ellipse((ex - 3 * s, cy - 17 * s, ex + 3 * s, cy - 11 * s), fill="#DDE7F2")
        d.ellipse((ex - 1.5 * s, cy - 15.5 * s, ex + 1.5 * s, cy - 12.5 * s), fill=INK)
    d.line((cx - 5 * s, cy - 9 * s, cx + 5 * s, cy - 9 * s), fill=INK)
    d.rectangle((cx - 2 * s, cy - 6 * s, cx + 2 * s, cy - 2 * s), fill=INK)
    d.rounded_rectangle((cx - 12 * s, cy - 2 * s, cx + 12 * s, cy + 16 * s),
                        radius=3, fill="#8FA9C9", outline=INK)
    d.rectangle((cx - 6 * s, cy + 3 * s, cx + 6 * s, cy + 10 * s), fill="#DDE7F2", outline=INK)
    d.ellipse((cx - 1.5 * s, cy + 5 * s, cx + 1.5 * s, cy + 8 * s), fill=RED)
    for side in (-1, 1):
        d.line((cx + side * 12 * s, cy + 2 * s, cx + side * 18 * s, cy + 10 * s), fill=INK, width=3)
        d.line((cx + side * 18 * s, cy + 10 * s, cx + side * 15 * s, cy + 18 * s), fill=INK, width=3)
        d.ellipse((cx + side * 18 * s - 2 * s, cy + 8 * s,
                   cx + side * 18 * s + 2 * s, cy + 12 * s), fill="#6C8EBF")
        d.line((cx + side * 5 * s, cy + 16 * s, cx + side * 7 * s, cy + 25 * s), fill=INK, width=3)
        d.line((cx + side * 7 * s, cy + 25 * s, cx + side * 9 * s, cy + 29 * s), fill=INK, width=3)
        d.ellipse((cx + side * 9 * s - 4 * s, cy + 28 * s,
                   cx + side * 9 * s + 3 * s, cy + 31 * s), fill="#6C8EBF")
    d.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), outline=RED, width=3)
    d.line((cx - 20, cy - 20, cx + 20, cy + 20), fill=RED, width=3)
    pill(d, 3, 3, "21 NOV · GENEVA · 128 STATES", F["art_s"])
    tag(d, 3, h - 15, "BAN AUTOWEAPONS TALKS")


def s_space(d, w, h):
    """Mercury 18:24 UTC — BepiColombo's 37-minute burn after a nine-year trip."""
    d.rectangle((0, 0, w, h), fill="#101A2C")
    for i in range(30):
        x, y = (i * 47) % w, (i * 29) % h
        d.ellipse((x, y, x + 1, y + 1), fill="#FFFFFF")
    cx, cy, r = w * .74, h * .50, h * .30
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="#8C877E", outline="#CFCBC0")
    for dx, dy, rr in ((-.35, -.30, 2.5), (.05, -.40, 2), (.40, -.10, 3),
                       (-.20, .25, 2.5), (.28, .32, 2)):
        d.ellipse((cx + dx * r - rr, cy + dy * r - rr,
                   cx + dx * r + rr, cy + dy * r + rr), fill="#6E6A63")
    d.arc((w * .06, h * .06, w * .94, h * .96), 195, 345, fill="#E8B23A", width=2)
    sx, sy = w * .30, h * .34
    d.rectangle((sx - 10, sy - 3, sx + 10, sy + 3), fill="#E8B23A")
    d.rectangle((sx - 20, sy - 8, sx - 12, sy + 8), fill="#2E5B9A")
    d.rectangle((sx + 12, sy - 8, sx + 20, sy + 8), fill="#2E5B9A")
    d.polygon([(sx - 2, sy + 3), (sx + 2, sy + 3), (sx, sy + 14)], fill="#E2672A")
    d.line((sx, sy + 14, cx - r, cy), fill="#F2C14E")
    pill(d, 3, 3, "18:24 UTC · MERCURY ORBIT", F["art_s"])
    tag(d, 3, h - 15, "9-YEAR TRIP · 37-MIN BURN")


def s_jets(d, w, h):
    """Taipei, 21 jets across the median line — Taiwan scrambles."""
    d.rectangle((0, 0, w, h), fill=rgb(OCEAN))
    d.polygon([(0, 0), (w * .26, 0), (w * .22, h), (0, h)], fill=rgb(LAND))
    d.polygon([(w * .78, h * .10), (w * .92, h * .18), (w * .90, h * .70),
               (w * .80, h * .88), (w * .76, h * .55)], fill=rgb(LAND), outline=rgb(COAST))
    d.line((w * .50, 0, w * .50, h), fill=RED, width=1)
    for i in range(21):
        x = w * .30 + (i % 7) * w * .055
        y = h * .26 + (i // 7) * h * .20
        d.polygon([(x - 4, y), (x + 5, y), (x, y + 3)], fill=INK)
        d.line((x, y + 1, x - 3, y + 6), fill=INK, width=1)
    for x in (w * .66, w * .72):
        d.polygon([(x - 5, h * .68), (x + 6, h * .68), (x, h * .72)], fill="#2E5B9A")
    pill(d, 3, 3, "21 NOV · TAIPEI", F["art_s"])
    tag(d, 3, h - 15, "21 JETS CROSS MEDIAN LINE")


def s_trade(d, w, h):
    """Brussels 09:42 UTC — EU and Indonesia sign; tariffs fall 98.5%."""
    d.rectangle((0, 0, w, h), fill="#EEF0E8")
    d.rectangle((10, 18, 42, 38), fill="#2E5B9A")
    for i in range(12):
        a = 2 * math.pi * i / 12
        sx, sy = 26 + 8 * math.cos(a), 28 + 6 * math.sin(a)
        d.ellipse((sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5), fill="#F2C14E")
    _flag(d, w - 42, 10, 32, 20, ["#CE1126", "#FFFFFF"])
    d.rectangle((w * .40, h * .28, w * .64, h * .86), fill="#FFFFFF", outline=MUTED)
    for j in range(3):
        d.line((w * .43, h * .40 + j * 8, w * .61, h * .40 + j * 8), fill=MUTED)
    d.line((w * .50, h * .62, w * .60, h * .74), fill="#2E5B9A", width=2)
    for i, hg in enumerate((18, 12, 7)):
        d.rectangle((w * .70 + i * 12, h * .80 - hg, w * .70 + i * 12 + 8, h * .80), fill="#7D8C6A")
    pill(d, 3, 3, "09:42 UTC · BRUSSELS", F["art_s"])
    tag(d, 3, h - 15, "EU-INDONESIA FTA · -98.5%")


def s_rugby(d, w, h):
    """Twickenham — England 37–12 New Zealand, the record winning margin."""
    d.rectangle((0, 0, w, h), fill="#3F7A4E")
    d.line((0, h * .28, w, h * .28), fill="#FFFFFF")
    d.line((w * .80, 4, w * .80, h * .62), fill="#FFFFFF", width=2)
    d.line((w * .72, h * .28, w * .88, h * .28), fill="#FFFFFF", width=2)
    d.ellipse((w * .38, h * .42, w * .50, h * .62), fill="#8A5A2B", outline="#FFFFFF")
    for x, c in ((w * .16, "#FFFFFF"), (w * .28, "#1B1B1B"), (w * .60, "#FFFFFF")):
        _person(d, x, h * .55, 1.5, c)
    d.rectangle((w * .06, h * .04, w * .58, h * .22), fill=INK)
    txt(d, (w * .32, h * .13), "ENG 37-12 NZL", F["art_s"], "#FFFFFF", "mm")
    pill(d, 3, h - 15, "TWICKENHAM · RECORD MARGIN", F["art_s"])


def s_crypto(d, w, h):
    """New York 20:00 UTC — $55,100 low, then an 8% same-day rebound."""
    d.rectangle((0, 0, w, h), fill="#1C2431")
    pts = [(6, 26), (38, 30), (66, 22), (92, 46), (118, 56), (146, 32), (176, 24), (w - 6, 18)]
    d.line(pts, fill="#E2672A", width=2)
    d.ellipse((w * .44, 18, w * .55, 40), fill="#E8B23A", outline="#FFFFFF")
    txt(d, (w * .495, 29), "B", F["art_l"], "#7A4E12", "mm")
    d.polygon([(104, 40), (114, 50), (94, 50)], fill="#E2672A")
    d.polygon([(170, 32), (180, 20), (160, 24)], fill="#5FA777")
    pill(d, 3, 3, "20:00 UTC · NEW YORK", F["art_s"])
    tag(d, 3, h - 15, "$55,100 LOW · +8% REBOUND")


SCENES = {
    "gulf": s_gulf, "cop": s_cop, "quake": s_quake, "ship": s_ship,
    "capture": s_capture, "robot": s_robot, "space": s_space, "jets": s_jets,
    "trade": s_trade, "rugby": s_rugby, "crypto": s_crypto,
}


def art(scene, w, h):
    im = Image.new("RGB", (w, h), rgb(PAPER))
    SCENES[scene](ImageDraw.Draw(im), w, h)
    return im


# --------------------------------------------------------------------------
# Map helpers
# --------------------------------------------------------------------------
def px_lon(lon):
    return 324 + (lon + 180) / 360 * 376


def py_lat(lat):
    return 756 + (83 - lat) / 141 * 188


def load_world():
    path = os.path.join(BASE, "world110.geojson")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def draw_world(d):
    d.rectangle((324, 756, 700, 944), fill=rgb(OCEAN))
    for lon in range(-180, 181, 30):
        x = px_lon(lon)
        d.line((x, 756, x, 944), fill=rgb(GRAT))
    for lat in range(-60, 84, 30):
        y = py_lat(lat)
        d.line((324, y, 700, y), fill=rgb(GRAT))
    gj = load_world()
    for feat in gj["features"]:
        props = feat.get("properties", {})
        name = props.get("NAME") or props.get("name") or ""
        if "Antarctica" in name:
            continue
        geom = feat["geometry"]
        polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
        for poly in polys:
            for ring in poly:
                pts = [(px_lon(lo), py_lat(la)) for lo, la in ring]
                if len(pts) > 2:
                    d.polygon(pts, fill=rgb(LAND))
                    d.line(pts + [pts[0]], fill=rgb(COAST), width=1)


def arrow(d, x0, y0, x1, y1, fill):
    d.line((x0, y0, x1, y1), fill=fill, width=1)
    a = math.atan2(y1 - y0, x1 - x0)
    for k in (-0.5, 0.5):
        d.line((x1, y1, x1 - 5 * math.cos(a + k), y1 - 5 * math.sin(a + k)), fill=fill, width=1)


def place_badges(d, stories):
    placed = []
    for s in stories:
        dx, dy = px_lon(s["lon"]), py_lat(s["lat"])
        c = rgb(REGION_COLORS[s["region"] - 1])
        d.ellipse((dx - 3, dy - 3, dx + 3, dy + 3), fill=c, outline="#FFFFFF", width=1)
        best = None
        for rad in (0, 8, 15, 23, 32, 42):
            for k in range(8):
                a = 2 * math.pi * k / 8
                bx, by = dx + rad * math.cos(a), dy + rad * math.sin(a)
                if not (328 < bx < 696 and 760 < by < 940):
                    continue
                if all(math.hypot(bx - qx, by - qy) >= 12 for qx, qy in placed):
                    best = (bx, by)
                    break
            if best:
                break
        if not best:
            best = (dx, dy)
        bx, by = best
        placed.append((bx, by))
        if math.hypot(dx - bx, dy - by) > 4:
            arrow(d, dx, dy, bx, by, c)
        d.ellipse((bx - 6, by - 6, bx + 6, by + 6), fill=c, outline="#FFFFFF", width=2)
        txt(d, (bx, by), str(s["n"]), F["num"], "#FFFFFF", "mm")


def draw_legend(d):
    x = 330
    step = 52
    for i, name in enumerate(REGION_NAMES):
        cx = x + i * step
        d.ellipse((cx, 953, cx + 7, 960), fill=rgb(REGION_COLORS[i]))
        txt(d, (cx + 10, 956), name[:9], F["leg"], INK, "lm")


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------
def draw_header(d):
    d.rectangle((0, 0, 1024, 24), fill=rgb(RED))
    txt(d, (12, 12), "THE WORLD IN ONE DAY", F["lab"], "#FFFFFF", "lm")
    txt(d, (512, 12), "DAY 325 OF 2026", F["lab"], "#FFFFFF", "mm")
    txt(d, (1012, 12), "ALL TIME UTC", F["lab"], "#FFFFFF", "rm")
    txt(d, (512, 62), "Saturday 21 November 2026", F["mast"], rgb(INK), "mm")
    txt(d, (512, 113), DECK, F["deck"], rgb(MUTED), "mm")
    d.line((12, 126, 1012, 126), fill=rgb(LINE), width=1)
    for i, (num, cap) in enumerate(STATS):
        sx = 12 + i * 142
        d.line((sx, 130, sx, 170), fill=rgb(LINE))
        txt(d, (sx + 71, 143), num, F["stat"], rgb(RED), "mm")
        txt(d, (sx + 71, 164), cap, F["cap"], rgb(INK), "mm")
    for i, name in enumerate(REGION_NAMES):
        bx = 12 + i * 142
        d.rectangle((bx, 173, bx + 140, 192), fill=rgb(REGION_COLORS[i]))
        txt(d, (bx + 6, 182.5), name, F["rgn"], "#FFFFFF", "lm")


def draw_main_cards(im, d):
    for i, s in enumerate([x for x in STORIES if x["size"] == "main"]):
        x = 12 + i * 336
        d.rectangle((x, 198, x + 326, 391), fill=rgb(CARD), outline=rgb(LINE))
        a = art(s["scene"], 320, 90)
        im.paste(a, (x + 3, 201))
        d.rectangle((x + 3, 293, x + 323, 307), fill=rgb(REGION_COLORS[s["region"] - 1]))
        rrect(d, (x + 7, 293, x + 21, 307), 3, fill="#FFFFFF")
        txt(d, (x + 14, 300), str(s["n"]), F["num"], rgb(REGION_COLORS[s["region"] - 1]), "mm")
        sw = d.textlength(s["source"], font=F["ms"])
        txt(d, (x + 26, 302), fit(d, s["kicker"], F["mk"], 281 - sw), F["mk"], "#FFFFFF", "lm")
        txt(d, (x + 315, 302), s["source"], F["ms"], "#FFFFFF", "rm")
        lines = wrap(d, s["headline"], F["mh"], 312)[:2]
        for j, ln in enumerate(lines):
            txt(d, (x + 7, 310 + j * 21), fit(d, ln, F["mh"], 312), F["mh"], rgb(INK))
        bl = wrap(d, s["body"], F["mb"], 312)[:2]
        for j, ln in enumerate(bl):
            txt(d, (x + 7, 350 + j * 12), fit(d, ln, F["mb"], 312), F["mb"], rgb(MUTED))
        chip(d, x + 250, 377, s["status"])


def draw_small_cards(im, d):
    for i, s in enumerate([x for x in STORIES if x["size"] == "small"]):
        col, row = i % 4, i // 4
        x, y = 12 + col * 252, 395 + row * 166
        d.rectangle((x, y, x + 244, y + 160), fill=rgb(CARD), outline=rgb(LINE))
        a = art(s["scene"], 238, 80)
        im.paste(a, (x + 3, y + 4))
        d.rectangle((x + 3, y + 86, x + 241, y + 100), fill=rgb(REGION_COLORS[s["region"] - 1]))
        rrect(d, (x + 7, y + 86, x + 21, y + 100), 3, fill="#FFFFFF")
        txt(d, (x + 14, y + 93), str(s["n"]), F["num"], rgb(REGION_COLORS[s["region"] - 1]), "mm")
        sw = d.textlength(s["source"], font=F["ss"])
        txt(d, (x + 26, y + 93), fit(d, s["kicker"], F["sk"], 203 - sw), F["sk"], "#FFFFFF", "lm")
        txt(d, (x + 235, y + 93), s["source"], F["ss"], "#FFFFFF", "rm")
        hl = wrap(d, s["headline"], F["sh"], 232)[:2]
        for j, ln in enumerate(hl):
            txt(d, (x + 6, y + 103 + j * 12), fit(d, ln, F["sh"], 232), F["sh"], rgb(INK))
        bl = wrap(d, s["brief"], F["sb"], 232)[:2]
        for j, ln in enumerate(bl):
            txt(d, (x + 6, y + 129 + j * 9), fit(d, ln, F["sb"], 232), F["sb"], rgb(MUTED))
        chip(d, x + 174, y + 147, s["status"])


def draw_lists(d):
    briefs = [x for x in STORIES if x["size"] == "brief"]
    left = [x for x in briefs if x["region"] in (1, 3, 5)]
    right = [x for x in briefs if x["region"] in (2, 4, 6)]
    rows = {}
    for side, items, x0, x1 in (("L", left, 12, 312), ("R", right, 712, 1012)):
        top = 720 + 31
        step = (970 - top - 10) // len(items)
        for i, s in enumerate(items):
            cy = top + i * step
            rows[s["n"]] = ("L" if side == "L" else "R", cy + 7)
            rrect(d, (x0 + 6, cy - 3, x1 - 6, cy + step - 4), 3, fill=rgb(BUTTON), outline=rgb(LINE))
            bx = x0 + 20
            rrect(d, (bx - 10, cy - 2, bx + 10, cy + 14), 3, fill=rgb(REGION_COLORS[s["region"] - 1]), outline="#FFFFFF")
            txt(d, (bx, cy + 5), str(s["n"]), F["num"], "#FFFFFF", "mm")
            tx = x0 + 40
            hl = wrap(d, s["brief"], F["lh"], 174)[:2]
            for j, ln in enumerate(hl):
                txt(d, (tx, cy + j * 8), fit(d, ln, F["lh"], 174), F["lh"], rgb(INK))
            txt(d, (x1 - 10, cy + 7), s["source"], F["ls"], rgb(MUTED), "rm")
    return rows


def draw_date_check(d):
    d.rectangle((12, 974, 1012, 1002), fill="#FBF6EE", outline=rgb(RED))
    d.rectangle((18, 977, 68, 999), fill=rgb(RED))
    txt(d, (43, 984), "DATE", F["idx"], "#FFFFFF", "mm")
    txt(d, (43, 994), "CHECK", F["idx"], "#FFFFFF", "mm")
    txt(d, (76, 978), fit(d, DATE_LINE_1, F["date"], 928), F["date"], rgb(INK))
    txt(d, (76, 990), fit(d, DATE_LINE_2, F["date"], 928), F["date"], rgb(INK))
    txt(d, (1012, 1011), SOURCE_LINE, F["src"], rgb(INK), "rm")


def build():
    im = Image.new("RGB", (1024, 1024), rgb(PAPER))
    d = ImageDraw.Draw(im)
    draw_header(d)
    draw_main_cards(im, d)
    draw_small_cards(im, d)

    rrect(d, (12, 722, 1012, 972), 4, fill=rgb(PANEL), outline=rgb(LINE), width=1)
    d.rectangle((20, 724, 94, 738), fill=rgb(RED))
    txt(d, (57, 731), "INDEX", F["idx"], "#FFFFFF", "mm")
    txt(d, (102, 731), "ALSO ON SATURDAY 21 NOVEMBER — 24 MORE STORIES, RANKED BY CONSEQUENCE",
        F["lab"], rgb(INK), "lm")
    d.line((12, 742, 1012, 742), fill=rgb(LINE))
    rrect(d, (316, 748, 708, 968), 6, outline=rgb(LINE), width=1)

    draw_world(d)
    mapped = [s for s in STORIES if s["size"] in ("main", "small")]
    place_badges(d, mapped)
    draw_legend(d)

    briefs = [s for s in STORIES if s["size"] == "brief"]
    left = [s for s in briefs if s["region"] in (1, 3, 5)]
    right = [s for s in briefs if s["region"] in (2, 4, 6)]
    link_rows = {}
    for side, items, x0, x1 in (("L", left, 12, 312), ("R", right, 712, 1012)):
        top = 751
        step = (970 - top - 10) // len(items)
        for i, s in enumerate(items):
            link_rows[s["n"]] = ((306 if side == "L" else 718), top + i * step + 7)
    for s in briefs:
        dx, dy = px_lon(s["lon"]), py_lat(s["lat"])
        c = lighten(REGION_COLORS[s["region"] - 1], 0.62)
        d.ellipse((dx - 2, dy - 2, dx + 2, dy + 2), fill=rgb(REGION_COLORS[s["region"] - 1]), outline="#FFFFFF")
        tx, ty = link_rows[s["n"]]
        if abs(dx - tx) > 2:
            arrow(d, dx, dy, tx, ty, c)

    draw_lists(d)
    draw_date_check(d)
    return im


if __name__ == "__main__":
    out = os.environ.get("ENTRY_OUT", os.path.join(BASE, "entry.png"))
    img = build()
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes", img.size)
