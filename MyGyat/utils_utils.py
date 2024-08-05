# Maybe this file shouldnt exist but i think
# its not a bad solution to unload main utils
# At least someday in the future i will look at this
# And say hey this is shitcode, and get a good laugh of this

import os
import zlib
from pathlib import Path

from gyat_exceptions import IsNotGyatDirError
from const import GYAT_OBJECTS


# Not a good practice to mix things (return|raise) but func isnt too complex
# so, idk, its not a worst solution at this specific situation
def find_repo_gyat(cur_path: str = ".") -> Path:
    abs_path = Path.absolute(cur_path)

    while abs_path.name:

        if (abs_path / ".gyat").exists():
            return abs_path

        abs_path = abs_path.parent

    raise IsNotGyatDirError


def deserialize_gyat_object(
        repo_parent: Path, object_sha: str) -> tuple[bytes, bytes]:

    with open(
            repo_parent / GYAT_OBJECTS /
            (object_sha[:2] + "/" + object_sha[2:]),
            mode="rb") as file:

        data_decompressed = zlib.decompress(file.read())
        header, content = data_decompressed.split(b"\x00", 1)

        return header, content


def create_gyat_object(parent_repo: Path, sha: str, data_bytes: bytes) -> None:

    os.makedirs(parent_repo / GYAT_OBJECTS / f"{sha[:2]}", exist_ok=True)
    with open(parent_repo / GYAT_OBJECTS / f"{sha[:2]}/{sha[2:]}", "wb") as f:
        f.write(zlib.compress(data_bytes))


def resolve_refs(base_dir: Path) -> list[str, Path]:

    refs: list[str, Path] = []

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

                refs.append(content, cur_path)
                return
            for next_path in os.listdir(base_dir / cur_path):
                recursia(cur_path / Path(next_path))

        except FileNotFoundError as e:
            print(e)

    recursia()

    return refs


def get_all_files_name(main_dir: Path) -> set[str]:

    set_files: set[str] = set()
    dirs: list[Path] = [main_dir]

    while dirs:

        cur_path = dirs.pop()

        if cur_path.is_file():
            set_files.add(cur_path.name())
            continue

        for next_path in os.listdir(cur_path):
            dirs.append(next_path)
