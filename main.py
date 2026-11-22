"""make.fun program/v1 entrypoint: publish the pre-rendered front page."""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
DEST_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
DEST = DEST_DIR / "entry.png"

DEST_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE, DEST)
os.chmod(DEST, 0o644)
print(f"published {SOURCE.name} to {DEST}")
