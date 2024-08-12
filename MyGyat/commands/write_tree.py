import os
from pathlib import Path
from hashlib import sha1

from MyGyat.const import GYATIGNORE_DIR
from MyGyat.utils import (
    create_blob, create_gyat_object, get_gitignore, read_index)


def gyat_write_tree(
     base_dir: Path, w: bool = False, w_blobs: bool = False) -> str:

    dirs_files_skip = set(get_gitignore(base_dir) + list(GYATIGNORE_DIR))
    paths_for_tree = {Path(e.name).name for e in read_index(base_dir)[0]}

    def write_tree(path_name: Path):

        tree = []
        for new_path in sorted(os.listdir(path_name)):

            if new_path in dirs_files_skip:
                continue

            abs_path = path_name / new_path
            if abs_path.is_file() and new_path in paths_for_tree:
                tree.append(
                    f"100644 {new_path}\0".encode("utf-8") +
                    bytes.fromhex(create_blob(base_dir, abs_path, w_blobs))
                )

            elif abs_path.is_dir():
                _, sha = write_tree(path_name / new_path)
                if sha:
                    tree.append(
                        f"40000 {new_path}\0".encode("utf-8") +
                        bytes.fromhex(sha)
                    )

        tree_data = b"".join(tree)
        sha1_tree = ""
        header = ""

        if tree_data:
            header = f"tree {len(tree_data)}\0".encode("utf-8")
            sha1_tree = sha1(header[0] + tree_data).hexdigest()

        return header, tree_data, sha1_tree

    header, content, sha_tree = write_tree(base_dir)
    if w:
        create_gyat_object(base_dir, sha_tree, header+content)

    return sha_tree
