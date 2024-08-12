from pathlib import Path

import pytest

from MyGyat.commands import gyat_clone_rep, gyat_init


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent.parent.parent.parent / "test"

    return [
        (base_path, url, answer) for url, answer in
        [("https://github.com/DDExpo/Gyat", " ")]
    ]


def test_gyat_clone(setup_data):

    for base_path, url, answer in setup_data:
        gyat_init(base_path, True)
        assert gyat_clone_rep(cur_dir=base_path, url=url) == answer
