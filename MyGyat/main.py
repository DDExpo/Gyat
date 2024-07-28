import argparse
import sys

from abstr_command import (
    cmd_add, cmd_cat_file, cmd_check_ignore, cmd_checkout, cmd_commit,
    cmd_commit_tree, cmd_hash_object, cmd_init, cmd_log, cmd_ls_files,
    cmd_ls_tree, cmd_rev_parse, cmd_rm, cmd_show_ref, cmd_status, cmd_tag,
    cmd_write_tree
)


def main(argv: str = sys.argv[1:]):
    arg_parser = argparse.ArgumentParser()
    argsubparsers = arg_parser.add_subparsers(title="Commands", dest="command")
    argsubparsers.required = True

    argsp_init = argsubparsers.add_parser(
        "init", help="Initialize a new, empty repository.")
    argsp_init.add_argument(
        "path", metavar="directory", nargs="?", default=".",
        help="Where to create the repository."
    )
    argsp_log = argsubparsers.add_parser(
        "log", help="Display history of a given commit.")
    argsp_log.add_argument(
        "commit", default="HEAD", nargs="?", help="Commit to start at.")
    argsp_hash = argsubparsers.add_parser(
        "hash-object", help="Initialize a new, empty repository.")
    argsp_hash.add_argument(
        "-t", dest="type", choices=["blob", "commit", "tag", "tree"],
        default="blob", help="Create object.")
    argsp_hash.add_argument(
        "-w", dest="write", action="store_true", help="Create object.")
    argsp_hash.add_argument(
        "path", help="Where to create the object."
    )
    argsp_cat = argsubparsers.add_parser(
        "cat-file", help="Initialize a new, empty repository.")
    argsp_cat.add_argument("sha", help="Objets hash.")

    args = arg_parser.parse_args(argv)
    match args.command:
        case "add"          : cmd_add(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "commit-tree"  : cmd_commit_tree(args)
        case "write-tree"   : cmd_write_tree(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")


if __name__ == '__main__':
    main()
