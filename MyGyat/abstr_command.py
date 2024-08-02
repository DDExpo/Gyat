import os
from pathlib import Path

from gyat_exceptions import IsNotSameTypeError, IsNotGyatDirError
from const import GYAT_OBJECTS
from utils import is_gyat_object, find_repo_gyat, valid_tag_name

from commands import (
    gyat_cat_file, gyat_commit_tree, gyat_hash_object, gyat_ls_tree,
    gyat_write_tree, gyat_init, gyat_show_ref, gyat_tag)


# TODO REFACTOR TRY EXCEPT VYRVIGLAZNYI GOVNOCOD

def cmd_add(args, base_dir: Path) -> None:
    # Implement the 'add' functionality
    pass


def cmd_ls_tree(args, base_dir: Path) -> None:

    sha_tree = args.sha

    try:
        base_dir = find_repo_gyat(Path(os.getcwd()))
        is_gyat_object(base_dir, sha_tree, "tree")

    except PermissionError as e:
        print(f"error: {e}")
    except FileNotFoundError as e:
        print(f"sha key invalid or object is not exist\nerror: {e}")
    except IsNotSameTypeError as e:
        print(f"error: {e}")
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        print(f"error: {e}")
    except IsNotGyatDirError as e:
        print(f"error {e}")
    else:
        gyat_ls_tree(base_dir, args, sha_tree)


def cmd_commit_tree(args, base_dir: Path) -> None:

    sha_tree = args.sha
    parent, message = args.p, args.m

    try:
        base_dir = find_repo_gyat(Path(os.getcwd()))
        is_gyat_object(base_dir, sha_tree, "tree")
    except PermissionError as e:
        print(f"error: {e}")
    except FileNotFoundError as e:
        print(f"sha key invalid or object is not exist\nerror: {e}")
    except IsNotSameTypeError as e:
        print(f"error: {e}")
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        print(f"error: {e}")
    except IsNotGyatDirError as e:
        print(e)

    gyat_commit_tree(
        parent_repo=base_dir, sha_tree=sha_tree,
        is_parent=parent, is_message=message)


def cmd_write_tree(args, base_dir: Path) -> None:
    directory = Path(args.path)

    try:
        find_repo_gyat(directory)
    except IsNotGyatDirError as e:
        print(e)

    if not directory.exists():
        print(f"Path to {directory} is not exists")
        return
    elif not directory.is_dir():
        print("Directory should be directory and not a file")
        return

    gyat_write_tree(directory)


def cmd_cat_file(args, base_dir: Path) -> None:

    try:
        base_dir = find_repo_gyat(Path(os.getcwd()))
        object_sha = args.sha
        if not object_sha:
            print("Sha shouldnt be empty line")
        else:
            gyat_cat_file(base_dir, object_sha)
    except PermissionError:
        print("Permission to object: "
              f'{GYAT_OBJECTS / (object_sha[:2] + object_sha[2:])} Denied!\n')
    except FileNotFoundError:
        print("sha key invalid or object is not exist")
    except IsNotGyatDirError as e:
        print(e)


def cmd_tag(args, base_dir: Path) -> None:

    try:
        base_dir = find_repo_gyat(Path(os.getcwd()))
        tag_name = args.name
        tag_message = args.m
        object_tag = args.obj
        annotated_tag = args.a
        if tag_name and valid_tag_name(tag_name):
            gyat_tag(
                base_dir=base_dir, tag_name=tag_name, message=tag_message,
                obj=object_tag, annotated_tag=annotated_tag)
        else:
            gyat_show_ref(base_dir, tag=True)
    except PermissionError:
        print(f"Permission to object: {object_tag} Denied!\n")
    except FileNotFoundError:
        print("sha key invalid or object is not exist")
    except IsNotGyatDirError as e:
        print(e)


def cmd_check_ignore(args, base_dir: Path) -> None:
    # Implement the 'check-ignore' functionality
    pass


def cmd_checkout(args, base_dir: Path) -> None:
    # Implement the 'checkout' functionality
    pass


def cmd_commit(args, base_dir: Path) -> None:
    # Implement the 'commit' functionality
    pass


def cmd_hash_object(args, base_dir: Path) -> None:
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


def cmd_init(args, base_dir: Path) -> None:
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


def cmd_show_ref() -> None:

    try:
        base_dir = find_repo_gyat(Path(os.getcwd()))
        gyat_show_ref(base_dir)

    except IsNotGyatDirError as e:
        print(e)


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
