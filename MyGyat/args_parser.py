from argparser_class import ArgumentParserNotExit


def arparser_settings():
    arg_parser = ArgumentParserNotExit(exit_on_error=False)
    argsubparsers = arg_parser.add_subparsers(title="Commands", dest="command")
    argsubparsers.required = False

    argsp_init = argsubparsers.add_parser(
        "init", help="Initialize a new, empty repository.")
    argsp_init.add_argument(
        "path", metavar="directory", nargs="?", default=".",
        help="Where to create the repository."
    )

    argsp_ls_tree = argsubparsers.add_parser(
        "ls_tree", help="View tree object from the dir.")
    argsp_ls_tree.add_argument(
        "sha", help="Sha of the tree or ref/tag.")
    argsp_ls_tree.add_argument(
        "-f", dest="format", default="name-only",
        choices=["name-only", "object-only", "full-tree"],
        help="Output format"
    )

    argsp_write_tree = argsubparsers.add_parser(
        "write_tree", help=" Create a tree object from the dir.")
    argsp_write_tree.add_argument(
        "-w", action="store_true", help="Write object to disk.")
    argsp_write_tree.add_argument(
        "path", metavar="directory", nargs="?", default=".",
        help="Where to start."
    )

    argsp_commit_tree = argsubparsers.add_parser(
        "commit_tree",
        help=("Write commit of a given tree object. "
              "with optional parent and message"))
    argsp_commit_tree.add_argument(
        "sha", help="Sha of the Tree or ref/tag.")
    argsp_commit_tree.add_argument(
        "-w", actions="store_true", help=" of commit.")
    argsp_commit_tree.add_argument(
        "-m", type=str, nargs="?", help="Write object to disk.")
    argsp_commit_tree.add_argument(
        "-p", type=str, nargs="?", help="Parent sha of current tree."
    )

    argsp_hash = argsubparsers.add_parser(
        "hash_object",
        help="Hash object with sha1 and optionaly write object to disk.")
    argsp_hash.add_argument(
        "path", help="Path to object.")
    argsp_hash.add_argument(
        "-t", dest="type", choices=["blob", "commit", "tag", "tree"],
        default="blob", help="Type of the object.")
    argsp_hash.add_argument(
        "-w", dest="write", action="store_true", help="write object to disk."
    )

    argsp_cat = argsubparsers.add_parser(
        "cat_file", help="view gyat objects")
    argsp_cat.add_argument(
        "sha", help="Objets hash or ref/tag."
    )

    argsp_tag = argsubparsers.add_parser(
        "tag", help="list all tags if ar")
    argsp_tag.add_argument(
        "-a", action="store_true", help="Create annotated tag.")
    argsp_tag.add_argument(
        "name", help="Tags name.")
    argsp_tag.add_argument(
        "-m", nargs="?", default="", help="Tags message.")
    argsp_tag.add_argument(
        "obj", nargs="?", default="HEAD",
        help="The object the new tag will point to."
    )

    argsp_ls_files = argsubparsers.add_parser(
        "ls_files",  help="List all the stage files.")
    argsp_ls_files.add_argument(
        "-v", action="store_true", help="Show everything."
    )

    argsp_checkout = argsubparsers.add_parser(
        "checkout", help="Checkout a commit inside of a directory.")
    argsp_checkout.add_argument(
        "sha", help="The commit or tree to checkout.")
    argsp_checkout.add_argument(
        "path", help="The empty directory to checkout on."
    )

    argsp_check_ignore = argsubparsers.add_parser(
        "check-ignore", help="Check path(s) against ignore rules.")
    argsp_check_ignore.add_argument(
        "path", nargs="+", help="Paths to check"
    )

    argsp_status = argsubparsers.add_parser(
        "status",  help="Show the working tree status."
    )

    argsp_rm = argsubparsers.add_parser(
        "rm", help="Remove files from the working tree and the index.")
    argsp_rm.add_argument(
        "path", nargs="+", help="Files to remove"
    )

    argsp_add = argsubparsers.add_parser(
        "add", help="Add files contents to the index.")
    argsp_add.add_argument(
        "path", nargs="+", help="Files to add"
    )

    argsp_comm = argsubparsers.add_parser(
        "commit", help="Record changes to the repository.")
    argsp_comm.add_argument(
        "-m", metavar="message", dest="message",
        help="Message to associate with this commit."
    )

    argsp_clone = argsubparsers.add_parser(
        "clone", help="Clone remote repository to current dir, by url.")
    argsp_clone.add_argument(
        "url", help="Url link to github rep."
    )

    argsp_log = argsubparsers.add_parser(
        "log", help="Display history of a given commit.")
    argsp_log.add_argument(
        "commit", nargs="?", help="Commit to start at."
    )

    return arg_parser
