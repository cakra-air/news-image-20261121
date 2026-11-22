"""make.fun program/v1 entrypoint.

Publishes the rendered front page into the directory the grader reads.
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARTWORK = ROOT / "entry.png"


def publish_image(destination: Path) -> int:
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "entry.png"
    shutil.copyfile(ARTWORK, target)
    target.chmod(0o644)
    return target.stat().st_size


def main() -> None:
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    size = publish_image(output)
    print(f"published entry.png ({size} bytes) to {output}")


if __name__ == "__main__":
    main()
