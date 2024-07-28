import os
import zlib
from hashlib import sha1
from pathlib import Path

from const import BASE_DIR, GYAT_OBJECTS


def create_git_object(sha: str, data):
    os.makedirs(BASE_DIR / GYAT_OBJECTS / f"{sha[:2]}", exist_ok=True)

    with open(BASE_DIR / GYAT_OBJECTS / f"{sha[:2]}/{sha[2:]}", "wb") as f:
        f.write(zlib.compress(data))


def create_blob(path_file: Path, create_f: bool = False) -> str:
    data = open(path_file, "rb").read()
    header = f"blob {len(data)}\0".encode("utf-8")
    sha = sha1(header+data).hexdigest()

    if create_f:
        create_git_object(sha=sha, data=header+data)

    return sha


def parse_commit_to_graphiz(sha: str):
    pass


def create_tag(path_file: Path, create_f: bool = False) -> str:
    data = open(path_file, "rb").read()
    header = f"blob {len(data)}\0".encode("utf-8")
    sha = sha1(header+data).hexdigest()

    if create_f:
        create_git_object(sha=sha, data=header+data)

    return sha


def repo_is_git(cur_path: str = ".", required: bool = False) -> bool:
    abs_path = Path.absolute(cur_path)

    while abs_path:

        if (abs_path / ".gyat").exists():
            return True

        abs_path = abs_path / ".."

    if required:
        raise Exception("No git directory.")

    return False
