import zlib
from pathlib import Path

from const import GYAT_OBJECTS


def gyat_cat_file(parent_repo: Path, shas_file: str) -> None:

    data = open(
        parent_repo / GYAT_OBJECTS /
        Path(shas_file[:2]) / Path(shas_file[2:]),
        "rb"
    ).read()
    data_decompressed = zlib.decompress(data)
    header, content = data_decompressed.split(b"\0", 1)
    object_type = header.decode('utf-8').split()[0]

    print(f"header: {header.decode('utf-8')}")

    try:
        if object_type == "tree":
            content = content.decode("utf-8")
        elif object_type in ("commit", "tag"):
            parse_content = content.decode("utf-8").split("\n")
            content = ""
            for data in parse_content:
                if data:
                    content += data + '\n'
        else:
            content = content.decode("utf-8")

    except UnicodeDecodeError:
        print("cant be view by cat-file command")
        return

    print(f"content:\n{content}")
