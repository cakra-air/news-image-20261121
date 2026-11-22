"""Draw the 21 November 2026 world-news front page.

Everything here is drawn from primitives: no photographs, no downloaded art.
The only external data is world110.geojson for the coastline.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

from stories import STORIES, DATE_CHECK, SOURCES_LINE, REGIONS, REGION_COLORS

W = H = 1024
PAPER = "#F7F2E7"
INK = "#181818"
RED = "#9E1F1F"
MUTED = "#6C6459"
LINE = "#CBBB9C"
CARD = "#FDFBF4"
OCEAN = "#D8E8F1"
LAND = "#EADCB9"
COAST = "#B8A175"
GRAT = "#C6DEEA"

FONT_DIR = r"C:\Windows\Fonts"

# Filled by map_panel so the audit can check spacing and offsets exactly.
MAP_PLACEMENTS = []


def font(size, bold=False, serif=False):
    if serif:
        name = "georgiab.ttf" if bold else "georgia.ttf"
    else:
        name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def rgb(hexstr):
    h = hexstr.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def wrap(text, fnt, maxw, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def put(d, xy, text, fnt, fill=INK, anchor=None):
    d.text(xy, text, font=fnt, fill=rgb(fill) if isinstance(fill, str) else fill, anchor=anchor)


def badge(d, cx, cy, n, color, r=7, fsize=10):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb(color), outline=(255, 255, 255), width=2)
    put(d, (cx, cy + 0.5), str(n), font(fsize, True), "#FFFFFF", anchor="mm")


def chip(d, x, y, text, fill="#E7DFCC", fsize=8):
    f = font(fsize, True)
    w = d.textlength(text, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=rgb(fill), outline=rgb(LINE))
    put(d, (x + 5, y + 6.5), text, f, INK, anchor="lm")


# ---------------------------------------------------------------------------
# vignettes. Each one carries a place tag and a time tag inside the drawing.
# ---------------------------------------------------------------------------
def scene(d, box, s):
    x0, y0, x1, y1 = box
    col = rgb(REGION_COLORS[s["region"]])
    d.rectangle(box, fill="#E8EEF1" if s["scene"] not in ("missiles", "quake") else "#1F2A3A")
    light = s["scene"] in ("missiles", "quake")
    ink = "#F2F2EE" if light else INK

    if s["scene"] == "cop":
        cx, cy = x0 + 38, y0 + 44
        d.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], outline=col, width=2)
        for k in range(-18, 19, 9):
            d.arc([cx - 25, cy - 25, cx + 25, cy + 25], 0, 360, fill=rgb(GRAT))
            d.line([cx + k * 1.4, cy - 24, cx + k * 1.4, cy + 24], fill=rgb(GRAT), width=1)
        d.line([cx - 24, cy, cx + 24, cy], fill=rgb(GRAT), width=1)
        d.rounded_rectangle([x0 + 74, y0 + 20, x1 - 8, y0 + 66], radius=3,
                            fill="#FFFDF7", outline=rgb(LINE))
        put(d, (x0 + 80, y0 + 28), "DRAFT 3", font(10, True), INK)
        put(d, (x0 + 80, y0 + 43), "no deal", font(9), MUTED)
        d.rounded_rectangle([x1 - 62, y0 + 46, x1 - 10, y0 + 70], radius=3, fill=rgb(RED))
        put(d, (x1 - 36, y0 + 58), "OVERTIME", font(9, True), "#FFFFFF", anchor="mm")

    elif s["scene"] == "missiles":
        for bx in range(x0 + 8, x1 - 8, 18):
            h = 14 + (bx % 5) * 5
            d.rectangle([bx, y1 - 10 - h, bx + 12, y1 - 10], fill="#33445C")
            for wy in range(y1 - 8 - h, y1 - 12, 6):
                d.rectangle([bx + 2, wy, bx + 4, wy + 2], fill="#E8B84B")
        for i in range(3):
            sx = x0 + 18 + i * 26
            d.line([sx, y1 - 12, sx + 22, y0 + 16], fill="#F2C14E", width=2)
            d.ellipse([sx + 18, y0 + 12, sx + 26, y0 + 20], fill="#F2A03D")
        put(d, (x0 + 8, y0 + 6), "03:00", font(9, True), "#F2F2EE")

    elif s["scene"] == "quake":
        d.polygon([(x0, y1), (x0 + 40, y0 + 42), (x0 + 76, y1),
                   (x0 + 112, y0 + 50), (x1, y1)], fill="#6B5B42")
        pts = []
        for i in range(0, int(x1 - x0), 4):
            amp = 16 if 60 < i < 100 else 2
            yy = y0 + 44 + (amp if (i // 4) % 2 == 0 else -amp)
            pts.append((x0 + i, yy))
        d.line(pts, fill=rgb(RED), width=2)
        for hx in (x0 + 32, x0 + 118):
            d.rectangle([hx, y1 - 16, hx + 20, y1], fill="#EADCB9", outline="#3A3026")
            d.polygon([(hx - 2, y1 - 16), (hx + 10, y1 - 24), (hx + 22, y1 - 16)], fill=rgb(RED))
        put(d, (x0 + 8, y0 + 6), "00:09 UTC · 108 km", font(9, True), "#F2F2EE")

    elif s["scene"] == "bridge":
        d.line([x0, y0 + 62, x1, y0 + 62], fill="#5C5C5C", width=3)
        for i in range(4):
            px = x0 + 18 + i * 24
            d.line([px, y0 + 62, px, y0 + 28], fill="#5C5C5C", width=2)
            d.ellipse([px - 3, y0 + 22, px + 3, y0 + 28], fill=rgb(RED))
        d.polygon([(x0 + 52, y0 + 8), (x0 + 58, y0 + 22), (x0 + 46, y0 + 22)], fill=rgb(RED))
        put(d, (x0 + 6, y0 + 4), "DOUBLE TAP", font(8, True), INK)

    elif s["scene"] == "uranium":
        d.ellipse([x0 + 22, y0 + 22, x0 + 62, y0 + 62], outline=col, width=3)
        d.ellipse([x0 + 32, y0 + 32, x0 + 52, y0 + 52], fill=col)
        d.line([x0 + 42, y0 + 10, x0 + 42, y0 + 22], fill=col, width=3)
        put(d, (x0 + 6, y0 + 66), "STAYS IN IRAN", font(8, True), INK)

    elif s["scene"] == "tax":
        for i in range(3):
            bx = x0 + 10 + i * 26
            d.rectangle([bx, y0 + 30, bx + 20, y1 - 8], fill="#4A5A6A")
            for wy in (y0 + 36, y0 + 46, y0 + 56):
                d.rectangle([bx + 3, wy, bx + 8, wy + 3], fill="#D9E2EA")
        d.ellipse([x1 - 58, y0 + 12, x1 - 12, y0 + 58], outline=rgb(RED), width=3)
        put(d, (x1 - 35, y0 + 35), "%", font(22, True), rgb(RED), anchor="mm")

    elif s["scene"] == "flags":
        d.rectangle([x0 + 12, y0 + 16, x0 + 44, y0 + 56], fill=rgb(RED))
        d.ellipse([x0 + 18, y0 + 24, x0 + 28, y0 + 34], fill="#F2C14E")
        d.rectangle([x1 - 46, y0 + 16, x1 - 14, y0 + 56], fill="#FFFFFF", outline="#B0B0B0")
        d.ellipse([x1 - 34, y0 + 26, x1 - 22, y0 + 38], fill=rgb(RED))
        put(d, ((x0 + x1) // 2, y0 + 64), "RETRACT", font(8, True), INK, anchor="mm")

    elif s["scene"] == "btc":
        pts = [(x0 + 8, y0 + 56), (x0 + 28, y0 + 30), (x0 + 48, y0 + 42),
               (x0 + 70, y0 + 18), (x0 + 96, y0 + 34), (x1 - 8, y0 + 12)]
        d.line(pts, fill=rgb(RED), width=3)
        d.rectangle([x0 + 4, y0 + 2, x0 + 62, y0 + 13], fill="#E8EEF1")
        put(d, (x0 + 6, y0 + 4), "BTC $60,000", font(8, True), INK)

    elif s["scene"] == "robot":
        d.rounded_rectangle([x0 + 30, y0 + 18, x0 + 66, y0 + 58], radius=6, outline=col, width=3)
        d.ellipse([x0 + 40, y0 + 30, x0 + 45, y0 + 35], fill=col)
        d.ellipse([x0 + 52, y0 + 30, x0 + 57, y0 + 35], fill=col)
        put(d, (x0 + 6, y0 + 4), "2028", font(13, True), INK)
        put(d, (x0 + 6, y0 + 62), "no ban yet", font(8), MUTED)

    elif s["scene"] == "cricket":
        d.line([x0 + 14, y1 - 16, x0 + 58, y0 + 24], fill="#8A6A3C", width=5)
        d.ellipse([x0 + 52, y0 + 18, x0 + 64, y0 + 30], fill=rgb(RED))
        d.rounded_rectangle([x1 - 70, y0 + 14, x1 - 8, y0 + 54], radius=3, fill="#2E3A46")
        put(d, (x1 - 39, y0 + 34), "136", font(18, True), "#FFFFFF", anchor="mm")

    elif s["scene"] == "f1":
        d.polygon([(x0 + 10, y0 + 56), (x0 + 54, y0 + 44), (x0 + 92, y0 + 52),
                   (x0 + 78, y0 + 60), (x0 + 18, y0 + 62)], fill=rgb(RED))
        for wx in (x0 + 22, x0 + 72):
            d.ellipse([wx, y0 + 56, wx + 14, y0 + 70], fill="#202020")
        d.line([x1 - 34, y0 + 18, x1 - 34, y0 + 58], fill="#505050", width=2)
        d.polygon([(x1 - 34, y0 + 18), (x1 - 8, y0 + 26), (x1 - 34, y0 + 34)], fill=rgb(RED))
        put(d, (x0 + 8, y0 + 4), "POLE", font(10, True), INK)

    else:
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=col, width=2)
        put(d, (cx, cy), s["place"].split(",")[0][:10], font(8, True), INK, anchor="mm")

    # place + time tag, always inside the illustration
    tag = s["place"]
    put(d, (x0 + 6, y1 - 13), tag, font(8, True), ink if light else MUTED)


# ---------------------------------------------------------------------------
# map
# ---------------------------------------------------------------------------
def map_panel(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=4, fill="#FFFDF7", outline=rgb(LINE), width=1)
    put(d, (x0 + 8, y0 + 5), "WHERE IT HAPPENED", font(10, True), INK)

    mx0, my0, mx1, my1 = x0 + 6, y0 + 24, x1 - 6, y1 - 46
    d.rectangle([mx0, my0, mx1, my1], fill=rgb(OCEAN))
    LAT_TOP, LAT_BOT = 83.0, -58.0

    def px(lon):
        return mx0 + (lon + 180.0) / 360.0 * (mx1 - mx0)

    def py(lat):
        return my0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * (my1 - my0)

    for lon in range(-180, 181, 30):
        d.line([px(lon), my0, px(lon), my1], fill=rgb(GRAT), width=1)
    for lat in range(-60, 90, 30):
        d.line([mx0, py(lat), mx1, py(lat)], fill=rgb(GRAT), width=1)

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "world110.geojson")
    with open(path, encoding="utf-8") as fh:
        geo = json.load(fh)
    for feat in geo["features"]:
        g = feat.get("geometry") or {}
        polys = g.get("coordinates") or []
        if g.get("type") == "Polygon":
            polys = [polys]
        for poly in polys:
            for ring in poly:
                pts = [(px(c[0]), py(c[1])) for c in ring if len(c) >= 2]
                if len(pts) > 2:
                    # skip Antarctica by latitude of the ring's centroid
                    if sum(p[1] for p in pts) / len(pts) > my1 - 4:
                        continue
                    d.polygon(pts, fill=rgb(LAND))
                    d.line(pts + [pts[0]], fill=rgb(COAST), width=1, joint="curve")

    # dots first, then greedy badges so a badge never covers its own dot
    placed = []
    MAP_PLACEMENTS.clear()
    for s in STORIES:
        dx, dy = px(s["lon"]), py(s["lat"])
        col = REGION_COLORS[s["region"]]
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=rgb(col), outline=(255, 255, 255), width=1)
        got = None
        for r in (0, 8, 15, 23, 32, 42):
            for k in range(16):
                ang = 2 * math.pi * k / 16
                bx, by = dx + r * math.cos(ang), dy + r * math.sin(ang)
                if not (mx0 + 8 < bx < mx1 - 8 and my0 + 8 < by < my1 - 8):
                    continue
                if all(math.hypot(bx - qx, by - qy) >= 2 * 6 + 3 for qx, qy, _ in placed):
                    got = (bx, by)
                    break
            if got:
                break
        if got is None:
            got = (dx, dy)
        bx, by = got
        if math.hypot(bx - dx, by - dy) > 4:
            d.line([dx, dy, bx, by], fill=rgb(col), width=1)
            ang = math.atan2(by - dy, bx - dx)
            hx, hy = bx - 7 * math.cos(ang), by - 7 * math.sin(ang)
            d.line([hx, hy, bx, by], fill=rgb(col), width=2)
            d.polygon([(bx, by), (hx + 3 * math.sin(ang), hy - 3 * math.cos(ang)),
                       (hx - 3 * math.sin(ang), hy + 3 * math.cos(ang))], fill=rgb(col))
        placed.append((bx, by, s["n"]))
        MAP_PLACEMENTS.append((s["n"], dx, dy, bx, by))
        badge(d, bx, by, s["n"], col, r=6, fsize=8)

    # legend, one row of seven
    lx, ly = x0 + 7, y1 - 37
    for reg in REGIONS:
        cnt = sum(1 for s in STORIES if s["region"] == reg)
        d.ellipse([lx, ly + 2, lx + 8, ly + 10], fill=rgb(REGION_COLORS[reg]))
        put(d, (lx + 12, ly + 6), f"{reg} {cnt}", font(8, True), INK, anchor="lm")
        lx += d.textlength(f"{reg} {cnt}", font=font(8, True)) + 22
    put(d, (x0 + 8, y1 - 14),
        "Each number is the story with that number on this page. Dots mark the place; lines join dot to number.",
        font(7), MUTED)


def list_panel(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=4, fill="#FFFDF7", outline=rgb(LINE), width=1)
    put(d, (x0 + 8, y0 + 5), f"ALSO ON SATURDAY 21 NOVEMBER — {len(STORIES) - 11} MORE STORIES",
        font(10, True), INK)
    briefs = [s for s in STORIES if s["size"] == "brief"]
    colw = (x1 - x0 - 16) // 2
    f = font(8)
    for i, s in enumerate(briefs):
        cx = x0 + 8 + (i // 10) * colw
        cy = y0 + 22 + (i % 10) * 23
        col = REGION_COLORS[s["region"]]
        badge(d, cx + 7, cy + 7, s["n"], col, r=6, fsize=8)
        lines = wrap(s["headline"], f, colw - 24, d)[:2]
        for j, ln in enumerate(lines):
            put(d, (cx + 18, cy + 1 + j * 10), ln, f, INK)
        put(d, (cx + 18, cy + 17), s["source"], font(7), MUTED)


# ---------------------------------------------------------------------------
# page
# ---------------------------------------------------------------------------
def build(out="entry.png"):
    im = Image.new("RGB", (W, H), rgb(PAPER))
    d = ImageDraw.Draw(im)

    d.rectangle([0, 0, W, 24], fill=rgb(RED))
    put(d, (12, 12), "THE WORLD IN ONE DAY", font(10, True), "#FFFFFF", anchor="lm")
    put(d, (W - 12, 12),
        f"{len(STORIES)} STORIES · 7 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
        font(9, True), "#FFFFFF", anchor="rm")

    put(d, (W // 2, 62), "Saturday 21 November 2026", font(66, True, True), INK, anchor="mm")
    put(d, (W // 2, 113),
        "COP31 runs past its deadline · Missiles over Riyadh · A deep quake shakes Peru",
        font(15, False, True), MUTED, anchor="mm")

    stats = [("DAY 13", "of COP31, still no deal"), ("3", "missiles downed over Riyadh"),
             ("6.7", "magnitude, Peru quake"), ("15", "hurt in Junín"),
             ("$60,000", "Bitcoin back above"), ("136", "Rahul's Test score"),
             ("2028", "killer-robot talks")]
    sw = (W - 24) // 7
    for i, (big, small) in enumerate(stats):
        sx = 12 + i * sw
        put(d, (sx + sw // 2, 141), big, font(24, True, True), rgb(RED), anchor="mm")
        put(d, (sx + sw // 2, 162), small, font(7), INK, anchor="mm")
        if i:
            d.line([sx, 130, sx, 170], fill=rgb(LINE))

    barx, bary, barw = 12, 173, (W - 24) // 7
    counts = {r: sum(1 for s in STORIES if s["region"] == r) for r in REGIONS}
    for i, r in enumerate(REGIONS):
        bx = 12 + i * barw
        d.rectangle([bx, bary, bx + barw - 2, bary + 19], fill=rgb(REGION_COLORS[r]))
        put(d, (bx + 6, bary + 9.5), f"{r} · {counts[r]}", font(9, True), "#FFFFFF", anchor="lm")

    mains = [s for s in STORIES if s["size"] == "main"][:3]
    mw = (W - 24 - 20) // 3
    for i, s in enumerate(mains):
        x = 12 + i * (mw + 10)
        y = 198
        d.rectangle([x, y, x + mw, y + 188], fill=rgb(CARD), outline=rgb(LINE))
        scene(d, (x + 3, y + 3, x + mw - 3, y + 93), s)
        d.rectangle([x + 3, y + 95, x + mw - 3, y + 109], fill=rgb(REGION_COLORS[s["region"]]))
        put(d, (x + 8, y + 102), s["kicker"], font(9, True), "#FFFFFF", anchor="lm")
        badge(d, x + mw - 16, y + 102, s["n"], REGION_COLORS[s["region"]], r=7, fsize=10)
        yy = y + 113
        for ln in wrap(s["headline"], font(16, True, True), mw - 14, d)[:2]:
            put(d, (x + 7, yy), ln, font(16, True, True), INK)
            yy += 19
        yy = max(yy + 4, y + 150)
        for ln in wrap(s["body"], font(10), mw - 16, d)[:2]:
            put(d, (x + 7, yy), ln, font(10), INK)
            yy += 13
        chip(d, x + mw - 76, y + 174, s["status"])

    smalls = [s for s in STORIES if s["size"] == "small"][:8]
    cw = (W - 24 - 24) // 4
    for i, s in enumerate(smalls):
        row, col = divmod(i, 4)
        x = 12 + col * (cw + 8)
        y = 392 + row * 108
        d.rectangle([x, y, x + cw, y + 104], fill=rgb(CARD), outline=rgb(LINE))
        scene(d, (x + 3, y + 3, x + 83, y + 99), s)
        d.rectangle([x + 86, y + 3, x + cw - 3, y + 15], fill=rgb(REGION_COLORS[s["region"]]))
        put(d, (x + 89, y + 9), s["kicker"], font(7, True), "#FFFFFF", anchor="lm")
        badge(d, x + cw - 13, y + 9, s["n"], REGION_COLORS[s["region"]], r=6, fsize=8)
        yy = y + 20
        for ln in wrap(s["headline"], font(10, True), cw - 92, d)[:2]:
            put(d, (x + 87, yy), ln, font(10, True), INK)
            yy += 12
        yy = max(yy + 3, y + 58)
        for ln in wrap(s["body"], font(8), cw - 92, d)[:2]:
            put(d, (x + 87, yy), ln, font(8), MUTED)
            yy += 10
        put(d, (x + 87, y + 96), s["source"], font(7, True), rgb(REGION_COLORS[s["region"]]))

    map_panel(d, (12, 614, 362, 884))
    list_panel(d, (370, 614, W - 12, 884))

    d.rounded_rectangle([12, 890, W - 12, 976], radius=4, fill="#F3E7D5", outline=rgb(RED), width=1)
    put(d, (20, 898), "DATE CHECK — stories left out on purpose", font(11, True), rgb(RED))
    yy = 913
    for ln in wrap(DATE_CHECK, font(9), W - 44, d)[:5]:
        put(d, (20, yy), ln, font(9), INK)
        yy += 12
    put(d, (20, 969), SOURCES_LINE, font(7), MUTED)

    put(d, (W // 2, 996),
        "Every story happened, or was first reported, on Saturday 21 November 2026. Original drawings by this agent.",
        font(8), MUTED, anchor="mm")

    im.save(out, "PNG", optimize=True)
    return out
