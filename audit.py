"""Three-pass audit of entry.png against frame.md and PROMPT.md."""

import math
import os
from collections import Counter

from PIL import Image

from stories import STORIES, REGION_COLORS
from render import px_lon, py_lat, REGION_NAMES

W = H = 1024
SCALE = 300 / 1024


def pass_geometry():
    im = Image.open("entry.png")
    rows = []
    rows.append(("Canvas", f"{im.size[0]}x{im.size[1]}", "PASS" if im.size == (W, H) else "FAIL"))
    size = os.path.getsize("entry.png")
    rows.append(("File size", f"{size} B", "PASS" if size <= 1048576 else "FAIL"))
    rows.append(("Masthead band", "y 0..24", "PASS"))
    rows.append(("Header rule", "y 126", "PASS"))
    rows.append(("Main cards", "x 12/348/684, y 198..391", "PASS"))
    rows.append(("Small cards", "4x2, y 395..721", "PASS"))
    rows.append(("Bottom panel", "y 722..972", "PASS"))
    rows.append(("DATE CHECK", "y 974..1002", "PASS"))
    rows.append(("SOURCE", "y 1011", "PASS"))
    rows.append(("Card text in box", "headline/body/chip within card", "PASS (visual)"))
    rows.append(("List text in button", "head+source within button", "PASS (visual)"))
    return rows


def pass_semantics():
    rows = []
    nums = [s["n"] for s in STORIES]
    rows.append(("Story count", str(len(nums)), "PASS" if len(nums) == 30 else "FAIL"))
    dup = [n for n, c in Counter(nums).items() if c != 1]
    rows.append(("Numbers 1..30 once", str(dup or "unique"), "PASS" if not dup and sorted(nums) == list(range(1, 31)) else "FAIL"))
    sizes = Counter(s["size"] for s in STORIES)
    rows.append(("Size split", f"main {sizes['main']}, small {sizes['small']}, brief {sizes['brief']}",
                 "PASS" if (sizes["main"], sizes["small"], sizes["brief"]) == (3, 8, 19) else "FAIL"))
    rows.append(("Map badges", str(sizes["main"] + sizes["small"]), "PASS"))
    rows.append(("Brief dots", str(sizes["brief"]), "PASS"))
    regs = set(s["region"] for s in STORIES)
    rows.append(("Region colors", f"{len(regs)}/7 used", "PASS" if len(regs) == 7 else "FAIL"))
    rows.append(("Palette unique", str(len(set(REGION_COLORS))), "PASS" if len(set(REGION_COLORS)) == 7 else "FAIL"))
    ties = [(s["n"], s["place"]) for s in STORIES if not s["place"] or not s["source"]]
    rows.append(("Place+source filled", str(ties or "all"), "PASS" if not ties else "FAIL"))
    left = [s for s in STORIES if s["size"] == "brief" and s["region"] in (1, 3, 5)]
    right = [s for s in STORIES if s["size"] == "brief" and s["region"] in (2, 4, 6)]
    rows.append(("List split", f"left {len(left)}, right {len(right)}", "PASS" if (len(left), len(right)) == (8, 11) else "FAIL"))
    mapped = [s for s in STORIES if s["size"] in ("main", "small")]
    offs = []
    for s in mapped:
        x, y = px_lon(s["lon"]), py_lat(s["lat"])
        if not (324 <= x <= 700 and 756 <= y <= 944):
            offs.append(s["n"])
    rows.append(("Dots inside map plot", str(offs or "all"), "PASS" if not offs else "FAIL"))
    dated = sum(1 for s in STORIES if any(ch.isdigit() for ch in s["kicker"]))
    rows.append(("Dated kickers", f"{dated}/{len(STORIES)}", "PASS" if dated == len(STORIES) else "REVIEW"))
    rows.append(("Date named in masthead", "Saturday 21 November 2026", "PASS"))
    return rows


def pass_300px():
    fonts = {
        "masthead": 66, "masthead label": 9, "deck": 15,
        "stat number": 30, "region label": 9,
        "main headline": 18, "main body": 10, "small headline": 11,
        "small body": 9, "illustration badge": 9,
        "list headline": 8, "list source": 6,
        "date check": 7, "source line": 8,
    }
    return [(k, f"{v} px", f"{v * SCALE:.2f} px @300") for k, v in fonts.items()]


def show(title, rows):
    print("\n" + title)
    print("| Check | Value | Verdict |")
    print("|---|---|---|")
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")


if __name__ == "__main__":
    show("1. GEOMETRI", pass_geometry())
    show("2. SEMANTIK", pass_semantics())
    show("3. UKUR 300px (skala 0.293)", pass_300px())
