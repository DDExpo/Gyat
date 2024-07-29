import argparse


def arparser_settings():
    arg_parser = argparse.ArgumentParser()
    argsubparsers = arg_parser.add_subparsers(title="Commands", dest="command")
    argsubparsers.required = True

    argsp_ls_tree = argsubparsers.add_parser(
        "ls-tree", help="View tree object from the dir.")
    argsp_ls_tree.add_argument("sha", type=str, help="Sha of the tree.")
    argsp_ls_tree.add_argument(
        "--name-only", action="store_true",
        help="Show only the names of files.")
    argsp_ls_tree.add_argument(
        "--object-only", action="store_true",
        help="Show only the object information.")
    argsp_ls_tree.add_argument(
        "--full-name", action="store_true",
        help="Show full names of files.")
    argsp_ls_tree.add_argument(
        "--full-tree", action="store_true",
        help="Show the full tree structure."
    )

    argsp_commit_tree = argsubparsers.add_parser(
        "commit-tree", help=" Create a tree object from the dir.")
    argsp_commit_tree.add_argument(
        "path", metavar="directory", nargs="?", default=".",
        help="Where to start.")
    argsp_commit_tree.add_argument(
        "-m", type=str, nargs="?", help="Message of commit.")
    argsp_commit_tree.add_argument(
        "-p", type=str, nargs="?", help="parent of cyrrent commit."
    )

    argsp_write_tree = argsubparsers.add_parser(
        "write-tree", help=" Create a tree object from the dir.")
    argsp_write_tree.add_argument(
        "path", metavar="directory", nargs="?", default=".",
        help="Where to start."
    )

    argsp_init = argsubparsers.add_parser(
        "init", help="Initialize a new, empty repository.")
    argsp_init.add_argument(
        "path", metavar="directory", nargs="?", default=".",
        help="Where to create the repository."
    )

    argsp_log = argsubparsers.add_parser(
        "log", help="Display history of a given commit.")
    argsp_log.add_argument(
        "commit", nargs="?", help="Commit to start at."
    )

    argsp_hash = argsubparsers.add_parser(
        "hash-object",
        help="Hash object with sha1 and optionaly write object to disk.")
    argsp_hash.add_argument(
        "-t", dest="type", choices=["blob", "commit", "tag", "tree"],
        default="blob", help="Create object.")
    argsp_hash.add_argument(
        "-w", dest="write", action="store_true", help="write object to disk.")
    argsp_hash.add_argument(
        "path", help="Path to object."
    )

    argsp_cat = argsubparsers.add_parser("cat-file", help="view gyat objects")
    argsp_cat.add_argument(
        "sha", help="Objets hash."
    )

    return arg_parser
