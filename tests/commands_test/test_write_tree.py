from pathlib import Path

import pytest

from MyGyat.commands import gyat_write_tree


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent.parent

    return [(base_path, "fd5395778e0449c16b30f4e0e772066fd3fa6629")]


def test_gyat_write_tree(setup_data):
    '''
    Verifies `gyat_write_tree' if func return corect
    hash of tree object from the current index.
    '''

    for base_path, answer in setup_data:
        assert gyat_write_tree(base_dir=base_path) == answer
