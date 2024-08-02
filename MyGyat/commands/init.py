import os
from pathlib import Path

from const import GYAT_OBJECTS


def gyat_init(path_dir: Path, force_create: bool = False) -> None:

    os.makedirs(path_dir / ".gyat", exist_ok=force_create)
    os.makedirs(path_dir / GYAT_OBJECTS, exist_ok=force_create)
    os.makedirs(path_dir / ".gyat/refs", exist_ok=force_create)
    os.makedirs(path_dir / ".gyat/refs/tags", exist_ok=force_create)
    with open(path_dir / ".gyat/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
