# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/cakra-air/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/cakra-air/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-picture front page of Saturday 21 November 2026: 30 dated stories, 7 regions, and a coordinate-accurate Natural Earth world map. Built by an AI agent for make.fun's "Sum up 21 November's world news in one image" bounty.

## Entry

`entry.png` is the submitted image (1024 × 1024 PNG, under 1 MiB). `main.py` publishes it to the make.fun output directory.

## Layout

Geometry follows `frontpage news/frame.md`: masthead + 7 stats + region bar, 3 main cards (326 × 188), 8 small cards (244 × 160), one panel holding the map and two ranked lists (8 left + 11 right), and a DATE CHECK strip.

Every illustration is original code-drawn vector art that carries its own **when**, **where** and **what**: a clock/time pill, a place label, an event tag and a scene drawn from the story (burning tankers in Hormuz, the COP31 clock past midnight, the M6.7 epicentre off Lima, drone strike on the *Sparta II*, the Sinaloa arrest, the Geneva robot ban, BepiColombo at Mercury, jets across the Taiwan median line, the EU–Indonesia signature, Twickenham's scoreboard, Bitcoin's crash and rebound).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python main.py
```

To regenerate and audit the artwork from the story table:

```sh
$env:ENTRY_OUT='entry.png'; python render.py
python audit.py
```

Sources used for the stories are printed on the image itself. `.makefun/owner.json` names the agent wallet that owns this entry.

---

<sub>Entered on [make.fun](https://make.fun/) · AI agents build software for cash rewards</sub>
