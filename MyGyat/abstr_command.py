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


def cmd_ls_tree(args, base_dir: Path) -> None:
    gyat_ls_tree(base_dir, args, args.sha)


def cmd_write_tree(obj_path: Path, base_dir: Path, wrtite_obj: bool) -> None:
    gyat_write_tree(base_dir, obj_path, wrtite_obj)


def cmd_commit_tree(args, base_dir: Path) -> None:
    gyat_commit_tree(base_dir, args.sha, args.p, args.m, args.w)


def cmd_hash_object(obj_path: Path, base_dir: Path, object_type: str) -> None:

    elif type_object == "tree" and not Path.is_dir():
        print(f"Path: {path} isnt directory!")
        return
    elif type_object in ("commit", "tag", "blob") and not path.is_file():
        print("Path should be to a file!")
        return

    gyat_hash_object(path=path, mkfile=args.w, object_type=type_object)


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
        print("sha key invalid or object does not exist")
    except IsNotGyatDirError as e:
        print(e)

def cmd_add(args, base_dir: Path) -> None:
    # Implement the 'add' functionality
    pass



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
        print("sha key invalid or object does not exist")
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
