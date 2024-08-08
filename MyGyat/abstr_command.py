import os
from pathlib import Path

from const import GYAT_REFS
from utils import read_index, get_active_branch
from utils_utils import tree_from_index
from commands import (
    gyat_cat_file, gyat_commit_tree, gyat_hash_object, gyat_ls_tree,
    gyat_write_tree, gyat_init, gyat_show_ref, gyat_tag, gyat_ls_files,
    gyat_check_ignore, gyat_status, gyat_rm, gyat_add, gyat_clone_rep)


def cmd_init(cur_directory: Path) -> None:

    flag = True
    if (cur_directory / ".git").exists():
        print(
            "Directory already exist, still initialize gyat in this dir? (Y|n)"
        )
        if not input().strip() == "Y":
            return

    gyat_init(cur_directory, force_create=flag)


def cmd_ls_tree(base_dir: Path, sha: str, output_format: str) -> None:
    gyat_ls_tree(base_dir, sha, output_format)


def cmd_write_tree(obj_path: Path, base_dir: Path, wrtite_obj: bool) -> None:
    sha = gyat_write_tree(base_dir, obj_path, wrtite_obj)
    print(sha)


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


def cmd_status(base_dir: Path) -> None:
    gyat_status(base_dir)


def cmd_ls_files(base_dir: Path, verbose: bool) -> None:
    gyat_ls_files(base_dir, verbose)


def cmd_check_ignore(paths, base_dir: Path) -> None:
    gyat_check_ignore(paths, base_dir)


def cmd_rm(paths, base_dir: Path) -> None:
    gyat_rm(base_dir, paths)


def cmd_add(paths, base_dir: Path) -> None:
    gyat_add(paths, base_dir)


def cmd_commit(message: str, base_dir: Path) -> None:
    index_content, _ = read_index(base_dir)
    tree = tree_from_index(base_dir, index_content)

    commit = gyat_commit_tree(parent_repo=base_dir, sha_tree=tree,
                              message=message)

    active_branch = get_active_branch(base_dir)
    if active_branch:
        with open(base_dir / GYAT_REFS / "heads" / active_branch, "w") as fd:
            fd.write(commit + "\n")
    else:
        with open(base_dir / ".git/HEAD", "w") as fd:
            fd.write("\n")


def cmd_clone(url: str, dir: str) -> None:

    cur_dir = Path(os.getcwd())
    if dir:
        cur_dir = cur_dir / dir
        if (cur_dir / dir).exists():
            print("Directory already exist,"
                  " still clone repo in this dir? (Y|n)")
            if not input().strip() == "Y":
                return

        os.makedirs(name=cur_dir, exist_ok=True)
    gyat_init(cur_dir, force_create=True)
    gyat_clone_rep(cur_dir, url)
