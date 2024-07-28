import zlib
from pathlib import Path

from const import GYAT_OBJECTS


def gyat_cat_file(shas_file: str) -> None:

    data = open(
        GYAT_OBJECTS /
        Path(shas_file[:2] / shas_file[2:]),
        "rb"
    ).read()
    data_decompressed = zlib.decompress(data)
    _, content = data_decompressed.split(b"\0")
    print(content.decode("utf-8"), end="")
