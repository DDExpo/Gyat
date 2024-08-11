from pathlib import Path

import pytest

from MyGyat.commands import gyat_write_tree


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent.parent

    return [(base_path, "8003ac9f64c9a130d1ede4b3b96b1f219a8a318d")]


def test_gyat_write_tree(setup_data):
    '''
    Verifies `gyat_write_tree' if func return corect hash of tree.
    '''

    for base_path, answer in setup_data:
        assert gyat_write_tree(base_dir=base_path) == answer
