from typing import cast
import requests
import zlib
import struct
import hashlib
from pathlib import Path

import urllib.request


from utils_utils import create_gyat_object, deserialize_gyat_object


def gyat_clone_rep(cur_dir: Path, url: str):

    response = requests.get(f"{url}/info/refs?service=git-upload-pack")
    lines = response.text.split("\n")
    refs = {}

    for line in lines:
        line = line[4:]

        if line.startswith("#"):
            continue

        line = line.split("\0")[0]
        if line.endswith("HEAD"):
            line = line[4:]

        parts = line.split(" ")
        if len(parts) == 2:
            refs[parts[1]] = parts[0]

    for name, sha in refs.items():
        with open(cur_dir / ".git" / name, "w") as f:
            f.write(sha + "\n")

    body = (
        b"0011command=fetch0001000fno-progress" +
        b"".join(b"0032want " + ref.encode() + b"\n" for ref in refs.values())
        + b"0009done\n0000"
    )

    req = urllib.request.Request(
                f"{url}/git-upload-pack",
                data=body,
                headers={"Git-Protocol": "version=2"},
            )
    pack_bytes = ""
    with urllib.request.urlopen(req) as f:
        pack_bytes = cast(bytes, f.read())

    pack_lines = []
    while pack_bytes:
        line_len = int(pack_bytes[:4], 16)
        if line_len == 0:
            break
        pack_lines.append(pack_bytes[4:line_len])
        pack_bytes = pack_bytes[line_len:]

    pack_files = b"".join(pack[1:] for pack in pack_lines[1:])

    def next_size_type(bs: bytes):
        ty = (bs[0] & 0b_0111_0000) >> 4
        match ty:
            case 1:
                ty = "commit"
            case 2:
                ty = "tree"
            case 3:
                ty = "blob"
            case 4:
                ty = "tag"
            case 6:
                ty = "ofs_delta"
            case 7:
                ty = "ref_delta"
            case _:
                ty = "unknown"
        size = bs[0] & 0b_0000_1111
        i = 1
        off = 4
        while bs[i - 1] & 0b_1000_0000:
            size += (bs[i] & 0b_0111_1111) << off
            off += 7
            i += 1
        return ty, size, bs[i:]

    def next_size(bs: bytes):
        size = bs[0] & 0b_0111_1111
        i = 1
        off = 7
        while bs[i - 1] & 0b_1000_0000:
            size += (bs[i] & 0b_0111_1111) << off
            off += 7
            i += 1
        return size, bs[i:]

    _ = pack_files[:8]
    pack_file = pack_files[8:]
    n_objs, *_ = struct.unpack("!I", pack_file[:4])
    pack_file = pack_file[4:]
    base_content = b""
    count = 0
    for _ in range(n_objs):
        ty, _, pack_file = next_size_type(pack_file)
        match ty:
            case "commit" | "tree" | "blob" | "tag":
                dec = zlib.decompressobj()
                content = dec.decompress(pack_file)
                pack_file = dec.unused_data
                header = f"{ty.encode()} {len(content)}\x00".encode()
                sha = hashlib.sha1(header+content).hexdigest()
                create_gyat_object(cur_dir, sha, header+content)
            case "ref_delta":
                obj = pack_file[:20].hex()
                pack_file = pack_file[20:]
                dec = zlib.decompressobj()
                content = dec.decompress(pack_file)
                pack_file = dec.unused_data
                target_content = b""
                try:
                    _, base_content = deserialize_gyat_object(cur_dir, obj)
                except (FileNotFoundError, FileExistsError):
                    count += 1

                _, content = next_size(content)
                _, content = next_size(content)
                while content:
                    is_copy = content[0] & 0b_1000_0000
                    if is_copy:
                        data_ptr = 1
                        offset = 0
                        size = 0
                        for i in range(0, 4):
                            if content[0] & (1 << i):
                                offset |= content[data_ptr] << (i * 8)
                                data_ptr += 1
                        for i in range(0, 3):
                            if content[0] & (1 << (4 + i)):
                                size |= content[data_ptr] << (i * 8)
                                data_ptr += 1

                        content = content[data_ptr:]
                        target_content += bytes(
                            base_content[offset: offset + size])
                    else:
                        size = content[0]
                        append = content[1:size + 1]
                        content = content[size + 1:]
                        target_content += append

                header = f"{ty.encode()} {len(target_content)}\x00".encode()
                sha = hashlib.sha1(header+content).hexdigest()
                create_gyat_object(cur_dir, sha, header+content)
            case _:
                raise RuntimeError("Not implemented")
    print(f"Packages lost {count}")
