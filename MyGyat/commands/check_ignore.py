import fnmatch
import os
from pathlib import Path

from MyGyat.utils import gyatignore_read


def gyat_check_ignore(paths, base_dir: Path):

    rules = gyatignore_read(base_dir)
    for path in paths:
        if check_ignore(rules, Path(path)):
            print(path)


def check_ignore(index_rules, exclude_rules, path: Path):

    result = check_ignore_index(index_rules, path)
    if result is not None:
        return result

    return check_ignore_exclude(exclude_rules, path)


def check_ignore_index(rules, path: Path):
    parent = os.path.dirname(path)
    result = None
    while True:
        if parent in rules:
            for (pattern, value) in rules[parent]:
                if fnmatch(path, pattern):
                    result = value
            if result is not None:
                return result
        if parent == "":
            break
        parent = os.path.dirname(parent)
    return None


def check_ignore_exclude(rules, path: Path):
    parent = os.path.dirname(path)
    result = None
    for ruleset in rules:
        for (pattern, value) in ruleset:
            if fnmatch(parent, pattern):
                result = value
        if result is not None:
            return result
    return False
