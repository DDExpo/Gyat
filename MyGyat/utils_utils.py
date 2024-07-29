# Maybe this file shouldnt exist but i think
# its not a bad solution to unload main utils
# At least someday in the future i will look at this
# And say hey this is shitcode, and get a good laugh of this

import os
import zlib
from pathlib import Path

from const import GYAT_OBJECTS


def find_repo_gyat(cur_path: str = ".") -> Path | None:
    abs_path = Path.absolute(cur_path)

    while abs_path:

        if (abs_path / ".gyat").exists():
            return abs_path

        abs_path = abs_path / ".."

    return None


def deserialize_gyat_object(repo_parent: Path,
                            object_sha: str) -> tuple[bytes, bytes]:

    try:
        with open(
             repo_parent / GYAT_OBJECTS /
             (object_sha[:2] + "/" + object_sha[2:]),
             mode="rb") as file:

            data_decompressed = zlib.decompress(file.read())
            header, content = data_decompressed.split(b"\0", 1)

            return header, content
    except FileNotFoundError:
        print(
            "File: "
            f"{repo_parent / (object_sha[:2] + '/' + object_sha[2:])}"
            " wasnt found")


def create_git_object(parent_repo: Path, sha: str, data):
    os.makedirs(parent_repo / GYAT_OBJECTS / f"{sha[:2]}", exist_ok=True)

    with open(parent_repo / GYAT_OBJECTS / f"{sha[:2]}/{sha[2:]}", "wb") as f:
        f.write(zlib.compress(data))
