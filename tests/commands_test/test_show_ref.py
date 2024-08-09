from pathlib import Path

from utils_utils import resolve_refs
from const import GYAT_REFS


def gyat_show_ref(base_dir: Path, tag: bool = False):

    base_dir = base_dir / GYAT_REFS / "tags" if tag else base_dir / GYAT_REFS

    for ref_content, ref_path in resolve_refs():
        print(f"{ref_content} {ref_path}")
