import os
from pathlib import Path

from MyGyat.gyat_index_entry_class import GyatIndexEntry
from MyGyat.utils import write_index, read_index, create_blob


def gyat_add(paths, base_dir: Path):

    clean_paths = list()
    set_paths = {Path(path).absolute() for path in paths}
    for path in paths:
        abspath = os.path.abspath(path)
        if not (abspath.startswith(base_dir) and os.path.isfile(abspath)):
            raise Exception(f"Not a file, or outside the worktree: {path}")
        relpath = os.path.relpath(abspath, base_dir)
        clean_paths.append((abspath,  relpath))

    index_content, version = read_index(base_dir)
    kept_index_entries = []

    for e in index_content:
        if not (base_dir / e.name).absolute() in set_paths:
            kept_index_entries.append(e)

    for (abspath, relpath) in clean_paths:
        sha = create_blob(base_dir, abspath)

        stat = os.stat(abspath)

        ctime_s = int(stat.st_birthtime)
        ctime_ns = stat.st_ctime_ns % 10**9
        mtime_s = int(stat.st_mtime)
        mtime_ns = stat.st_mtime_ns % 10**9

        kept_index_entries.append(
            GyatIndexEntry(
                ctime=(ctime_s, ctime_ns), mtime=(mtime_s, mtime_ns),
                dev=stat.st_dev, ino=stat.st_ino, mode_type=0b1000,
                mode_perms=0o644, uid=stat.st_uid, gid=stat.st_gid,
                fsize=stat.st_size, sha=sha, flag_assume_valid=False,
                flag_stage=False, name=relpath))

    write_index(base_dir, kept_index_entries, version)
