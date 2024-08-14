# Maybe this file shouldnt exist but i think
# its not a bad solution to loadade main utils
# At least someday in the future i will look at this
# And say hey this is shitcode, and get a good laugh of this

import os
import zlib
from hashlib import sha1
from collections import defaultdict
from pathlib import Path

from MyGyat.gyat_index_entry_class import GyatIndexEntry
from MyGyat.gyat_exceptions import IsNotGyatDirError, IsNotInGyatDir
from MyGyat.const import GYAT_OBJECTS


# Not a good practice to mix things (return|raise) but func isnt too complex
# so, idk, its not a worst solution at this specific situation
def find_repo_gyat(cur_path: Path = Path(".")) -> Path:
    '''Return path if ok else raise IsNotGyatDirError'''
    abs_path = Path.absolute(cur_path)

    while abs_path.name:

        if (abs_path / ".git").exists():
            return abs_path

        abs_path = abs_path.parent

    raise IsNotGyatDirError


def is_path_in_gyat_dir(abs_path: Path) -> None:

    while abs_path.name:

        if (abs_path / ".git").exists():
            return

        abs_path = abs_path.parent

    raise IsNotInGyatDir


def deserialize_gyat_object(repo_parent: Path,
                            object_sha: str) -> tuple[bytes, bytes]:

    with open(repo_parent / GYAT_OBJECTS /
              object_sha[:2] / object_sha[2:], mode="rb") as f:

        data_decompressed = zlib.decompress(f.read())
        header, content = data_decompressed.split(b"\x00", maxsplit=1)

    return header, content


def create_gyat_object(parent_repo: Path, sha: str, data_bytes: bytes) -> None:

    os.makedirs(parent_repo / GYAT_OBJECTS / f"{sha[:2]}", exist_ok=True)
    with open(parent_repo / GYAT_OBJECTS / f"{sha[:2]}/{sha[2:]}", "wb") as f:
        f.write(zlib.compress(data_bytes))


def resolve_refs(base_dir: Path, tag: bool = False) -> list[str, Path]:

    refs: list[tuple[str, Path]] = []

    def recursia(cur_path: Path = Path("."), start_path: str = ""):

        if (base_dir / cur_path).is_file():
            content = open(base_dir / cur_path, "r",
                           encoding="utf8").read().strip("\n")

            maybe_path = content.split()
            for maybe in maybe_path:
                if (base_dir / maybe).exists():
                    recursia(Path(maybe), cur_path)
                    return
            refs.append((content, start_path))
            return

        for next_path in sorted(os.listdir(base_dir / cur_path)):
            recursia(cur_path / Path(next_path), cur_path / Path(next_path))

    try:
        if tag:
            recursia("refs/tags", "refs/tags")
        else:
            recursia("refs", "refs")

    except FileNotFoundError as e:
        print(e)
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


def parse_gyatignore(gitignore_path: Path):

    patterns = []
    with open(gitignore_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('\\#'):
                line = line[1:]
            elif line.startswith('\\!'):
                line = line[1:]
            patterns.append(line)
    return patterns


def tree_from_index(base_dir, index_entries: GyatIndexEntry) -> str:

    contents = defaultdict(list)

    for entry in index_entries:

        dirname = os.path.dirname(entry.name)
        key = dirname
        while key != "":
            contents[key] = list()
            key = os.path.dirname(key)

        contents[dirname].append(entry)

    sorted_paths = sorted(contents.keys(), key=len, reverse=True)

    sha: str
    data: bytes
    header: bytes

    for path in sorted_paths:

        tree = []

        for entry in contents[path]:
            if isinstance(entry, GyatIndexEntry):

                leaf_mode = (f"{entry.mode_type:02o}"
                             f"{entry.mode_perms:04o}").encode("ascii")
                leaf = (
                    leaf_mode +
                    f" {os.path.basename(entry.name)}\0".encode() +
                    bytes.fromhex(entry.sha)
                )
            else:
                leaf = (
                    f"40000 {entry[0]}\0".encode() +
                    bytes.fromhex(entry[1])
                )

            tree.append(leaf)

        data = b"".join(tree)
        header = f"tree {len(data)}\0".encode("utf-8")
        sha = sha1(header+data).hexdigest()
        create_gyat_object(base_dir, sha, header+data)

        parent = os.path.dirname(path)
        base = os.path.basename(path)
        contents[parent].append((base, sha))

    return sha
