from pathlib import Path

import pytest

from MyGyat.commands import gyat_write_tree


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent.parent

    return [(base_path, "d5162deab68ae9a41d87cc1152f20a7e494536c6")]


def test_gyat_write_tree(setup_data):
    '''
    Verifies `gyat_write_tree' if func return corect hash of tree.
    '''

    for base_path, answer in setup_data:
        assert gyat_write_tree(base_dir=base_path) == answer
