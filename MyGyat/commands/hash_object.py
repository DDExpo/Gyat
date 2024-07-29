from pathlib import Path

from utils import create_blob
from commands.write_tree import gyat_write_tree
from commands.commit_tree import gyat_commit_tree


# TODO implement validation for tree and commit

def gyat_hash_object(path_object: Path, mkfile: bool,
                     object_type: str) -> None:

    sha_content = ""

    if object_type == "blob":
        if not path_object.is_file():
            print("Path should be to a file!")
            return
        sha_content = create_blob(path_file=path_object, create_f=mkfile)

    elif object_type == "tree":
        if not path_object.is_dir():
            print("Path should be to a directory!")
            return
        sha_content = "Not implemented"

    elif object_type == "commit":
        if not path_object.is_file():
            print("Path should be to a file!")
            return
        sha_content = "Not implemented"

    elif object_type == "tag":
        pass

    print(sha_content, end="")
