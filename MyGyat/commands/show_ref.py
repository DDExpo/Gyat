from pathlib import Path

from MyGyat.utils_utils import resolve_refs


def gyat_show_ref(base_dir: Path, tag: bool = False):

    for ref_content, ref_path in resolve_refs(base_dir / ".git", tag):
        print(f"{ref_content} {ref_path}")
