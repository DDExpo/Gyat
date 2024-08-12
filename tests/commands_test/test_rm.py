from pathlib import Path

import pytest

from MyGyat.commands import gyat_cat_file


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent / "data_fixture"

    # Data paths is hardcoded and data is precreated i think its not the
    # best way to do testing, but data is small, so i think its okay
    return [
        (base_path / data, sha, answer) for data, sha, answer in
        []
        ]


def test_gyat_cat_file(setup_data):
    '''
    Verifies `gyat_cat_file` processes checks if the function return header and
    content of the objects[blob, tree, commit, tag] as expected.
    '''

    for base_path, sha, answer in setup_data:
        assert gyat_cat_file(parent_repo=base_path, shas_file=sha) == answer
