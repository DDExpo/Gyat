import configparser
import re
import os
from math import ceil
from hashlib import sha1
from pathlib import Path
from functools import wraps

from MyGyat.gyat_index_entry_class import GyatIndexEntry
from MyGyat.commands.cat_file import gyat_cat_file
from MyGyat.const import INVALID_CHARS_TAG, GYAT_REFS
from MyGyat.gyat_exceptions import IsNotSameTypeError
from MyGyat.utils_utils import (
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

    data = open(Path(os.getcwd()) / path_file, "rb").read().replace(b'\r\n',
                                                                    b'\n')
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


def get_gitignore(base_dir: Path) -> list[str]:

    with open(base_dir / ".gitignore", "r") as f:
        return [line.strip() for line in f.readlines()]


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

    content_index, _ = read_index(base_dir)
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


def read_index(base_dir: Path) -> tuple[list[GyatIndexEntry], int]:

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

            if version < 4:
                idx = 8 * ceil(idx / 8)

            entries.append(
                GyatIndexEntry(
                    ctime=(ctime_s, ctime_ns), mtime=(mtime_s,  mtime_ns),
                    dev=dev, ino=ino, mode_type=mode_type,
                    mode_perms=mode_perms, uid=uid, gid=gid,
                    fsize=fsize, sha=sha, flag_assume_valid=flag_assume_valid,
                    flag_stage=flag_stage, name=name,
                    bit_reserved=bit_reserved, skip_worktree=skip_worktree,
                    intent_to_add_flag=intent_to_add_flag)
                )

        return (entries, version)


def write_index(base_dir: Path, index: list[GyatIndexEntry], version: int):

    with open(base_dir / ".git/index", "wb") as f:

        f.write(b"DIRC")
        f.write(version.to_bytes(4, "big"))
        f.write(len(index).to_bytes(4, "big"))

        idx = 0
        for e in index:
            f.write(e.ctime[0].to_bytes(4, "big"))
            f.write(e.ctime[1].to_bytes(4, "big"))
            f.write(e.mtime[0].to_bytes(4, "big"))
            f.write(e.mtime[1].to_bytes(4, "big"))
            f.write(e.dev.to_bytes(4, "big"))
            f.write(e.ino.to_bytes(4, "big"))

            mode = (e.mode_type << 12) | e.mode_perms
            f.write(mode.to_bytes(4, "big"))

            f.write(e.uid.to_bytes(4, "big"))
            f.write(e.gid.to_bytes(4, "big"))

            f.write(e.fsize.to_bytes(4, "big"))
            f.write(int(e.sha, 16).to_bytes(20, "big"))

            flag_assume_valid = 0x1 << 15 if e.flag_assume_valid else 0

            name_bytes = e.name.encode("utf8")
            bytes_len = len(name_bytes)
            if bytes_len >= 0xFFF:
                name_length = 0xFFF
            else:
                name_length = bytes_len

            f.write(
                (flag_assume_valid | e.flag_stage |
                 name_length).to_bytes(2, "big"))
            f.write(name_bytes)
            f.write((0).to_bytes(1, "big"))

            idx += 62 + len(name_bytes) + 1

            if idx % 8 != 0 and version < 4:
                pad = 8 - (idx % 8)
                f.write((0).to_bytes(pad, "big"))
                idx += pad


def gitconfig_read():
    xdg_config_home = (os.environ["XDG_CONFIG_HOME"]
                       if "XDG_CONFIG_HOME" in os.environ
                       else "~/.config")
    configfiles = [
        os.path.expanduser(os.path.join(xdg_config_home, ".git/config")),
        os.path.expanduser("~/.gitconfig")
    ]

    config = configparser.ConfigParser()
    config.read(configfiles)
    return config


def get_active_branch(base_dir: Path):

    with open(base_dir / ".sgit/HEAD", "r") as f:
        head = f.read()

        if head.startswith("ref: refs/heads/"):
            return head[16:-1]
        else:
            return False
