import os
from pathlib import Path

from utils import read_index, write_index


def gyat_rm(base_dir: Path, paths):

    index_content, version = read_index(base_dir)
    abspaths = []

    for path in paths:
        abspath = os.path.abspath(path)
        if abspath.startswith(base_dir):
            abspaths.append(abspath)
        else:
            print(f"Paths outside of worktree wouldnt be removed: {path}")

    kept_entries = list()

    for e in index_content:
        full_path = str(base_dir / e.name)

        if full_path in abspaths:
            os.unlink(full_path)
            abspaths.remove(full_path)
        else:
            kept_entries.append(e)

    if len(abspaths) > 0:
        raise Exception(
            f"Cannot remove paths not in the index: {abspaths}")

    write_index(base_dir, kept_entries, version)
