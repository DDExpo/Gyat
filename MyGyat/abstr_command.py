from pathlib import Path

from const import GYAT_OBJECTS


from commands import (
    gyat_cat_file, gyat_commit_tree, gyat_hash_object, gyat_ls_tree,
    gyat_write_tree, gyat_init)


def cmd_add(args):
    # Implement the 'add' functionality
    pass


def cmd_ls_tree(args):
    gyat_ls_tree(args)


def cmd_commit_tree(args):
    # Implement the 'commit-tree' functionality
    pass


def cmd_write_tree(args):
    # Implement the 'write-tree' functionality
    pass


def cmd_cat_file(args):

    object_sha = args.sha
    try:
        gyat_cat_file()
    except PermissionError:
        print("Permission to object: "
              f'.gyat\\objects\\{object_sha[:2] / object_sha[2:]} Denied!')
    except FileExistsError:
        print("sha key invalid or object is not exist")
    except FileNotFoundError:
        print("sha key invalid or object is not exist")


def cmd_check_ignore(args):
    # Implement the 'check-ignore' functionality
    pass


def cmd_checkout(args):
    # Implement the 'checkout' functionality
    pass


def cmd_commit(args):
    # Implement the 'commit' functionality
    pass


def cmd_hash_object(args):
    path_file = Path(args.path)
    type_object = args.t

    gyat_hash_object(path_file=path_file, mkfile=args.w,
                     object_type=type_object)


def cmd_init(args):
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


def cmd_log(args):
    # Implement the 'log' functionality
    pass


def cmd_ls_files(args):
    # Implement the 'ls-files' functionality
    pass


def cmd_rev_parse(args):
    # Implement the 'rev-parse' functionality
    pass


def cmd_rm(args):
    # Implement the 'rm' functionality
    pass


def cmd_show_ref(args):
    # Implement the 'show-ref' functionality
    pass


def cmd_status(args):
    # Implement the 'status' functionality
    pass


def cmd_tag(args):
    # Implement the 'tag' functionality
    pass
