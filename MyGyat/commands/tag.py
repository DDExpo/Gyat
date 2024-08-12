import time
from pathlib import Path
from hashlib import sha1

from MyGyat.const import GYAT_REFS
from MyGyat.utils import gitconfig_read
from MyGyat.utils_utils import deserialize_gyat_object, create_gyat_object


def gyat_tag(
        base_dir: Path, tag_name: str,
        message: str, obj: str, annotated_tag: bool):

    if not annotated_tag:
        with open(base_dir / GYAT_REFS / "tags" / tag_name,
                  "w", encoding="utf-8") as f:
            f.write(obj)
    else:
        type_obj = deserialize_gyat_object(
            base_dir, obj)[0].decode("utf-8").split()[0]

        config = gitconfig_read()

        data = (
            f"object {obj}\ntype {type_obj}\ntag {tag_name}\n"
            f"tagger {config['user']['name']} <{config['user']['email']}> "
            f"{int(time.time())} {time.strftime('%z')}\n\n{message}\n"
        ).encode()

        header = f"tag {len(data)}\0".encode()

        sha = sha1(header + data).hexdigest()

        create_gyat_object(base_dir, sha, header+data)
