"""Entrypoint: draw the front page and write entry.png next to this file.

The day is fixed by stories.DAY; nothing in this entry reads the network.
"""
import os

from render import build


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build(out)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
