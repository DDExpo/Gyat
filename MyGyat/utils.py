from hashlib import sha1
from pathlib import Path
from functools import wraps

from const import INVALID_CHARS_TAG
from gyat_exceptions import IsNotSameTypeError
from utils_utils import create_gyat_object, deserialize_gyat_object


def catch_common_exceptions_with_args(func):
    def catch_common_exceptions(func):
        @wraps
        def wrapper(*args, **kwargs):
            try:
                func()
            except PermissionError as e:
                print(f"error: {e}")
            except TypeError as e:
                print(f"error: {e}")
            except FileNotFoundError as e:
                print("sha key invalid or object does not exist\n"
                      f"error: {e}")
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                print(f"error: {e}")
            except BaseException as e:
                print(f"Something went wrong {e}")
        return wrapper
    return catch_common_exceptions


def create_blob(base_dir: Path, path_file: Path,
                create_f: bool = False) -> str:
    '''Create sha of the given object, optionally write blob to a disk'''

    data = open(path_file, "rb").read()
    header = f"blob {len(data)}\x00".encode("utf-8")
    sha = sha1(header+data).hexdigest()

    if create_f:
        create_gyat_object(parent_repo=base_dir, sha=sha,
                           data_bytes=header+data)

    return sha


def is_gyat_object(repo: Path, object_sha: str, gyat_obj_type: str) -> bool:

    header = deserialize_gyat_object(repo_parent=repo,
                                     object_sha=object_sha)[0]
    object_type = header.decode('utf-8').strip().split()[0]
    if not object_type == gyat_obj_type:
        raise IsNotSameTypeError(object_type, gyat_obj_type)


def valid_tag_name(name: str):
    '''Almost validate name of the tag by the git standarts'''

    for char in INVALID_CHARS_TAG:
        if char in name:
            f"Not a valid tag name! char: {char}"
            return False
    return True
