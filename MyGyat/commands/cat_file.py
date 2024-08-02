from pathlib import Path

from utils_utils import deserialize_gyat_object


def gyat_cat_file(parent_repo: Path, shas_file: str) -> None:

    header, content = deserialize_gyat_object(parent_repo, shas_file)
    object_type = header.decode('utf-8').split()[0]

    print(f"header: {header.decode('utf-8')}")

    try:
        if object_type == "tree":
            content = content
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
