import time
from hashlib import sha1
from pathlib import Path

from MyGyat.utils import gitconfig_read, is_gyat_object
from MyGyat.utils_utils import create_gyat_object


def gyat_commit_tree(
        parent_repo: Path, sha_tree: str, parent_sha: str,
        message: str, write_com: bool = True) -> str:

    config = gitconfig_read()

    commit = (
        f"tree {sha_tree}\nauthor {config['user']['name']}"
        f" <{config['user']['email']}>"
        f"{int(time.time())} {time.strftime('%z')}"
        f"\ncommitter {config['user']['name']} <{config['user']['email']}>"
        f"{int(time.time())} {time.strftime('%z')}"
    )

    if message:
        commit = commit + f"\n\n{message}"

    if parent_sha:
        is_gyat_object(parent_sha, parent_sha, "tree")
        commit = f"parent {parent_sha}\n" + commit

    commit_bytes = commit.encode("utf-8")
    header = f"commit {len(commit_bytes)}\0".encode("utf-8")

    sha_commit = sha1(header+commit_bytes).hexdigest()
    if write_com:
        create_gyat_object(
            parent_repo=parent_repo, sha=sha_commit,
            data_bytes=(header+commit_bytes)
        )

    print(sha_commit)
    return sha_commit
