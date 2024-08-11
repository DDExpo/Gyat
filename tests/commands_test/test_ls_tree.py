from pathlib import Path

import pytest

from MyGyat.commands import gyat_hash_object


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent

    return [
        (base_path, obj_path, obj_type, answer) for
        obj_path, obj_type, answer in
        [(Path("data_fixture/test_blob/test_blob_two.txt"), "blob",
         "0e5866872763e31177b8acc9a2b4ab3a17d8f7c6")]
    ]


def test_gyat_hash_object(setup_data):
    '''
    Verifies `gyat_hash_object' if func return corect hash.
    '''

    for base_path, obj_path, obj_type, answer in setup_data:
        assert gyat_hash_object(
            path_object=obj_path, object_type=obj_type,
            base_dir=base_path) == answer
