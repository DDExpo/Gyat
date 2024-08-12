from pathlib import Path

import pytest

from MyGyat.commands import gyat_status


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent / "data_fixture/test_status"

    return [(base_path, answer) for answer in ["ff"]]


def test_gyat_status(setup_data, capsys):
    '''
    Verifies `gyat_status` if func displays correct references available
    in a local repository along with the associated commit IDs
    '''

    for base_path, answer in setup_data:
        gyat_status(base_path)
        assert capsys.readouterr().out == answer
