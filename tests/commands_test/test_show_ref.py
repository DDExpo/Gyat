from pathlib import Path

import pytest

from MyGyat.commands import gyat_show_ref


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent / "data_fixture/tag"

    return [
        (base_path, is_tag, answer) for is_tag, answer in
        [
            (False,
             "387fb0c3120e2a3d9ca097a3e472d4b41bbb4a10 refs\\heads\\main\n"
             "387fb0c3120e2a3d9ca097a3e472d4b41bbb4a10 "
             "refs\\remotes\\origin\\HEAD\n"
             "387fb0c3120e2a3d9ca097a3e472d4b41bbb4a10 "
             "refs\\remotes\\origin\\main\n"
             "387fb0c3120e2a3d9ca097a3e472d4b41bbb4a10 "
             "refs\\tags\\test_show_ref\n"
             ),
            (True,
             "387fb0c3120e2a3d9ca097a3e472d4b41bbb4a10 "
             "refs\\tags\\test_show_ref\n")
        ]
    ]


def test_gyat_show_ref(setup_data, capsys):
    '''
    Verifies `gyat_show_ref` if func displays correct references available
    in a local repository along with the associated commit IDs
    '''

    for base_path, is_tag, answer in setup_data:
        gyat_show_ref(base_path, is_tag)
        assert capsys.readouterr().out == answer
