from pathlib import Path

from utils import create_blob
from commands.write_tree import gyat_write_tree
from commands.commit_tree import gyat_commit_tree


# TODO implement validation for tree and commit

def gyat_hash_object(
     path_object: Path, base_dir: Path,
     object_type: str, write_obj: bool) -> None:

    sha_content = ""

    if object_type == "blob":
        sha_content = create_blob(base_dir, path_object, write_obj)

    elif object_type == "tree":
        sha_content = "Not implemented"

    elif object_type == "commit":
        sha_content = "Not implemented"

    elif object_type == "tag":
        pass

    print(sha_content, end="")
