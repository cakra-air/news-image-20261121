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
    "num": face("arialbd.ttf", 8),
    "lh": face("arial.ttf", 8),
    "ls": face("arial.ttf", 6),
    "leg": face("arial.ttf", 6),
    "idx": face("arialbd.ttf", 8),
    "lab": face("arialbd.ttf", 9),
    "date": face("arial.ttf", 7),
    "src": face("arial.ttf", 8),
    "art_l": face("arialbd.ttf", 8),
    "art_s": face("arialbd.ttf", 7),
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
# Original vector illustrations
# --------------------------------------------------------------------------
def _ship(d, x, y, s=1.0, fire=False):
    d.polygon([(x - 15 * s, y), (x + 15 * s, y), (x + 11 * s, y + 7 * s), (x - 11 * s, y + 7 * s)], fill=INK)
    d.rectangle((x - 7 * s, y - 7 * s, x + 4 * s, y), fill="#CFCBC0")
    d.rectangle((x + 5 * s, y - 4 * s, x + 9 * s, y), fill="#8A857B")
    if fire:
        d.polygon([(x - 4 * s, y - 7 * s), (x, y - 17 * s), (x + 4 * s, y - 7 * s)], fill="#E2672A")
        d.polygon([(x - 2 * s, y - 7 * s), (x, y - 13 * s), (x + 2 * s, y - 7 * s)], fill="#F2C14E")
        for k in range(3):
            d.ellipse((x + 6 * s + k * 4 * s, y - 16 * s - k * 3 * s,
                       x + 12 * s + k * 4 * s, y - 10 * s - k * 3 * s), fill="#9A958C")


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
    d.rectangle((0, 0, w, h), fill=rgb(OCEAN))
    d.polygon([(0, 0), (w * .22, 0), (w * .17, h * .62), (0, h)], fill=rgb(LAND))
    d.polygon([(w * .80, 0), (w, 0), (w, h), (w * .87, h * .7)], fill=rgb(LAND))
    d.ellipse((w * .36, h * .50, w * .45, h * .72), fill=rgb(LAND), outline=rgb(COAST))
    _ship(d, w * .57, h * .34, 1.0, True)
    _ship(d, w * .68, h * .58, .8, False)
    for ex, ey in ((w * .55, h * .44), (w * .70, h * .72)):
        d.line((w * .44, h * .60, ex, ey), fill=RED, width=1)
        d.ellipse((ex - 2, ey - 2, ex + 2, ey + 2), fill=RED)
    d.ellipse((w * .40, h * .55, w * .47, h * .67), outline=RED, width=2)
    txt(d, (5, 4), "05:00 UTC  ·  STRAIT OF HORMUZ", F["art_l"], INK)
    txt(d, (w - 4, h - 10), "SAUDI ARABIA        IRAN", F["art_s"], MUTED, "ra")


def s_cop(d, w, h):
    d.rectangle((0, 0, w, h), fill="#E8EFE3")
    for i in range(13):
        x = 8 + i * 13
        fill = "#DDE7D6" if i < 12 else RED
        d.rectangle((x, 16, x + 10, 30), fill=fill, outline=MUTED)
    txt(d, (8, 6), "NOVEMBER 2026 · DAY 13 → 21", F["art_s"], INK)
    d.rectangle((w - 30, 12, w - 22, 48), fill="#FFFFFF", outline=MUTED)
    d.rectangle((w - 28, 30, w - 24, 46), fill=RED)
    d.ellipse((w - 32, 8, w - 20, 20), fill=RED)
    for i in range(3):
        x = 16 + i * 26
        d.rectangle((x, h - 26, x + 16, h - 8), fill="#9C8A64")
        d.line((x, h - 26, x + 16, h - 8), fill=RED, width=2)
    d.rectangle((w * .48, h - 30, w * .78, h - 8), fill="#CFCBC0")
    for i in range(4):
        _person(d, w * .52 + i * 18, h - 14, 1.0, ["#3F6EA8", "#7D4C9E", "#3F8F4F", "#9E1F1F"][i])
    txt(d, (5, h - 10), "22:10 UTC  ·  ANTALYA", F["art_s"], INK)


def s_quake(d, w, h):
    d.rectangle((0, 0, w, h * .42), fill="#DCE7EF")
    d.rectangle((0, h * .42, w, h), fill="#D9C9A7")
    d.polygon([(0, h * .45), (w * .25, h * .16), (w * .45, h * .45)], fill="#A9966F")
    d.polygon([(w * .50, h * .45), (w * .72, h * .20), (w, h * .45)], fill="#A9966F")
    ex, ey = w * .52, h * .78
    d.ellipse((ex - 4, ey - 4, ex + 4, ey + 4), fill=RED)
    for r in (12, 24, 38):
        d.arc((ex - r, ey - r, ex + r, ey + r), 200, 340, fill=RED, width=2)
    for i in range(5):
        x = w * .62 + i * 10
        d.rectangle((x, h * .40 - (i % 2) * 8, x + 6, h * .50), fill="#7A7A7A")
    txt(d, (5, 4), "00:09 UTC  ·  USGS M6.7  ·  108 KM", F["art_l"], INK)


def s_ship(d, w, h):
    d.rectangle((0, 0, w, h), fill="#1E3A4C")
    d.polygon([(0, h), (0, h - 20), (w * .22, h - 32), (w * .34, h)], fill="#3B4A46")
    _ship(d, w * .55, h * .56, 1.35, True)
    d.polygon((w * .80, 16, w * .86, 20, w * .83, 26, w * .77, 22), fill="#D9D5CA")
    d.line((w * .83, 22, w * .70, h * .42), fill=RED, width=1)
    txt(d, (5, 4), "06:50 UTC  ·  GULF OF FINLAND", F["art_s"], "#FFFFFF")


def s_capture(d, w, h):
    d.rectangle((0, 0, w, h), fill="#263C2A")
    for i in range(9):
        x = i * 28
        d.ellipse((x, -10, x + 36, 34), fill="#355239")
    _flag(d, w - 34, 6, 26, 16, ["#CE1126", "#FFFFFF", "#CE1126"])
    for i, sx in enumerate((w * .40, w * .52, w * .64)):
        _person(d, sx, h * .78, 1.2, "#6B705C")
    _person(d, w * .55, h * .70, 1.3, "#1F2933")
    d.rectangle((w * .51, h * .74, w * .59, h * .78), outline="#E8B23A", width=2)
    txt(d, (5, 4), "02:00 UTC  ·  GUASAVE, SINALOA", F["art_s"], "#FFFFFF")


def s_robot(d, w, h):
    d.rectangle((0, 0, w, h), fill="#E9EEF4")
    for i in range(6):
        _flag(d, 10 + i * 16, 8, 12, 8, ["#2E5B9A", "#F2C14E", "#C0392B"][:1 + i % 3])
    d.rectangle((w * .18, h * .38, w * .48, h * .88), fill="#FFFFFF", outline=MUTED)
    for j in range(4):
        d.line((w * .21, h * .48 + j * 9, w * .44, h * .48 + j * 9), fill=MUTED)
    d.rectangle((w * .58, h * .32, w * .80, h * .82), fill="#6C8EBF", outline=INK)
    d.ellipse((w * .62, h * .40, w * .76, h * .54), fill="#DDE7F2")
    d.ellipse((w * .655, h * .45, w * .67, h * .465), fill=INK)
    d.ellipse((w * .715, h * .45, w * .73, h * .465), fill=INK)
    d.ellipse((w * .82, h * .20, w * .96, h * .52), outline=RED, width=3)
    d.line((w * .84, h * .22, w * .94, h * .50), fill=RED, width=3)
    txt(d, (5, h - 10), "GENEVA · 128 STATES", F["art_s"], INK)


def s_space(d, w, h):
    d.rectangle((0, 0, w, h), fill="#101A2C")
    for i in range(24):
        x = (i * 47) % w
        y = (i * 29) % h
        d.ellipse((x, y, x + 1, y + 1), fill="#FFFFFF")
    cx, cy, r = w * .72, h * .52, h * .26
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="#8C877E", outline="#CFCBC0")
    for i in range(4):
        d.ellipse((cx - r * .7 + i * 7, cy - r * .4, cx - r * .5 + i * 7, cy - r * .2), fill="#6E6A63")
    d.arc((w * .10, h * .10, w * .90, h * .90), 200, 350, fill="#E8B23A", width=1)
    sx, sy = w * .28, h * .34
    d.rectangle((sx - 10, sy - 3, sx + 10, sy + 3), fill="#E8B23A")
    d.rectangle((sx - 18, sy - 7, sx - 11, sy + 7), fill="#2E5B9A")
    d.rectangle((sx + 11, sy - 7, sx + 18, sy + 7), fill="#2E5B9A")
    d.polygon([(sx - 2, sy + 3), (sx + 2, sy + 3), (sx, sy + 13)], fill="#E2672A")
    d.line((sx, sy + 13, cx - r, cy), fill="#F2C14E")
    txt(d, (5, 4), "18:24 UTC  ·  37-MIN BURN", F["art_s"], "#FFFFFF")


def s_jets(d, w, h):
    d.rectangle((0, 0, w, h), fill=rgb(OCEAN))
    d.polygon([(0, 0), (w * .30, 0), (w * .26, h), (0, h)], fill=rgb(LAND))
    d.polygon([(w * .72, 0), (w, 0), (w, h), (w * .76, h)], fill=rgb(LAND))
    d.line((w * .50, 0, w * .50, h), fill=RED, width=1)
    for i in range(5):
        x, y = w * .42 + i * 16, h * .25 + (i % 2) * 22
        d.polygon([(x - 5, y), (x + 6, y), (x, y + 3)], fill=INK)
        d.line((x, y + 1, x - 3, y + 7), fill=INK, width=1)
    txt(d, (5, 4), "21 JETS  ·  MEDIAN LINE", F["art_s"], INK)


def s_trade(d, w, h):
    d.rectangle((0, 0, w, h), fill="#EEF0E8")
    _flag(d, 12, 12, 34, 22, ["#2E5B9A"] + ["#F2C14E"] * 12, vertical=False)
    for i in range(12):
        a = 2 * math.pi * i / 12
        d.ellipse((12 + 17 + 8 * math.cos(a) - 1.5, 23 + 8 * math.sin(a) - 1.5,
                   12 + 17 + 8 * math.cos(a) + 1.5, 23 + 8 * math.sin(a) + 1.5), fill="#F2C14E")
    _flag(d, w - 48, 12, 34, 22, ["#CE1126", "#FFFFFF"])
    d.rectangle((w * .40, h * .30, w * .62, h * .84), fill="#FFFFFF", outline=MUTED)
    d.line((w * .45, h * .45, w * .57, h * .45), fill=INK, width=2)
    d.line((w * .45, h * .55, w * .57, h * .55), fill=INK, width=2)
    for i in range(5):
        d.rectangle((12 + i * 13, h - 16, 22 + i * 13, h - 6), fill=["#5B7FA6", "#B4674A", "#7D8C6A"][i % 3])
    txt(d, (5, 4), "09:42 UTC  ·  TARIFFS −98.5%", F["art_s"], INK)


def s_rugby(d, w, h):
    d.rectangle((0, 0, w, h), fill="#3F7A4E")
    d.line((0, h * .25, w, h * .25), fill="#FFFFFF")
    d.line((w * .80, 6, w * .80, h * .60), fill="#FFFFFF", width=2)
    d.line((w * .72, h * .30, w * .88, h * .30), fill="#FFFFFF", width=2)
    d.ellipse((w * .38, h * .42, w * .50, h * .62), fill="#8A5A2B", outline="#FFFFFF")
    _person(d, w * .18, h * .70, 1.5, "#FFFFFF")
    _person(d, w * .30, h * .64, 1.5, "#1B1B1B")
    txt(d, (5, 4), "TWICKENHAM · 37–12", F["art_s"], "#FFFFFF")


def s_crypto(d, w, h):
    d.rectangle((0, 0, w, h), fill="#1C2431")
    pts = [(8, 26), (40, 30), (70, 22), (95, 48), (120, 56), (150, 30), (180, 24), (w - 8, 18)]
    d.line(pts, fill="#E2672A", width=2)
    d.ellipse((w * .44, 18, w * .55, 40), fill="#E8B23A", outline="#FFFFFF")
    txt(d, (w * .495, 29), "B", F["art_l"], "#7A4E12", "mm")
    d.polygon([(104, 40), (114, 50), (94, 50)], fill="#E2672A")
    d.polygon([(170, 32), (180, 20), (160, 24)], fill="#5FA777")
    txt(d, (5, h - 10), "$55,100 LOW  ·  +8% REBOUND", F["art_s"], "#FFFFFF")


SCENES = {
    "gulf": s_gulf, "cop": s_cop, "quake": s_quake, "ship": s_ship,
    "capture": s_capture, "robot": s_robot, "space": s_space, "jets": s_jets,
    "trade": s_trade, "rugby": s_rugby, "crypto": s_crypto,
}


def art(scene, w, h):
    im = Image.new("RGB", (w, h), rgb(PAPER))
    d = ImageDraw.Draw(im)
    SCENES[scene](d, w, h)
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
        d.rectangle((x, 198, x + 326, 386), fill=rgb(CARD), outline=rgb(LINE))
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
            txt(d, (x + 7, 346 + j * 13), fit(d, ln, F["mb"], 312), F["mb"], rgb(MUTED))
        chip(d, x + 250, 372, s["status"])


def draw_small_cards(im, d):
    for i, s in enumerate([x for x in STORIES if x["size"] == "small"]):
        col, row = i % 4, i // 4
        x, y = 12 + col * 252, 390 + row * 166
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
            txt(d, (x + 6, y + 104 + j * 10), fit(d, ln, F["sh"], 232), F["sh"], rgb(INK))
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
            rrect(d, (bx - 10, cy - 2, bx + 10, cy + 16), 3, fill=rgb(REGION_COLORS[s["region"] - 1]), outline="#FFFFFF")
            txt(d, (bx, cy + 7), str(s["n"]), F["num"], "#FFFFFF", "mm")
            tx = x0 + 40
            hl = wrap(d, s["brief"], F["lh"], 174)[:2]
            for j, ln in enumerate(hl):
                txt(d, (tx, cy + 1 + j * 9), fit(d, ln, F["lh"], 174), F["lh"], rgb(INK))
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

    rrect(d, (12, 720, 1012, 970), 4, fill=rgb(PANEL), outline=rgb(LINE), width=1)
    d.rectangle((20, 724, 94, 738), fill=rgb(RED))
    txt(d, (57, 731), "INDEX", F["idx"], "#FFFFFF", "mm")
    txt(d, (102, 731), "ALSO ON SATURDAY 21 NOVEMBER — 26 MORE STORIES, RANKED BY CONSEQUENCE",
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
