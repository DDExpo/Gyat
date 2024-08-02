import os
from pathlib import Path

from gyat_exceptions import IsNotSameTypeError, IsNotGyatDirError
from const import GYAT_OBJECTS
from utils import is_gyat_object, valid_tag_name

from commands import (
    gyat_cat_file, gyat_commit_tree, gyat_hash_object, gyat_ls_tree,
    gyat_write_tree, gyat_init, gyat_show_ref, gyat_tag)


def cmd_init(cur_directory: Path) -> None:

    flag = False
    if (cur_directory / ".gyat").exists():
        print(
            "Directory already exist, still initialize gyat in this dir? (Y|n)"
        )
        if input().strip() == "Y":
            flag = True
        else:
            return

    gyat_init(cur_directory, force_create=flag)


def cmd_ls_tree(base_dir: Path, sha: str, output_format: str) -> None:
    gyat_ls_tree(base_dir, sha, output_format)


def cmd_write_tree(obj_path: Path, base_dir: Path, wrtite_obj: bool) -> None:
    gyat_write_tree(base_dir, obj_path, wrtite_obj)


def cmd_commit_tree(
     base_dir: Path, sha: str, parent_sha: str,
     message: str, write_com: bool) -> None:
    gyat_commit_tree(base_dir, sha, parent_sha, message, write_com)


def cmd_hash_object(obj_path: Path, base_dir: Path,
                    obj_type: str, w_obj: bool) -> None:
    gyat_hash_object(obj_path, base_dir, obj_type, w_obj)


def cmd_cat_file(sha: str, base_dir: Path) -> None:
    gyat_cat_file(sha, base_dir)


def cmd_show_ref(base_dir) -> None:
    gyat_show_ref(base_dir)


def cmd_tag(base_dir, tag_name, message, obj, annotated_tag) -> None:

    if tag_name:
        gyat_tag(base_dir, tag_name, message, obj, annotated_tag)
    else:
        gyat_show_ref(base_dir, tag=True)


def cmd_add(args, base_dir: Path) -> None:
    # Implement the 'add' functionality
    pass


def cmd_check_ignore(args, base_dir: Path) -> None:
    # Implement the 'check-ignore' functionality
    pass


def cmd_checkout(args, base_dir: Path) -> None:
    # Implement the 'checkout' functionality
    pass


def cmd_commit(args, base_dir: Path) -> None:
    # Implement the 'commit' functionality


def cmd_ls_files(args, base_dir: Path) -> None:
    # Implement the 'ls-files' functionality
    pass


def cmd_rev_parse(args, base_dir: Path) -> None:
    # Implement the 'rev-parse' functionality
    pass


def cmd_rm(args, base_dir: Path) -> None:
    # Implement the 'rm' functionality
    pass


def cmd_status(args, base_dir: Path) -> None:
    # Implement the 'status' functionality
    pass
