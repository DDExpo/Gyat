from pathlib import Path

from gyat_exceptions import IsNotCommitError, IsNotTreeError
from const import GYAT_OBJECTS
from utils import is_gyat_object
from utils_utils import find_repo_gyat


from commands import (
    gyat_cat_file, gyat_commit_tree, gyat_hash_object, gyat_ls_tree,
    gyat_write_tree, gyat_init, gyat_log)


def cmd_add(args) -> None:
    # Implement the 'add' functionality
    pass


def cmd_ls_tree(args) -> None:
    gyat_ls_tree(args)


def cmd_commit_tree(args) -> None:

    parent_repo = find_repo_gyat()
    sha_tree = args.sha

    try:
        if not (parent_repo / "objects" /
                (sha_tree[:2] + "/" + sha_tree[2:])).exists():
            raise FileNotFoundError
        is_gyat_object(sha_tree, "tree")

    except PermissionError as e:
        print(
            "Permission to object: " +
            (parent_repo / 'objects' / (sha_tree[:2] + sha_tree[2:])) +
            f"Denied!\nerror: {e}")
    except FileNotFoundError as e:
        print(f"sha key invalid or object is not exist\nerror: {e}")
    except IsNotTreeError as e:
        print(f"error: {e}")
    gyat_commit_tree(parent_repo=parent_repo, sha_tree=sha_tree)


def cmd_write_tree(args) -> None:
    # Implement the 'write-tree' functionality
    pass


def cmd_cat_file(args) -> None:

    object_sha = args.sha
    try:
        gyat_cat_file(find_repo_gyat(), object_sha)
    except PermissionError:
        print("Permission to object: "
              f'{GYAT_OBJECTS} + {object_sha[:2] + object_sha[2:]} Denied!')
    except FileNotFoundError:
        print("sha key invalid or object is not exist")


def cmd_check_ignore(args) -> None:
    # Implement the 'check-ignore' functionality
    pass


def cmd_checkout(args) -> None:
    # Implement the 'checkout' functionality
    pass


def cmd_commit(args) -> None:
    # Implement the 'commit' functionality
    pass


def cmd_hash_object(args) -> None:
    path_file = Path(args.path)
    type_object = args.t

    if not path_file.exists():
        print(f"Path: {path_file} isnt exist!")
        return

    gyat_hash_object(path_file=path_file, mkfile=args.w,
                     object_type=type_object)


def cmd_init(args) -> None:
    path_dir = Path(args.path)
    flag = False
    if (path_dir / ".gyat").exists():
        print(
            "Directory already exist, still initialize gyat in this dir? (Y|n)"
        )
        if input().strip() == "Y":
            flag = True
        else:
            return

    gyat_init(path_dir=path_dir, force_create=flag)


def cmd_log(args) -> None:

    commit_sha = args.commit
    try:
        is_gyat_object(commit_sha, "commit")
    except IsNotCommitError as e:
        print(f"error: {e}")
    gyat_log(find_repo_gyat(), args.commit)


def cmd_ls_files(args) -> None:
    # Implement the 'ls-files' functionality
    pass


def cmd_rev_parse(args) -> None:
    # Implement the 'rev-parse' functionality
    pass


def cmd_rm(args) -> None:
    # Implement the 'rm' functionality
    pass


def cmd_show_ref(args) -> None:
    # Implement the 'show-ref' functionality
    pass


def cmd_status(args) -> None:
    # Implement the 'status' functionality
    pass


def cmd_tag(args) -> None:
    # Implement the 'tag' functionality
    pass
