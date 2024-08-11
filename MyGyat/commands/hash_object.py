from pathlib import Path

from MyGyat.utils import create_blob


def gyat_hash_object(
     path_object: Path, base_dir: Path,
     object_type: str, write_obj: bool = False) -> None:

    sha_content = ""

    if object_type == "blob":
        sha_content = create_blob(base_dir, path_object, write_obj)

    print(sha_content, end="")
    return sha_content
