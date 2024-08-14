import os
import ctypes
from datetime import datetime as dt
from pathlib import Path

from utils import read_index

if not os.name == 'nt':
    import grp
    import pwd


def gyat_ls_files(base_dir: Path, verbose: bool):

    staging_data, version = read_index(base_dir)

    if verbose:
        print(
            f"Index file format v: {version}, containing"
            f" {len(staging_data)} entries.")

    for e in staging_data:
        print(e.name)
        if verbose:
            print(
                f"{0b1000: 'regular file', 0b1010: 'symlink', 0b1110: 'git link' [e.mode_type] with perms: e.mode_perms:o}")
            print(f"on blob: {e.sha}, file size: {e.fsize}")
            print(f"created: {dt.fromtimestamp(e.ctime[0])}.{e.ctime[1]},"
                  f" modified: {dt.fromtimestamp(e.mtime[0])}.{e.mtime[1]}")
            print(f"device: {e.dev}, inode: {e.ino}")
            if os.name == 'nt':  # Windows
                try:
                    user_info = ctypes.create_string_buffer(256)
                    user_name = user_info.value.decode('utf-16')
                except Exception:
                    user_name = f"UID {e.uid}"

                # Windows does not provide a straightforward
                # way to get group names.
                group_name = f"GID {e.gid}"
            else:  # Unix-like
                user_name = pwd.getpwuid(e.uid).pw_name
                group_name = grp.getgrgid(e.gid).gr_name

            print(
                f"user: {user_name} ({e.uid})  group: {group_name} ({e.gid})")
            print(
                f"flags: stage={e.flag_stage}"
                f" assume_valid={e.flag_assume_valid}")
