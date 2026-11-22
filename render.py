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
# vignettes. Normalised coordinates so each one fills whatever box it gets.
# Every vignette carries a place tag and a time tag inside the drawing.
# ---------------------------------------------------------------------------
def scene(d, box, s):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    col = rgb(REGION_COLORS[s["region"]])
    dark = s["scene"] in ("missiles", "quake")
    d.rectangle(box, fill="#1F2A3A" if dark else "#E8EEF1")
    ink = "#F2F2EE" if dark else INK

    def P(fx, fy):
        return (x0 + fx * bw, y0 + fy * bh)

    def line(a, b, fill, width=2):
        d.line([P(*a), P(*b)], fill=fill, width=width)

    def boxc(a, b, fill=None, outline=None, width=1):
        d.rectangle([P(*a), P(*b)], fill=fill, outline=outline, width=width)

    def ell(a, b, fill=None, outline=None, width=1):
        d.ellipse([P(*a), P(*b)], fill=fill, outline=outline, width=width)

    def poly(points, fill):
        d.polygon([P(*p) for p in points], fill=fill)

    k = s["scene"]
    if k == "cop":
        cx, cy = P(0.14, 0.48)
        r = 0.29 * bh
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
        line((0.14, 0.19), (0.14, 0.77), rgb(GRAT))
        line((0.03, 0.48), (0.25, 0.48), rgb(GRAT))
        boxc((0.33, 0.18), (0.93, 0.72), fill="#FFFDF7", outline=rgb(LINE))
        put(d, P(0.37, 0.30), "DRAFT 3", font(10, True), INK)
        put(d, P(0.37, 0.52), "no deal", font(9), MUTED)
        boxc((0.72, 0.60), (0.96, 0.90), fill=rgb(RED))
        put(d, P(0.84, 0.75), "OVERTIME", font(9, True), "#FFFFFF", anchor="mm")

    elif k == "missiles":
        for i in range(9):
            fx = 0.04 + i * 0.11
            h = 0.20 + (i % 4) * 0.06
            boxc((fx, 1 - h), (fx + 0.08, 0.88), fill="#33445C")
            for wy in (1 - h + 0.04, 1 - h + 0.13, 1 - h + 0.22):
                boxc((fx + 0.02, wy), (fx + 0.045, wy + 0.03), fill="#E8B84B")
        for i in range(3):
            fx = 0.10 + i * 0.28
            line((fx, 0.90), (fx + 0.16, 0.10), "#F2C14E", 2)
            ell((fx + 0.13, 0.06), (fx + 0.19, 0.14), fill="#F2A03D")
        put(d, P(0.04, 0.04), "03:00", font(9, True), "#F2F2EE")

    elif k == "quake":
        poly([(0, 0.92), (0.26, 0.32), (0.48, 0.92), (0.72, 0.36), (1, 0.92)], fill="#6B5B42")
        pts = []
        for i in range(41):
            fx = i / 40
            amp = 0.16 if 0.28 < fx < 0.62 else 0.01
            fy = 0.40 + (amp if i % 2 == 0 else -amp)
            pts.append(P(fx, fy))
        d.line(pts, fill=rgb(RED), width=2)
        for hx in (0.20, 0.76):
            boxc((hx, 0.72), (hx + 0.13, 0.92), fill="#EADCB9", outline="#3A3026")
            poly([(hx - 0.02, 0.72), (hx + 0.065, 0.60), (hx + 0.15, 0.72)], fill=rgb(RED))
        put(d, P(0.04, 0.04), "00:09 UTC · 108 km", font(9, True), "#F2F2EE")

    elif k == "bridge":
        line((0, 0.76), (1, 0.76), "#5C5C5C", 3)
        for i in range(4):
            fx = 0.12 + i * 0.24
            line((fx, 0.76), (fx, 0.30), "#5C5C5C", 2)
            ell((fx - 0.035, 0.23), (fx + 0.035, 0.30), fill=rgb(RED))
        poly([(0.50, 0.04), (0.57, 0.22), (0.43, 0.22)], fill=rgb(RED))
        put(d, P(0.04, 0.03), "DOUBLE TAP", font(8, True), INK)

    elif k == "uranium":
        ell((0.22, 0.12), (0.72, 0.62), outline=col, width=3)
        ell((0.36, 0.26), (0.58, 0.48), fill=col)
        line((0.47, 0.02), (0.47, 0.12), col, 3)
        put(d, P(0.05, 0.72), "STAYS IN IRAN", font(8, True), INK)

    elif k == "tax":
        for i in range(3):
            fx = 0.06 + i * 0.26
            boxc((fx, 0.30), (fx + 0.18, 0.92), fill="#4A5A6A")
            for wy in (0.38, 0.52, 0.66):
                boxc((fx + 0.04, wy), (fx + 0.10, wy + 0.05), fill="#D9E2EA")
        ell((0.56, 0.06), (0.94, 0.44), outline=rgb(RED), width=3)
        put(d, P(0.75, 0.25), "%", font(20, True), rgb(RED), anchor="mm")

    elif k == "flags":
        boxc((0.06, 0.14), (0.40, 0.70), fill=rgb(RED))
        ell((0.14, 0.28), (0.25, 0.40), fill="#F2C14E")
        boxc((0.58, 0.14), (0.92, 0.70), fill="#FFFFFF", outline="#B0B0B0")
        ell((0.68, 0.30), (0.81, 0.44), fill=rgb(RED))
        put(d, P(0.50, 0.82), "RETRACT", font(9, True), INK, anchor="mm")

    elif k == "btc":
        d.rectangle([P(0.02, 0.02), P(0.66, 0.15)], fill="#E8EEF1")
        put(d, P(0.04, 0.04), "BTC $60,000", font(8, True), INK)
        pts = [P(0.04, 0.72), P(0.22, 0.42), P(0.40, 0.56),
               P(0.60, 0.24), P(0.80, 0.40), P(0.96, 0.18)]
        d.line(pts, fill=rgb(RED), width=3)

    elif k == "robot":
        d.rounded_rectangle([P(0.24, 0.20), P(0.64, 0.68)], radius=6, outline=col, width=3)
        ell((0.34, 0.34), (0.41, 0.41), fill=col)
        ell((0.49, 0.34), (0.56, 0.41), fill=col)
        put(d, P(0.04, 0.04), "2028", font(13, True), INK)
        put(d, P(0.04, 0.80), "no ban yet", font(8), MUTED)

    elif k == "cricket":
        line((0.12, 0.96), (0.50, 0.18), "#8A6A3C", 6)
        ell((0.46, 0.12), (0.58, 0.24), fill=rgb(RED))
        d.rounded_rectangle([P(0.58, 0.16), P(0.96, 0.60)], radius=3, fill="#2E3A46")
        put(d, P(0.77, 0.38), "136", font(18, True), "#FFFFFF", anchor="mm")

    elif k == "f1":
        poly([(0.04, 0.60), (0.42, 0.44), (0.84, 0.54), (0.70, 0.66), (0.14, 0.68)], fill=rgb(RED))
        for fx in (0.18, 0.66):
            ell((fx, 0.60), (fx + 0.16, 0.76), fill="#202020")
        line((0.90, 0.14), (0.90, 0.54), "#505050", 2)
        poly([(0.90, 0.14), (0.99, 0.21), (0.90, 0.28)], fill=rgb(RED))
        put(d, P(0.04, 0.03), "POLE", font(10, True), INK)

    else:
        ell((0.34, 0.30), (0.66, 0.62), outline=col, width=2)
        put(d, P(0.50, 0.46), s["place"].split(",")[0][:10], font(8, True), INK, anchor="mm")

    put(d, (x0 + 5, y1 - 13), s["place"], font(8, True), ink)

# ---------------------------------------------------------------------------
# map
# ---------------------------------------------------------------------------
def map_panel(d, box):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=4, fill="#FFFDF7", outline=rgb(LINE), width=1)
    put(d, (x0 + 8, y0 + 5), "WHERE IT HAPPENED", font(10, True), INK)

    mx0, my0, mx1, my1 = x0 + 6, y0 + 24, x1 - 6, y1 - 62
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

    # legend, two rows so every region fits the wider map panel
    for i, reg in enumerate(REGIONS):
        row, col = divmod(i, 4)
        lx, ly = x0 + 7 + col * 96, y1 - 52 + row * 16
        cnt = sum(1 for s in STORIES if s["region"] == reg)
        d.ellipse([lx, ly + 2, lx + 8, ly + 10], fill=rgb(REGION_COLORS[reg]))
        put(d, (lx + 12, ly + 6), f"{reg} {cnt}", font(8, True), INK, anchor="lm")
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
    cw, ch = (W - 24 - 24) // 4, 140
    for i, s in enumerate(smalls):
        row, col = divmod(i, 4)
        x = 12 + col * (cw + 8)
        y = 390 + row * (ch + 6)
        d.rectangle([x, y, x + cw, y + ch], fill=rgb(CARD), outline=rgb(LINE))
        scene(d, (x + 4, y + 4, x + 96, y + ch - 4), s)
        d.rectangle([x + 100, y + 4, x + cw - 4, y + 18], fill=rgb(REGION_COLORS[s["region"]]))
        put(d, (x + 103, y + 11), s["kicker"], font(8, True), "#FFFFFF", anchor="lm")
        badge(d, x + cw - 13, y + 11, s["n"], REGION_COLORS[s["region"]], r=6, fsize=8)
        yy = y + 24
        for ln in wrap(s["headline"], font(13, True), cw - 108, d)[:3]:
            put(d, (x + 100, yy), ln, font(13, True), INK)
            yy += 16
        yy = max(yy + 3, y + 76)
        for ln in wrap(s["body"], font(10), cw - 108, d)[:3]:
            put(d, (x + 100, yy), ln, font(10), MUTED)
            yy += 12
        put(d, (x + 100, y + 131), s["source"], font(8, True), rgb(REGION_COLORS[s["region"]]))

    map_panel(d, (12, 680, 392, 930))
    list_panel(d, (400, 680, W - 12, 930))

    # Top-1 style: a slim red rule around one flowing DATE CHECK paragraph,
    # the label sitting inline in red, then two quiet lines underneath.
    d.rectangle([12, 934, W - 12, 974], fill="#FBF6EE", outline=rgb(RED), width=1)
    label = "DATE CHECK  "
    fl, fb = font(9, True), font(8)
    put(d, (20, 942), label, fl, rgb(RED))
    indent = 20 + d.textlength(label, font=fl)
    lines = wrap(DATE_CHECK, fb, 700, d)
    for i, ln in enumerate(lines[:3]):
        put(d, (20 if i else indent, 942 + i * 11), ln, fb, INK)
    put(d, (12, 987),
        "Every story happened, or was first reported, on Saturday 21 November 2026. "
        "Official counts and claims are attributed.",
        font(7), MUTED)
    put(d, (12, 1006), SOURCES_LINE, font(6.5), MUTED)

    im.save(out, "PNG", optimize=True)
    return out
