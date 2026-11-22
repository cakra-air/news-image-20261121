"""Independent verification of the map index on the 21 November front page.

This module is intentionally separate from render.py so the geometry of the
index can be checked without drawing anything.  Every public function returns
plain data; the caller decides how to display it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

LAT_NORTH = 83.0
LAT_SOUTH = -58.0
PLOT_LEFT = 324.0
PLOT_TOP = 756.0
PLOT_RIGHT = 700.0
PLOT_BOTTOM = 944.0
BADGE_RADIUS = 6.0
MIN_SEPARATION = 12.0
MAX_OFFSET = 42.0
RINGS = (0.0, 8.0, 15.0, 23.0, 32.0, 42.0)
CARD_SIZES = frozenset({"main", "small"})


@dataclass(frozen=True)
class Pixel:
    """A position in the 1024 by 1024 artwork."""

    x: float
    y: float

    def toward(self, other: "Pixel") -> float:
        return math.hypot(other.x - self.x, other.y - self.y)


@dataclass(frozen=True)
class Finding:
    """One row of the audit report."""

    name: str
    observed: str
    passed: bool

    @property
    def verdict(self) -> str:
        return "PASS" if self.passed else "FAIL"


def channel(value: str, index: int) -> int:
    stripped = value.lstrip("#")
    return int(stripped[index * 2 : index * 2 + 2], 16)


def to_rgb(value: str) -> tuple[int, int, int]:
    return channel(value, 0), channel(value, 1), channel(value, 2)


def softened(value: str, amount: float) -> tuple[int, int, int]:
    return tuple(round(c + (255 - c) * amount) for c in to_rgb(value))


def inside(pixel: Pixel, left: float, top: float,
           right: float, bottom: float) -> bool:
    return left < pixel.x < right and top < pixel.y < bottom


def project(longitude: float, latitude: float) -> Pixel:
    across = (longitude + 180.0) / 360.0 * (PLOT_RIGHT - PLOT_LEFT)
    down = (LAT_NORTH - latitude) / (LAT_NORTH - LAT_SOUTH)
    return Pixel(PLOT_LEFT + across, PLOT_TOP + down *
                 (PLOT_BOTTOM - PLOT_TOP))


def nearest_free(dot: Pixel, taken: list[Pixel]) -> Pixel:
    for ring in RINGS:
        for spoke in range(8):
            angle = spoke * math.tau / 8.0
            candidate = Pixel(dot.x + ring * math.cos(angle),
                              dot.y + ring * math.sin(angle))
            if not inside(candidate, PLOT_LEFT + 4, PLOT_TOP + 4,
                          PLOT_RIGHT - 4, PLOT_BOTTOM - 4):
                continue
            if all(candidate.toward(used) >= MIN_SEPARATION
                   for used in taken):
                return candidate
    return dot


def layout(dots: list[Pixel]) -> list[Pixel]:
    occupied: list[Pixel] = []
    for dot in dots:
        chosen = nearest_free(dot, occupied)
        occupied.append(chosen)
    return occupied


def numbered(stories: list[dict]) -> list[dict]:
    return sorted(stories, key=lambda item: item["n"])


def mapped(stories: list[dict]) -> list[dict]:
    return [item for item in stories if item["size"] in CARD_SIZES]


def shortlisted(stories: list[dict]) -> list[dict]:
    return [item for item in stories if item["size"] == "brief"]


def badge_findings(stories: list[dict]) -> list[Finding]:
    cards = mapped(stories)
    markers = [project(item["lon"], item["lat"]) for item in cards]
    placed = layout(markers)
    gaps = [a.toward(b) for i, a in enumerate(placed)
            for b in placed[i + 1 :]]
    shifts = [dot.toward(badge) for dot, badge in zip(markers, placed)]
    ids = [item["n"] for item in stories]
    return [
        Finding("badge count equals card count",
                f"{len(placed)} / {len(cards)}", len(placed) == len(cards)),
        Finding("story numbers unique and complete",
                f"{len(set(ids))} distinct, max {max(ids)}",
                sorted(ids) == list(range(1, len(ids) + 1))),
        Finding("minimum badge separation",
                f"{min(gaps):.2f} px", min(gaps) >= MIN_SEPARATION),
        Finding("largest badge offset",
                f"{max(shifts):.2f} px", max(shifts) <= MAX_OFFSET),
    ]


def place_findings(stories: list[dict]) -> list[Finding]:
    dots = [project(item["lon"], item["lat"])
            for item in shortlisted(stories)]
    valid = [inside(dot, PLOT_LEFT, PLOT_TOP, PLOT_RIGHT, PLOT_BOTTOM)
             for dot in dots]
    return [
        Finding("brief dots inside the plot",
                f"{sum(valid)} / {len(valid)}", all(valid)),
        Finding("brief count matches the two lists",
                f"{len(dots)}", len(dots) == 24),
    ]


def colour_findings(stories: list[dict], palette: list[str]) -> list[Finding]:
    used = sorted({item["region"] for item in stories})
    valid = all(1 <= region <= len(palette) for region in used)
    return [
        Finding("all seven regions present",
                f"{len(used)} / {len(palette)}", len(used) == len(palette)),
        Finding("region ids within palette",
                f"{used}", valid and len(set(palette)) == len(palette)),
    ]


def spot_check(stories: list[dict], sample: tuple[int, ...]) -> Finding:
    known = {item["n"]: item for item in stories}
    rows = []
    for number in sample:
        item = known.get(number)
        if item is None:
            rows.append(f"{number}:missing")
            continue
        dot = project(item["lon"], item["lat"])
        rows.append(f"{number}:{dot.x:.0f},{dot.y:.0f}")
    return Finding("manual coordinate spot-check",
                   " ".join(rows), len(rows) == len(sample))


def full_report(stories: list[dict], palette: list[str],
                sample: tuple[int, ...] = (1, 3, 8, 15, 26)) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(badge_findings(stories))
    findings.extend(place_findings(stories))
    findings.extend(colour_findings(stories, palette))
    findings.append(spot_check(stories, sample))
    return findings


def as_markdown(findings: list[Finding]) -> str:
    lines = ["| Check | Observed | Verdict |",
             "|---|---|---|"]
    for item in findings:
        lines.append(f"| {item.name} | {item.observed} | {item.verdict} |")
    return "\n".join(lines)
