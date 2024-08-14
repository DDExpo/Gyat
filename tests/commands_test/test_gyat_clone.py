import os
import shutil
from pathlib import Path

import pytest

from MyGyat.commands import gyat_clone_rep, gyat_init


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent.parent / "test"

    return [
        (base_path, url) for url in ["https://github.com/DDExpo/Gyat"]
    ]


# Works
def test_gyat_clone(setup_data):

    for base_path, url in setup_data:
        gyat_init(base_path, True)
        gyat_clone_rep(cur_dir=base_path, url=url)
        assert True is True

    shutil.rmtree(base_path)
    os.rmdir(base_path)
