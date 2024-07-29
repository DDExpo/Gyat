import os
from pathlib import Path

from gyat_exceptions import IsNotCommitError, IsNotTreeError
from const import GYAT_OBJECTS
from utils import is_gyat_object, find_repo_gyat


from commands import (
    gyat_cat_file, gyat_commit_tree, gyat_hash_object, gyat_ls_tree,
    gyat_write_tree, gyat_init, gyat_log)


def cmd_add(args) -> None:
    # Implement the 'add' functionality
    pass


def cmd_ls_tree(args) -> None:

    sha_tree = args.sha
    base_dir = find_repo_gyat(Path(os.getcwd()))
    try:
        if not (base_dir / GYAT_OBJECTS /
                (sha_tree[:2] + "/" + sha_tree[2:])).exists():
            raise FileNotFoundError
        if not is_gyat_object(base_dir, sha_tree, "tree"):
            raise IsNotTreeError(sha_tree)

    except PermissionError as e:
        print(
            "Permission to object: " +
            (base_dir / 'objects' / (sha_tree[:2] + sha_tree[2:])) +
            f"Denied!\nerror: {e}")
    except FileNotFoundError as e:
        print(f"sha key invalid or object is not exist\nerror: {e}")
    except IsNotTreeError as e:
        print(f"error: {e}")

    gyat_ls_tree(base_dir, args, sha_tree)


def cmd_commit_tree(args) -> None:

    sha_tree = args.sha
    base_dir = find_repo_gyat(Path(os.getcwd()))
    parent, message = args.p, args.m
    try:
        if not (base_dir / GYAT_OBJECTS /
                (sha_tree[:2] + "/" + sha_tree[2:])).exists():
            raise FileNotFoundError
        if not is_gyat_object(base_dir, sha_tree, "tree"):
            raise IsNotTreeError(sha_tree)

    except PermissionError as e:
        print(
            "Permission to object: " +
            (base_dir / 'objects' / (sha_tree[:2] + sha_tree[2:])) +
            f"Denied!\nerror: {e}")
    except FileNotFoundError as e:
        print(f"sha key invalid or object is not exist\nerror: {e}")
    except IsNotTreeError as e:
        print(f"error: {e}")
    gyat_commit_tree(
        parent_repo=base_dir, sha_tree=sha_tree,
        is_parent=parent, is_message=message)


def cmd_write_tree(args) -> None:
    directory = Path(args.path)
    if not directory.exists():
        print(f"Path to {directory} is not exists")
        return
    elif not directory.is_dir():
        print("Directory should be directory and not a file")
        return
    gyat_write_tree(directory)


def cmd_cat_file(args) -> None:

    base_dir = find_repo_gyat(Path(os.getcwd()))

    try:
        object_sha = args.sha
        gyat_cat_file(base_dir, object_sha)
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
    path = Path(args.path)
    type_object = args.t

    if not path.exists():
        print(f"Path: {path} isnt exist!")
        return
    elif type_object == "tree" and not Path.is_dir():
        print(f"Path: {path} isnt directory!")
        return
    elif type_object in ("commit", "tag", "blob") and not path.is_file():
        print("Path should be to a file!")
        return

    gyat_hash_object(path=path, mkfile=args.w, object_type=type_object)


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
    base_dir = find_repo_gyat(Path(os.getcwd()))

    try:
        if not is_gyat_object(base_dir, commit_sha, "commit"):
            raise IsNotCommitError(commit_sha)
    except IsNotCommitError as e:
        print(f"error: {e}")

    gyat_log(base_dir, commit_sha=commit_sha)


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
