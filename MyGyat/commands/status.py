import os
from pathlib import Path

from gyat_index_entry_class import GyatIndexEntry
from commands.check_ignore import gyat_check_ignore
from const import GYAT_OBJECTS
from utils import (
    read_index, find_resolve_tag_ref, create_blob, get_active_branch)
from utils_utils import deserialize_gyat_object


def gyat_status(base_dir: Path):
    index_content, _ = read_index(base_dir)

    status_branch(base_dir)
    status_head_index(base_dir, index_content)
    print()
    status_index_worktree(base_dir, index_content)


def status_branch(base_dir: Path):

    branch = get_active_branch(base_dir)

    if branch:
        print(f"On branch {branch}.")
    else:
        print(f"HEAD detached at {base_dir / '.git/HEAD'}")


def status_head_index(base_dir: Path, index_content: GyatIndexEntry):
    print("Changes to be committed:")

    head = tree_to_dict(base_dir, "HEAD")

    for entry in index_content:
        if entry.name in head:
            if head[entry.name] != entry.sha:
                print(f"modified: {entry.name}")
            del head[entry.name]
        else:
            print(f"added: {entry.name}")

    for entry in head.keys():
        print(f"deleted: {entry}")


def status_index_worktree(base_dir: Path, index_content: GyatIndexEntry):
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

    for entry in index_content:
        full_path = base_dir / entry.name

        if not os.path.exists(full_path):
            print(f"deleted: {entry.name}")
        else:
            stat = os.stat(full_path)

            ctime_ns = entry.ctime[0] * 10**9 + entry.ctime[1]
            mtime_ns = entry.mtime[0] * 10**9 + entry.mtime[1]
            if ((stat.st_ctime_ns != ctime_ns) or
               (stat.st_mtime_ns != mtime_ns)):
                if os.islink(full_path):
                    pass
                new_sha = create_blob(base_dir, full_path, False)
                if not entry.sha == new_sha:
                    print(f"modified: {entry.name}")

        if entry.name in all_files:
            all_files.pop(entry.name)

    print("\nUntracked files:")

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
        obj_type, content = content.split(b" ", maxsplit=1)
        sha = content[:40]

        if obj_type == "tree":
            trees.append(sha)
        else:
            result[base_dir / GYAT_OBJECTS /
                   leaf_sha[:2] / leaf_sha[2:]] = leaf_sha

    return result
