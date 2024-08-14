import fnmatch
from pathlib import Path

from read_gyatignore import gyatignore_read


def gyat_check_ignore(paths, base_dir: Path):

    rules = gyatignore_read(base_dir)
    for path in paths:
        if check_ignore(rules[0], rules[1], Path(path)):
            print(path)


def check_ignore(index_rules, exclude_rules, path: Path):

    result = check_ignore_index(index_rules, path)
    return result if result else check_ignore_exclude(exclude_rules, path)


def check_ignore_index(rules, path_cur: Path):
    parent = path_cur.parent
    result = None
    count = 0
    # TRASH and i am not smart
    while count <= 100:
        if parent in rules:
            for (pattern, value) in rules[parent]:
                if fnmatch(path_cur, pattern):
                    result = value
            if result:
                return result
        parent = path_cur.parent
        count += 1
    return None


def check_ignore_exclude(rules, path_cur: Path):
    parent = path_cur.parent
    result = None
    for ruleset in rules:
        for (pattern, value) in ruleset:
            if fnmatch(parent, pattern):
                result = value
        if result is not None:
            return result
    return False
