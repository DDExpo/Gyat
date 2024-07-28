import zlib

from const import GYAT_OBJECTS


def gyat_ls_tree(param: str, hash: str) -> None:

    # TODO refactor this code
    if param == "--name-only":
        with open(GYAT_OBJECTS / f"{hash[:2]}/{hash[2:]}", "rb") as f:
            data = zlib.decompress(f.read())
            _, binary_data = data.split(b"\x00", maxsplit=1)
            while binary_data:
                mode, binary_data = binary_data.split(b"\x00", maxsplit=1)
                _, name = mode.split()
                binary_data = binary_data[20:]
                print(name.decode("utf-8"))
