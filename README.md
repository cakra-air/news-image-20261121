# Saturday 21 November 2026 — the world in one image

A single 1024×1024 front page. Thirty stories, each first reported on
21 November 2026, mapped by exact place and drawn by hand in code with
Pillow primitives. No photographs and no downloaded illustrations.

## Run

```
python main.py
```

writes `entry.png` beside `main.py`.

## Layout

- Three lead cards, eight small cards, and nineteen briefs in the list
  beside the map.
- Each illustrated card carries a place tag and a time tag inside its own
  drawing, so a reader can understand the event from the picture alone.
- The map is drawn from `world110.geojson` (Natural Earth, Antarctica
  skipped) in an equirectangular projection. Every story has a dot at its
  longitude/latitude and a numbered badge; a short line joins dot to badge
  when the badge had to be moved to avoid a collision.
- Region colours follow the seven-entry legend: Europe blue, Middle East
  orange, Africa green, Asia red, Americas purple, Oceania teal, World grey.
- `DATE CHECK` names the stories deliberately left out and why; sources are
  named beside each story.

## Files

| file | role |
| --- | --- |
| `main.py` | entrypoint, writes `entry.png` |
| `render.py` | all drawing code: vignettes, map, cards, legend, date check |
| `stories.py` | the dated story list, coordinates, sources and colours |
| `world110.geojson` | Natural Earth coastline used by the map |
| `entry.png` | generated front page |

Licensed under MIT; see `LICENSE`.
