from pathlib import Path

import pytest

from MyGyat.commands import gyat_add


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent.parent

    return [(base_path, answer) for answer in [True]]


def test_gyat_cat_file(setup_data):
    '''
    Verifies `gyat_add`
    '''

    for base_path, answer in setup_data:
        assert gyat_add(["hh/tes.txt"], base_path) == answer
