import time
from hashlib import sha1
from pathlib import Path

from utils_utils import create_gyat_object


def gyat_commit_tree(
        parent_repo: Path, sha_tree: str, message: str, parent_sha: str,
        is_message: bool, is_parent: bool, write_com: bool = True) -> str:

    commit = (
        f"tree {sha_tree}\nauthor {'user'} <{'email'}>"
        f"{int(time.time())} {time.strftime('%z')}"
        f"\ncommitter {'user'} <{'email'}>"
        f"{int(time.time())} {time.strftime('%z')}"
    )

    if is_message:
        commit = commit + f"\n\n{message}"

    if is_parent:
        commit = f"parent {parent_sha}\n" + commit

    sha_commit = sha1(commit.encode("utf-8")).hexdigest()
    if write_com:
        create_gyat_object(
            parent_repo=parent_repo, sha=sha_commit,
            data_bytes=f"commit {len(commit.encode())}\x00{commit}".encode("utf-8"))

    print(sha_commit)
    return sha_commit
