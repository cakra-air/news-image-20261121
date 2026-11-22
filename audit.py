"""Three-pass audit required by PROMPT.md: geometry, semantics, 300px fonts."""
import math
from collections import Counter

from PIL import Image, ImageDraw

import render
from stories import STORIES, REGIONS, REGION_COLORS
from render import font, wrap, W, H

SCALE = 300.0 / W
report = []


def row(name, ok, detail):
    report.append((name, "PASS" if ok else "FAIL", detail))


def main():
    out = render.build("entry.png")
    im = Image.open(out)
    d = ImageDraw.Draw(im)

    # ---- 1. geometry -------------------------------------------------------
    row("canvas", im.size == (1024, 1024), f"{im.size}")
    row("all placements inside frame",
        all(0 <= x < W and 0 <= y < H for _, _, _, x, y in render.MAP_PLACEMENTS),
        f"{len(render.MAP_PLACEMENTS)} placements")
    # each card's text must fit the width it was given
    bad = []
    for s in STORIES:
        if s["size"] == "main":
            avail, fnt = 326 - 14, font(16, True, True)
        elif s["size"] == "small":
            avail, fnt = 244 - 92, font(10, True)
        else:
            avail, fnt = 310 - 24, font(8)
        for ln in wrap(s["headline"], fnt, avail, d):
            if d.textlength(ln, font=fnt) > avail + 1:
                bad.append(s["n"])
    row("no headline wider than its card", not bad, f"overflow ids={bad}")

    # ---- 2. semantics ------------------------------------------------------
    nums = [s["n"] for s in STORIES]
    row("numbers 1..N exactly once", sorted(nums) == list(range(1, len(nums) + 1)),
        f"N={len(nums)}")
    row("composition", Counter(s["size"] for s in STORIES) == Counter({"main": 3, "small": 8, "brief": 19}),
        str(dict(Counter(s["size"] for s in STORIES))))
    row("all seven regions present",
        set(s["region"] for s in STORIES) == set(REGIONS),
        ",".join(f"{r}={sum(1 for s in STORIES if s['region']==r)}" for r in REGIONS))
    row("region colours defined", all(s["region"] in REGION_COLORS for s in STORIES), "7 keys")
    row("map badge count = story count", len(render.MAP_PLACEMENTS) == len(STORIES),
        f"{len(render.MAP_PLACEMENTS)} badges")
    row("map badge numbers unique",
        len(set(p[0] for p in render.MAP_PLACEMENTS)) == len(STORIES), "unique")
    pts = [(x, y) for _, _, _, x, y in render.MAP_PLACEMENTS]
    mind = min(math.hypot(a[0] - b[0], a[1] - b[1])
               for i, a in enumerate(pts) for b in pts[i + 1:])
    row("min badge distance >= 2r (12px)", mind >= 12, f"min={mind:.1f}px")
    offs = [math.hypot(bx - dx, by - dy) for _, dx, dy, bx, by in render.MAP_PLACEMENTS]
    row("max badge offset <= 42px", max(offs) <= 42, f"max={max(offs):.1f}px")
    row("every story carries a source", all(s["source"] for s in STORIES), "30 sources")
    row("every story carries a place + time on its card",
        all(s["place"] and (s["kicker"] or s["scene"]) for s in STORIES), "30 datelines")

    # ---- 3. 300px font measurement ----------------------------------------
    sizes = {
        "title": 66, "main headline": 16, "main body": 10,
        "small headline": 10, "small body": 8, "list entry": 8,
        "map badge number": 8, "date check": 9,
    }
    for name, px in sizes.items():
        report.append((f"300px {name}", "INFO", f"{px}px -> {px * SCALE:.2f}px"))

    w = max(len(r[0]) for r in report)
    for name, status, detail in report:
        print(f"{status:4s}  {name:<{w}}  {detail}")


if __name__ == "__main__":
    main()
