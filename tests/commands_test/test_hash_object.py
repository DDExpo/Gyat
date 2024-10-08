from pathlib import Path

import pytest

from MyGyat.commands import gyat_hash_object


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent

    return [
        (base_path, obj_path, obj_type, answer) for
        obj_path, obj_type, answer in
        [(Path("tests/data_fixture/test_blob/test_blob_two.txt"), "blob",
         "e6b6d9bf6a5861ce54eba9ffc35efee018f75d06")]
    ]


def test_gyat_hash_object(setup_data):
    '''
    Verifies `gyat_hash_object' if func return corect hash.
    '''

    for base_path, obj_path, obj_type, answer in setup_data:
        assert gyat_hash_object(
            path_object=obj_path, object_type=obj_type,
            base_dir=base_path) == answer
