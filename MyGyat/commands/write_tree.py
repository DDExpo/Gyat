import os
from pathlib import Path
from hashlib import sha1

from const import GYATIGNORE_DIR
from utils import create_blob, create_gyat_object


def gyat_write_tree(
     base_dir: Path, path_object: Path = ".", write_tree: bool = False) -> str:

    # Maybe rafactor this later
    if path_object.is_file():

        sha = create_blob(base_dir, path_object, create_f=False)
        data = f"100644 blob {path_object.name}\x00{sha}".encode("utf-8")
        sha_tree = sha1(
            f"tree {len(data)}\x00".encode("utf-8") + data
        ).hexdigest()

        if write_tree:
            create_gyat_object(base_dir, sha_tree, data)
        print(sha_tree)
        return sha_tree

    def write_tree(path_name: Path):

        tree = []

        for new_path in sorted(os.listdir(path_name)):
            if new_path in GYATIGNORE_DIR:
                continue

            abs_path = path_name / new_path
            if abs_path.is_file():
                tree.append(
                    (f"100644 blob {new_path}\x00"
                     f"{create_blob(base_dir, abs_path, create_f=False)}"
                     ).encode("utf-8")
                )
            else:
                _, sha = write_tree(path_name / new_path)
                tree.append(f"040000 tree {new_path}\x00{sha}".encode("utf-8"))

        tree_data = b"".join(tree)

        sha1_tree = sha1(
            f"tree {len(tree_data)}\x00".encode("utf-8") + tree_data
        ).hexdigest()

        return tree_data, sha1_tree

    content, sha_tree = write_tree(path_object)
    if write_tree:
        create_gyat_object(base_dir, sha_tree, content)

    print(sha_tree)

    return sha_tree
