from pathlib import Path

import pytest

from MyGyat.commands import gyat_write_tree
from MyGyat.utils_utils import find_repo_gyat


@pytest.fixture
def setup_data():

    base_path = find_repo_gyat()

    return [(base_path, "fd5395778e0449c16b30f4e0e772066fd3fa6629")]


def test_gyat_write_tree(setup_data):
    '''
    Verifies `gyat_write_tree' if func return corect
    hash of tree object from the current index.
    '''

    # So write_tree depends on current stage of index so sha of tree would
    # change with changes to this file so to test this func it will be ignored
    # while testing and of course it was in gitignore when creating sha
    # with git to get valid answer to compare with func result
    open(setup_data[0][0] / ".gitignore", "a",
         encoding="utf-8").write(Path(__file__))

    for base_path, answer in setup_data:
        assert gyat_write_tree(base_dir=base_path) == answer

    with open(setup_data[0][0] / ".gitignore", "a") as gignore:
        lines = gignore.readlines()
        lines.pop()
        gignore.writelines(lines)
