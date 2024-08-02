import os
from pathlib import Path

from const import GYAT_REFS


def gyat_show_ref(base_dir: Path, tag: bool = False):

    base_dir = base_dir / GYAT_REFS / "tags" if tag else base_dir / GYAT_REFS

    def recursia(cur_path: Path = Path("")):

        try:
            if (base_dir / cur_path).is_file():
                content = open(base_dir / cur_path, "r",
                               encoding="utf8").read().strip("\n")

                # So refs is doubled [ref/ref] so we slice it
                maybe_path = content.split()[-1][5:]
                if (base_dir / maybe_path).exists():
                    recursia(Path(maybe_path))
                    return

                print(f"{content} {cur_path}")
                return
            for next_path in os.listdir(base_dir / cur_path):
                recursia(cur_path / Path(next_path))
        except FileNotFoundError as e:
            print(e)

    recursia()
