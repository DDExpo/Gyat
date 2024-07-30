import zlib

from const import GYAT_OBJECTS


def gyat_ls_tree(base_dir, args, sha_tree: str) -> None:

    # TODO make it
    if args.name_only:
        with open(base_dir / GYAT_OBJECTS / (sha_tree[:2] + sha_tree[2:]),
                  "rb") as f:
            data = zlib.decompress(f.read())
            _, binary_data = data.split(b"\x00", maxsplit=1)
            while binary_data:
                mode, binary_data = binary_data.split(b"\x00", maxsplit=1)
                _, name = mode.split()
                binary_data = binary_data[20:]
                print(name.decode("utf-8"))

    elif args.object_only:
        pass
    elif args.full_name:
        pass
    elif args.full_tree:
        pass
    else:
        pass
