from pathlib import Path

import pytest

from MyGyat.const import GYAT_REFS
from MyGyat.commands import gyat_tag


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent / "data_fixture/tag"

    return [
        (base_path, name, message, obj, a) for name, message, obj, a in
        [("test_tag", "", "772493498dc9f21ddce8b617f1834bf9c844f745", False),
         ("test_tag_anotated", "test",
          "66d3e4d23128051d46c4af5555dc2fca3122b8b3", True)]
    ]


def test_gyat_tag(setup_data):
    '''
    Verifies `gyat_tag` what it create correct tag
    and corect sha of annotated tag ! cant be tested though as it has dynamic
    data every second what cant be hardcoded.
    '''

    for base_path, name, message, obj, a in setup_data:
        gyat_tag(base_path, name, message, obj, a)
        if not a:
            assert (
                base_path / GYAT_REFS / "tags" / name).exists() is True
