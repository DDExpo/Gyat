import time
from hashlib import sha1
from pathlib import Path

from const import USER_NAME, USER_EMAIL
from utils import create_git_object


def gyat_commit_tree(
        parent_repo: Path, sha_tree: str, params: set[str]) -> str:

    parent_com_sha = ""
    message = ""

    commit = (
        f"tree {sha_tree}\nauthor {USER_NAME} <{USER_EMAIL}>"
        f"{int(time.time())} {time.strftime('%z')}"
        f"\ncommitter {USER_NAME} <{USER_EMAIL}>"
        f"{int(time.time())} {time.strftime('%z')}"
    )

    if "-m" in params:
        message = params[params.index("-m")+1]
        commit = commit + f"\n\n{message}"

    if "-p" in params:
        parent_com_sha = params[params.index("-p")+1]
        commit = f"parent {parent_com_sha}\n" + commit

    sha_commit = sha1(commit.encode("utf-8")).hexdigest()
    create_git_object(sha=sha_commit, data=commit.encode("utf-8"))

    return sha_commit
