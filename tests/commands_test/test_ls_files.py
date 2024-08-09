import grp
import pwd
from datetime import datetime as dt
from pathlib import Path

from utils import read_index


def gyat_ls_files(base_dir: Path, verbose: bool):

    staging_data, version = read_index(base_dir)

    if verbose:
        print(
            f"Index file format v: {version}, containing"
            f" {len(staging_data)} entries.")

    for e in staging_data:
        print(e.name)
        if verbose:
            print(f"{0b1000: 'regular file', 0b1010: 'symlink', 0b1110: 'git link' [e.mode_type] with perms: e.mode_perms:o}")
            print(f"on blob: {e.sha}, file size: {e.fsize}")
            print(f"created: {dt.fromtimestamp(e.ctime[0])}.{e.ctime[1]}, modified: {dt.fromtimestamp(e.mtime[0])}.{e.mtime[1]}")
            print(f"device: {e.dev}, inode: {e.ino}")
            print(f"user: {pwd.getpwuid(e.uid).pw_name} ({e[6]})  group: {grp.getgrgid(e.gid).gr_name} ({e.gid})")
            print(f"flags: stage={e.flag_stage} assume_valid={e.flag_assume_valid}")
