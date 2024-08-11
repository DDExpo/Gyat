from pathlib import Path

from MyGyat.utils_utils import deserialize_gyat_object


def gyat_cat_file(
     shas_file: str, parent_repo: Path) -> tuple[bytes, bytes | str]:
    '''
    Processes a Git object by SHA, returning its header and decoded content.
    Print content of the object to stdout, works as gits with -p arg
    '''

    header, content = deserialize_gyat_object(parent_repo, shas_file)

    object_type = header.decode('utf-8').split()[0]

    print(f"header: {header.decode('utf-8')}")

    if object_type == "tree":
        binary_data = content
        content = ""
        while binary_data:
            mode_name, binary_data = binary_data.split(b"\x00", maxsplit=1)
            mode, name = map(bytes.decode, mode_name.split())
            sha = binary_data[:20].hex()
            type_object = "blob"

            if mode[:2] == "40":
                type_object = "tree"
                mode = "0" + mode
            elif mode[:2] == "16":
                type_object = "commit"
            content += f"{mode} {type_object} {sha}    {name}\n"
            binary_data = binary_data[20:]

    elif object_type in ("commit", "tag"):
        parse_content = content.decode("utf-8").split("\n")
        content = ""
        for data in parse_content:
            if data:
                content += data + '\n'
    else:
        content = content.decode("utf-8")

    print(f"content:\n{content}")
    return (header, content)
