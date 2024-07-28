from pathlib import Path

from commands.write_tree import gyat_write_tree
from commands.commit_tree import gyat_commit_tree
from utils import create_blob


def gyat_hash_object(path_file: Path, mkfile: bool, object_type: str) -> None:

    if mkfile:
        sha_content = ""

        if object_type == "blob":
            sha_content = create_blob(path_file, True)

        elif object_type == "tree":
            sha_content = gyat_write_tree(path_file, True)

        elif object_type == "commit":
            sha_content = gyat_commit_tree(path_file, True)

        elif object_type == "tag":
            pass

    print(sha_content, end="")
