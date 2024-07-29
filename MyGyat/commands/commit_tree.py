import time
from hashlib import sha1
from pathlib import Path

from utils import create_git_object


def gyat_commit_tree(
        parent_repo: Path, sha_tree: str,
        is_message: bool, is_parent: bool, write_com: bool = True) -> str:

    parent_com_sha = ""
    message = ""

    commit = (
        f"tree {sha_tree}\nauthor {'user'} <{'email'}>"
        f"{int(time.time())} {time.strftime('%z')}"
        f"\ncommitter {'user'} <{'email'}>"
        f"{int(time.time())} {time.strftime('%z')}"
    )

    if is_message:
        commit = commit + f"\n\n{message}"

    if is_parent:
        commit = f"parent {parent_com_sha}\n" + commit

    sha_commit = sha1(commit.encode("utf-8")).hexdigest()
    if write_com:
        create_git_object(
            parent_repo=parent_repo, sha=sha_commit,
            data=commit.encode("utf-8"))

    return sha_commit
