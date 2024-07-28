from hashlib import sha1
from pathlib import Path

from gyat_exceptions import IsNotCommitError
from utils_utils import (
    create_git_object, deserialize_gyat_object, find_repo_gyat)


def create_blob(path_file: Path, create_f: bool = False) -> str:
    data = open(path_file, "rb").read()
    header = f"blob {len(data)}\0".encode("utf-8")
    sha = sha1(header+data).hexdigest()

    if create_f:
        create_git_object(
            parent_repo=find_repo_gyat(), sha=sha, data=header+data)

    return sha


def create_tag(path_file: Path, create_f: bool = False) -> str:
    data = open(path_file, "rb").read()
    header = f"tag {len(data)}\0".encode("utf-8")
    sha = sha1(header+data).hexdigest()

    if create_f:
        create_git_object(
            parent_repo=find_repo_gyat(), sha=sha, data=header+data)

    return sha


def is_gyat_object(object_sha: str, gyat_obj_type: str):

    header = deserialize_gyat_object(object_sha)[0]
    object_type = header.decode('utf-8').strip().split()[0]
    if not object_type == gyat_obj_type:
        raise IsNotCommitError(object_sha)


def repo_is_gyat(cur_path: str = ".", required: bool = False) -> bool:
    abs_path = Path.absolute(cur_path)

    while abs_path:

        if (abs_path / ".gyat").exists():
            return True

        abs_path = abs_path / ".."

    if required:
        raise Exception("No git directory.")

    return False
