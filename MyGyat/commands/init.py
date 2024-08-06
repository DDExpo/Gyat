import os
from pathlib import Path

from const import GYAT_OBJECTS


def gyat_init(path_dir: Path, force_create: bool) -> None:

    os.makedirs(path_dir / ".git", exist_ok=force_create)
    os.makedirs(path_dir / GYAT_OBJECTS, exist_ok=force_create)
    os.makedirs(path_dir / ".git/refs", exist_ok=force_create)
    os.makedirs(path_dir / ".git/refs/tags", exist_ok=force_create)
    open(path_dir / ".git/HEAD", "w").write("ref: refs/heads/main\n")
