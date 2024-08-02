from pathlib import Path

from const import GYAT_REFS
from utils_utils import deserialize_gyat_object, create_gyat_object


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

        data = (f"object: {object}\ntype: {type_obj}\n"
                f"tag: {tag_name}\ntagger:\n\n{message}")

        create_gyat_object(base_dir, object, data, "tag")
