import re
from hashlib import sha1
from pathlib import Path

from gyat_exceptions import IsNotSameTypeError
from utils_utils import (
    create_gyat_object, deserialize_gyat_object, find_repo_gyat)


def wrapper_try_except():
    pass


def create_blob(path_file: Path, create_f: bool = False) -> str:
    data = open(path_file, "rb").read()
    header = f"blob {len(data)}\x00".encode("utf-8")
    sha = sha1(header+data).hexdigest()

    if create_f:
        create_gyat_object(
            parent_repo=find_repo_gyat(), sha=sha, data=header+data, obj_type="blob")

    return sha


def is_gyat_object(repo: Path, object_sha: str, gyat_obj_type: str) -> bool:

    header = deserialize_gyat_object(repo_parent=repo,
                                     object_sha=object_sha)[0]
    object_type = header.decode('utf-8').strip().split()[0]
    if not object_type == gyat_obj_type:
        raise IsNotSameTypeError(object_type, gyat_obj_type)


def valid_tag_name(name: str) -> bool:
    '''Validate name of the tag by the git standarts'''

    pattern = re.compile(
        r"^(?!@)(?!.*//)(?!.*\.\.)[^@\000-\037\177 ~^:?*[](?<!\.(lock|))(?<!\.)$")

    return pattern.match(name)
