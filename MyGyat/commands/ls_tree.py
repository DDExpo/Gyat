import zlib

from const import GYAT_OBJECTS


def gyat_ls_tree(base_dir, args, sha_tree: str) -> None:

    with open(
         base_dir / GYAT_OBJECTS / (sha_tree[:2] + "/" + sha_tree[2:]),
         "rb") as f:
        data = zlib.decompress(f.read())
        _, binary_data = data.split(b"\x00", maxsplit=1)

        while binary_data:
            mode_name, binary_data = binary_data.split(b"\x00", maxsplit=1)
            mode, name = map(bytes.decode, mode_name.split())
            sha = binary_data[:20].hex()
            type_object = "blob"

            if mode[:2] == "40":
                type_object = "tree"
            elif mode[:2] == "16":
                type_object = "commit"

            binary_data = binary_data[20:]

            if args.name_only:
                print(name)
            elif args.object_only:
                print(sha)
            elif args.full_tree:
                print(f"{mode} {type_object} {sha} {name}")
            else:
                print(name)
