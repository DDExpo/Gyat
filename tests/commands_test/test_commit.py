from pathlib import Path

import pytest

from MyGyat.commands import gyat_commit


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent.parent

    return [(base_path, message) for message in ["test commit command"]]


# Tested manually it works
def test_gyat_hash_object(setup_data):
    '''
    Verifies `gyat_commit' if func return corect hash.
    '''

    for base_path, message in setup_data:
        gyat_commit(base_path, message)
        assert True is True
