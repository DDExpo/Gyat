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
        print(e[12])
        if verbose:
            print(f"  {{0b1000: 'regular file', 0b1010: 'symlink', 0b1110: 'git link'}[e[4]]} with perms: {e[5]:o}")
            print(f"  on blob: {e[9]}, file size: {e[8]}")
            print(f"  created: {dt.fromtimestamp(e[0][0])}.{e[0][1]}, modified: {dt.fromtimestamp(e[1][0])}.{e[1][1]}")
            print(f"  device: {e[2]}, inode: {e[3]}")
            print(f"  user: {pwd.getpwuid(e[6]).pw_name} ({e[6]})  group: {grp.getgrgid(e[7]).gr_name} ({e[7]})")
            print(f"  flags: stage={e[11]} assume_valid={e[10]}")
