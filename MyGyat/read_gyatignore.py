import os
from pathlib import Path

from commands.cat_file import gyat_cat_file
from const import GYAT_OBJECTS
from utils_utils import parse_gyatignore
from utils import read_index


def gyatignore_read(base_dir: Path):

    content_index, _ = read_index(base_dir)
    paths_index_rules = {}
    path_exclude_rules = []

    # Read local configuration in .git/info/exclude
    repo_file = os.path.join(base_dir / ".git/info/exclude")
    if os.path.exists(repo_file):
        with open(repo_file, "r") as f:
            path_exclude_rules.append(gyatignore_read(f.readlines()))

    # Global configuration
    if "XDG_CONFIG_HOME" in os.environ:
        config_home = os.environ["XDG_CONFIG_HOME"]
    else:
        config_home = os.path.expanduser("~/.config")
    global_file = os.path.join(config_home, "git/ignore")

    if os.path.exists(global_file):
        with open(global_file, "r") as f:
            path_exclude_rules.append(gyatignore_read(f.readlines()))

    # .gitignore files in the index
    for entry in content_index:
        if entry.name == ".gitignore" or entry.name.endswith("/.gitignore"):
            dir_name = os.path.dirname(entry.name)
            sha = entry.sha
            if not (base_dir / GYAT_OBJECTS / sha[:2] / sha[2:]).exists():
                continue

            _, content = gyat_cat_file(parent_repo=base_dir,
                                       shas_file=sha)
            lines = content.decode("utf-8").splitlines()
            paths_index_rules[dir_name] = parse_gyatignore(lines)

    return (paths_index_rules, path_exclude_rules)
