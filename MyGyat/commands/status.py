import os
from pathlib import Path
from commands.check_ignore import gyat_check_ignore

from const import GYAT_OBJECTS
from utils import read_index, find_resolve_tag_ref, create_blob
from utils_utils import deserialize_gyat_object


def gyat_status(base_dir: Path):
    index_content = read_index(base_dir)

    status_branch(base_dir)
    status_head_index(base_dir, index_content)
    print()
    status_index_worktree(base_dir, index_content)


def status_branch(base_dir: Path):

    branch = None

    with open((base_dir / ".git/HEAD"), "r") as f:
        head = f.read()
        if head.startswith("ref: refs/heads/"):
            branch = head[16:-1]

    if branch:
        print(f"On branch {branch}.")
    else:
        print(f"HEAD detached at {base_dir / '.git/HEAD'}")


def status_head_index(base_dir: Path, index_content):
    print("Changes to be committed:")

    head = tree_to_dict(base_dir, "HEAD")

    for entry in index_content.entries:
        if entry[12] in head:
            if head[entry[12]] != entry[9]:
                print(f"modified: {entry[12]}")
            del head[entry[12]]
        else:
            print(f"added: {entry[12]}")

    for entry in head.keys():
        print(f"deleted: {entry}")


def status_index_worktree(base_dir: Path, index_content):
    print("Changes not staged for commit:")

    gitdir_prefix = ".git" + os.path.sep

    all_files = {}

    for (root, _, files) in os.walk(base_dir, True):
        if root == (base_dir / ".git") or root.startswith(gitdir_prefix):
            continue
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, base_dir)
            all_files[rel_path] = 0

    for entry in index_content.entries:
        full_path = base_dir / entry[12]

        if not os.path.exists(full_path):
            print(f"deleted: {entry[12]}")
        else:
            stat = os.stat(full_path)

            ctime_ns = entry[0][0] * 10**9 + entry[0][1]
            mtime_ns = entry[1][0] * 10**9 + entry[1][1]
            if ((stat.st_ctime_ns != ctime_ns) or
               (stat.st_mtime_ns != mtime_ns)):
                # @FIXME This *will* crash on symlinks to dir.
                if os.islink(full_path):
                    pass
                new_sha = create_blob(base_dir, full_path, False)
                if not entry.sha == new_sha:
                    print(f"modified: {entry[12]}")

        if entry[12] in all_files:
            all_files.pop(entry[12])

    print()
    print("Untracked files:")

    for f in all_files.keys():
        if not gyat_check_ignore(f, base_dir):
            print(" ", f)


def tree_to_dict(base_dir: Path, ref: str):

    result = {}
    sha = find_resolve_tag_ref(base_dir, ref)
    trees = [sha]

    while trees:

        leaf_sha = trees.pop()
        _, content = deserialize_gyat_object(base_dir, leaf_sha)

        mode_name, content = content.split(b"\x00", maxsplit=1)
        mode, _ = map(bytes.decode, mode_name.split())
        sha = content[:20].hex()

        if mode.startswith("04") or mode.startswith("40"):
            trees.append(sha)
        else:
            result[base_dir / GYAT_OBJECTS /
                   leaf_sha[:2] / leaf_sha[2:]] = leaf_sha

    return result
