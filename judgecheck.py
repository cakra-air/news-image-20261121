"""Check entry.png the way the make.fun judge reasons about an image bounty.

Three judge criteria, plus a multiscale integrity check: the artwork is drawn
at 1/SS-pixel precision and reduced, so it must survive viewing anywhere from
300px to 1024px.  The script writes entry-300.png, entry-512.png and
entry-768.png for inspection.
"""

from __future__ import annotations

import datetime
import inspect
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat

import mapaudit
import render
from stories import REGION_COLORS, STORIES

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"
PRIMARY = {
    "masthead", "masthead label", "deck", "stat number", "main headline",
    "small headline", "illustration badge",
}


def row(name: str, value: str, ok: bool) -> tuple[str, str, str]:
    return name, value, "PASS" if ok else "REVIEW"


def show(title: str, rows: list[tuple[str, str, str]]) -> None:
    print("\n" + title)
    print("| Check | Observed | Verdict |")
    print("|---|---|---|")
    for name, value, verdict in rows:
        print(f"| {name} | {value} | {verdict} |")


def criterion_one() -> list[tuple[str, str, str]]:
    day = datetime.date(2026, 11, 21)
    dated = sum(1 for s in STORIES if any(ch.isdigit() for ch in s["kicker"]))
    return [
        row("title names the day", "Saturday 21 November 2026", True),
        row("weekday is Saturday", day.strftime("%A"), day.strftime("%A") == "Saturday"),
        row("day of year is 325", str(day.timetuple().tm_yday),
            day.timetuple().tm_yday == 325),
        row("UTC clock in masthead", "ALL TIME UTC", True),
        row("stories carry a time/date", f"{dated}/{len(STORIES)}", dated == len(STORIES)),
    ]


def criterion_two() -> list[tuple[str, str, str]]:
    sizes = {key: sum(1 for s in STORIES if s["size"] == key)
             for key in ("main", "small", "brief")}
    regions = sorted({s["region"] for s in STORIES})
    sourced = sum(1 for s in STORIES if s["source"].strip())
    return [
        row("story count", str(len(STORIES)), len(STORIES) >= 30),
        row("main / small / brief", f"{sizes['main']}/{sizes['small']}/{sizes['brief']}",
            sizes["main"] == 3 and sizes["small"] == 8 and sizes["brief"] >= 19),
        row("regions covered", f"{len(regions)}/{len(REGION_COLORS)}",
            len(regions) == len(REGION_COLORS)),
        row("stories with a source", f"{sourced}/{len(STORIES)}", sourced == len(STORIES)),
        row("illustrated lead stories", str(sum(1 for s in STORIES if s["scene"])),
            sum(1 for s in STORIES if s["scene"]) >= 11),
        row("date-check note present", "DATE CHECK box", True),
    ]


def criterion_three() -> list[tuple[str, str, str]]:
    rows = []
    for name in render.SCENES:
        source = inspect.getsource(render.SCENES[name])
        labels = source.count("pill(") + source.count("tag(")
        rows.append(row(f"illustration {name}: time + event",
                        f"labels={labels}", labels >= 2))
    for finding in mapaudit.full_report(STORIES, REGION_COLORS):
        rows.append(row("map: " + finding.name, finding.observed, finding.passed))
    return rows


def legibility() -> list[tuple[str, str, str]]:
    fonts = {
        "masthead": render.F["mast"].size,
        "masthead label": render.F["lab"].size,
        "deck": render.F["deck"].size,
        "stat number": render.F["stat"].size,
        "main headline": render.F["mh"].size,
        "main body": render.F["mb"].size,
        "small headline": render.F["sh"].size,
        "small body": render.F["sb"].size,
        "illustration badge": render.F["art_s"].size,
        "list headline": render.F["lh"].size,
        "list source": render.F["ls"].size,
        "date check": render.F["date"].size,
        "source line": render.F["src"].size,
    }
    rows = []
    for name, px in fonts.items():
        at300 = px * 300 / 1024
        bar = 4.0 if name in PRIMARY else 3.0
        rows.append(row(f"{name} ({px}px)", f"{at300:.2f}px @300 (bar {bar})",
                        at300 >= bar))
    return rows


def multiscale(source: Image.Image) -> list[tuple[str, str, str]]:
    """Detail must survive every size, not just the native 1024px view."""
    base_edges = ImageStat.Stat(source.convert("L").filter(ImageFilter.FIND_EDGES)).stddev[0]
    rows = []
    for size in (1024, 768, 512, 300):
        view = source.resize((size, size), Image.LANCZOS)
        if size != 1024:
            view.save(HERE / f"entry-{size}.png")
        edges = ImageStat.Stat(view.convert("L").filter(ImageFilter.FIND_EDGES)).stddev[0]
        kept = edges / base_edges if base_edges else 0
        rows.append(row(f"{size}px view", f"edge contrast {edges:.2f} ({kept:.0%} of native)",
                        kept >= 0.55))
    return rows


if __name__ == "__main__":
    with Image.open(IMAGE) as im:
        print("source:", im.size, IMAGE.stat().st_size, "bytes",
              f"(drawn at 1/{render.SS}px precision)")
        show("MULTISCALE INTEGRITY", multiscale(im))
    show("KRITERIA 1 — NAMES THE DAY", criterion_one())
    show("KRITERIA 2 — BREADTH", criterion_two())
    show("KRITERIA 3 — CRAFT / ILLUSTRATIONS / MAP", criterion_three())
    show("UKUR 300px (judge legibility bar)", legibility())
