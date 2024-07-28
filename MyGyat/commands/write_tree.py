import os
from pathlib import Path
from hashlib import sha1

from const import BASE_DIR, GYATIGNORE
from utils import create_blob, create_git_object


def gyat_write_tree(path_dir: Path = BASE_DIR) -> str:

    def write_tree(path_name: Path):
        tree = []

        for new_path in sorted(os.listdir(path_name)):
            if new_path in GYATIGNORE:
                continue

            abs_path = path_name / new_path
            if abs_path.is_file():
                tree.append(
                    (f"100644 blob {new_path}\0"
                        f"{create_blob(abs_path)}".encode("utf-8"))
                )
            else:
                _, sha = write_tree(path_name / new_path)
                tree.append(
                    f"040000 {new_path}\0{sha}".encode("utf-8")
                )

        tree_data = b"".join(tree)

        sha1_tree = sha1(
            f"tree {len(tree_data)}\0".encode("utf-8") + tree_data
        ).hexdigest()

        return tree_data, sha1_tree

    content, sha_tree = write_tree(path_dir)
    create_git_object(sha=sha_tree, data=content)

    return sha_tree
