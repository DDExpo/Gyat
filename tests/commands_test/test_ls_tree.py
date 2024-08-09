from pathlib import Path

from utils_utils import deserialize_gyat_object


def gyat_ls_tree(
     base_dir: Path, sha_tree: str, output_format: str) -> None:

    _, binary_data = deserialize_gyat_object(base_dir, sha_tree)

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

        if output_format == "name_only":
            print(name)
        elif output_format == "object_only":
            print(sha)
        elif output_format == "full_tree":
            print(f"{mode} {type_object} {sha} {name}")
