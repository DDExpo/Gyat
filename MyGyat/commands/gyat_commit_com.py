from pathlib import Path

from MyGyat.const import GYAT_REFS
from MyGyat.utils import read_index, get_active_branch
from MyGyat.utils_utils import tree_from_index
from MyGyat.commands import gyat_commit_tree


def gyat_commit(base_dir: Path, message: str):
    index_content, _ = read_index(base_dir)
    tree = tree_from_index(base_dir, index_content)

    parent = open(
        base_dir / ".git" / open(base_dir / ".git/HEAD",
                                 "r").read().split()[1],
        "r"
    ).read().strip()

    commit = gyat_commit_tree(
        parent_repo=base_dir, sha_tree=tree, message=message,
        parent_sha=parent)

    active_branch = get_active_branch(base_dir)
    if active_branch:
        with open(base_dir / GYAT_REFS / "heads" / active_branch, "w") as fd:
            fd.write(commit + "\n")
    else:
        with open(base_dir / ".git/HEAD", "w") as fd:
            fd.write("\n")
