import re
import os
from math import ceil
from hashlib import sha1
from pathlib import Path
from functools import wraps

from commands.cat_file import gyat_cat_file
from const import INVALID_CHARS_TAG, GYAT_REFS
from gyat_exceptions import IsNotSameTypeError
from utils_utils import (
    create_gyat_object, deserialize_gyat_object, parse_gyatignore)


def catch_common_exceptions_with_args(func):
    def catch_common_exceptions(func):
        @wraps
        def wrapper(*args, **kwargs):
            try:
                func()
            except PermissionError as e:
                print(f"error: {e}")
            except TypeError as e:
                print(f"error: {e}")
            except FileNotFoundError as e:
                print("sha key invalid or object does not exist\n"
                      f"error: {e}")
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                print(f"error: {e}")
            except BaseException as e:
                print(f"Something went wrong {e}")
        return wrapper
    return catch_common_exceptions


def create_blob(base_dir: Path, path_file: Path,
                create_f: bool = False) -> str:
    '''Create sha of the given object, optionally write blob to a disk'''

    data = open(path_file, "rb").read()
    header = f"blob {len(data)}\x00".encode("utf-8")
    sha = sha1(header+data).hexdigest()

    if create_f:
        create_gyat_object(parent_repo=base_dir, sha=sha,
                           data_bytes=header+data)

    return sha


def is_gyat_object(repo: Path, object_sha: str, gyat_obj_type: str) -> bool:

    header = deserialize_gyat_object(repo_parent=repo,
                                     object_sha=object_sha)[0]
    object_type = header.decode('utf-8').strip().split()[0]
    if not object_type == gyat_obj_type:
        raise IsNotSameTypeError(object_type, gyat_obj_type)


def valid_tag_name(name: str):
    '''Almost validate name of the tag by the git standarts'''

    if len(name) < 3:
        print("Name should be minimum lenght of 3!")
        return False

    for char in INVALID_CHARS_TAG:
        if char in name:
            f"Not a valid tag name! char: {char}"
            return False
    return True


# WHATS THE TRASH HOLY SHIT, I CANT EVEN FATHOM HOW BAD THIS LOOKS
def find_resolve_tag_ref(paren_repo: Path, ref_tag: str) -> str:

    dirs: list[Path] = [paren_repo / GYAT_REFS]

    if ref_tag == "HEAD":
        dirs = [paren_repo / '.git/HEAD']

    while dirs:

        cur_path = dirs.pop()

        if cur_path.name == ref_tag:
            while True:
                content = open(paren_repo / ".git/" / cur_path,
                               "r", encoding="utf-8").read()
                refs = re.search(r'^refs: (\w+)', content, re.MULTILINE)
                if refs:
                    cur_path = refs.group(1)
                    continue
                object_match = re.search(
                    r'^commit (\w+)', content, re.MULTILINE)

                if object_match:
                    return object_match.group(1)
                return content

        for next_path in os.listdir(cur_path):
            dirs.append(cur_path / next_path)


def gyatignore_read(base_dir: Path):

    content_index = read_index(base_dir)
    paths_index_rules = {}
    path_exclude_rules = []

    # Read local configuration in .git/info/exclude
    repo_file = os.path.join(base_dir / ".git/info/exclude")
    if os.path.exists(repo_file):
        with open(repo_file, "r") as f:
            path_exclude_rules.append(gyatignore_read(f.readlines()))

    # Global configuration
    if "XDG_CONFIG_HOME" in os.environ:
        config_home = os.environ["XDG_CONFIG_HOME"]
    else:
        config_home = os.path.expanduser("~/.config")
    global_file = os.path.join(config_home, "git/ignore")

    if os.path.exists(global_file):
        with open(global_file, "r") as f:
            path_exclude_rules.append(gyatignore_read(f.readlines()))

    # .gitignore files in the index
    for entry in content_index:
        if entry[12] == ".gitignore" or entry[12].endswith("/.gitignore"):
            dir_name = os.path.dirname(entry[12])
            _, content = gyat_cat_file(parent_repo=base_dir,
                                       shas_file=entry[9])
            lines = content.decode("utf8").splitlines()
            paths_index_rules[dir_name] = parse_gyatignore(lines)
    return (paths_index_rules, path_exclude_rules)


def read_index(base_dir: Path) -> tuple[list[tuple], int]:
    '''Read index. Content of the return
        entries[0][0] = (ctime_s, ctime_ns),
        entries[0][1] = (mtime_s, mtime_ns),
        entries[0][2] = dev,
        entries[0][3] = ino,
        entries[0][4] = mode_type,
        entries[0][5] = mode_perms,
        entries[0][6] = uid,
        entries[0][7] = gid,
        entries[0][8] = fsize,
        entries[0][9] = sha,
        entries[0][10] = flag_assume_valid,
        entries[0][11] = flag_stage,
        entries[0][12] = name,


        if version 3 and higher
            entries[0][13] = bit_reserved
            entries[0][14] = skip_worktree
            entries[0][15] = intent_to_add_flag
        else they value is -1
        And version as integer
    '''

    with open(base_dir / ".git/index", "rb") as f:

        raw = f.read()

        header = raw[:12]
        signature = header[:4]
        if not signature == b"DIRC":  # Stands for "DirCache"
            print("Not a valid signature")
            return None

        version = int.from_bytes(header[4:8], "big")
        count = int.from_bytes(header[8:12], "big")

        entries: list[tuple] = []

        content = raw[12:]
        idx = 0

        bit_reserved = -1
        skip_worktree = -1
        intent_to_add_flag = -1

        for _ in range(0, count):

            ctime_s = int.from_bytes(content[idx: idx+4], "big")
            # Read creation time, as nanoseconds after that timestamps,
            # for extra precision.
            ctime_ns = int.from_bytes(content[idx+4: idx+8], "big")
            # Same for modification time: first seconds from epoch.
            mtime_s = int.from_bytes(content[idx+8: idx+12], "big")
            # Then extra nanoseconds
            mtime_ns = int.from_bytes(content[idx+12: idx+16], "big")
            # Device ID
            dev = int.from_bytes(content[idx+16: idx+20], "big")
            # Inode
            ino = int.from_bytes(content[idx+20: idx+24], "big")
            # Ignored
            _ = int.from_bytes(content[idx+24: idx+26], "big")
            mode = int.from_bytes(content[idx+26: idx+28], "big")
            mode_type = mode >> 12

            mode_perms = mode & 0b0000000111111111
            # User ID
            uid = int.from_bytes(content[idx+28: idx+32], "big")
            # Group ID
            gid = int.from_bytes(content[idx+32: idx+36], "big")
            # file size
            fsize = int.from_bytes(content[idx+36: idx+40], "big")
            # SHA (object ID)
            sha = format(
                int.from_bytes(content[idx+40: idx+60], "big"), "040x")
            # Flags we're going to ignore
            flags = int.from_bytes(content[idx+60: idx+62], "big")
            # Parse flags
            flag_assume_valid = (flags & 0b1000000000000000) != 0
            flag_extended = (flags & 0b0100000000000000) != 0

            if flag_extended and version == 2:
                print("Somehow version (current 2) of the format"
                      "doesnt match with flag extended, so we abort")
                return None

            flag_stage = flags & 0b0011000000000000
            name_length = flags & 0b0000111111111111

            if flag_extended and version >= 3:
                # Reserved for future
                bit_reserved = flags & 0b00000000000000001000000000000000
                # skip-worktree flag (used by sparse checkout)
                skip_worktree = flags & 0b00000000000000000100000000000000
                # intent-to-add flag (used by "git add -N")
                intent_to_add_flag = flags & 0b00000000000000000010000000000000
                # Unused
                _ = flags & 0b00000000000000000001111111111111

            idx += 62

            if name_length < 0xFFF:
                raw_name = content[idx:idx+name_length]
                idx += name_length + 1
            else:
                null_idx = content.find(b'\x00', idx + 0xFFF)
                raw_name = content[idx: null_idx]
                idx = null_idx + 1

            name = raw_name.decode("utf8")

            if version != 4:
                idx = 8 * ceil(idx / 8)

            entries.append((
                (ctime_s, ctime_ns), (mtime_s,  mtime_ns),
                dev, ino, mode_type, mode_perms, uid, gid,
                fsize, sha, flag_assume_valid, flag_stage, name,
                bit_reserved, skip_worktree, intent_to_add_flag,
            ))

        return (entries, version)
