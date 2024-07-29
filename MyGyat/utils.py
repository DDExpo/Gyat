from hashlib import sha1
from pathlib import Path

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


def is_gyat_object(repo: Path, object_sha: str, gyat_obj_type: str) -> bool:

    header = deserialize_gyat_object(repo_parent=repo,
                                     object_sha=object_sha)[0]
    object_type = header.decode('utf-8').strip().split()[0]
    return object_type == gyat_obj_type
