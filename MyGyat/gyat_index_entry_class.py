from dataclasses import dataclass


@dataclass
class GyatIndexEntry:
    '''Just a convinient way of store and accesse data\n
        entries.ctime = (ctime_s, ctime_ns),
        entries.mtime = (mtime_s, mtime_ns),
        entries.dev = dev,
        entries.ino = ino,
        entries.mode_type = mode_type,
        entries.mode_perms = mode_perms,
        entries.uid = uid,
        entries.gid = gid,
        entries.fsize = fsize,
        entries.sha = sha,
        entries.flag_assume_valid = flag_assume_valid,
        entries.flag_stage = flag_stage,
        entries.name = name,

        if version 3 and higher
            entries.bit_reserved = bit_reserved
            entries.skip_worktree = skip_worktree
            entries.intent_to_add_flag = intent_to_add_flag
        else they value is -1
    '''

    # The last time a file's data changed.
    # This is a pair (timestamp in seconds, nanoseconds)
    ctime: tuple[int, int]
    mtime: tuple[int, int]
    dev: int  # The ID of device containing this file
    ino: int  # The file's inode number

    # The object type, either b1000 (regular), b1010 (symlink), b1110 (gitlink)
    mode_type: int
    mode_perms: int  # The object permissions, an integer.
    uid: int  # User ID of owner
    gid: int  # Group ID of ownner
    fsize: int  # Size of this object, in bytes
    sha: str  # The object's SHA
    flag_assume_valid: bool
    flag_stage: int
    name: str  # Name of the object
    bit_reserved: int = -1
    skip_worktree: bool = -1
    intent_to_add_flag: bool = -1
