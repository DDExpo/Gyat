from pathlib import Path

import pytest

from MyGyat.commands import gyat_ls_tree


@pytest.fixture
def setup_data():

    base_path = Path(__file__).parent.parent / "data_fixture" / "tree"
    sha = "1d42605abcb9df3388d6d4a44d8cc82a6f13b7be"

    return [
        (base_path, sha, frmt, answer) for frmt, sha, answer in
        [("name_only", sha,
          "__init__.py\nadd.py\ncat_file.py\ncheck_ignore.py\n"
          "commit_tree.py\ngyat_clone.py\nhash_object.py\ninit.py\n"
          "ls_files.py\nls_tree.py\nrm.py\nshow_ref.py\nstatus.py\ntag.py\n"
          "write_tree.py\n"),
         ("object_only", sha,
          "38f79819b8d6c7f1050e5fe26f6af875d57be581\n"
          "68260cbd68cc66e668dfe355518fa3b1bfcbd717\n"
          "6732a58978b3869473a7828481a62b533f388848\n"
          "367cf2157e55955698431c790d33924169476937\n"
          "825c1e9aad5ad28f1b5a6eabac322b0177d42b9c\n"
          "db20d72c5a23ae8bf41d661131c6b2bf271f5dc6\n"
          "c344fb43f58a448fedeb5db6f0775b800116c343\n"
          "95d1b3293d71b1042d53e7b3fe79494735e52ac1\n"
          "8fb097c5090ad085c332d2a82c28d22518ca924a\n"
          "4090eb3c8b19c4c4d1e34107c2770512814ce2e3\n"
          "7c115e52ff815b62dca57c86b392c8c7d372d09f\n"
          "3d8fa7330c14e8ca459eb83de6a19886513d0b87\n"
          "12bf3120afc3339dc5230377c6c41617359e0510\n"
          "16c856c01642d8031d1b513cc60983ea683eebb6\n"
          "8cb39d66b32429960df3289258570555e968c0ae\n"),
         ("full_tree", sha,
          "100644 blob 38f79819b8d6c7f1050e5fe26f6af875d57be581    "
          "__init__.py\n"
          "100644 blob 68260cbd68cc66e668dfe355518fa3b1bfcbd717    add.py\n"
          "100644 blob 6732a58978b3869473a7828481a62b533f388848    "
          "cat_file.py\n"
          "100644 blob 367cf2157e55955698431c790d33924169476937    "
          "check_ignore.py\n"
          "100644 blob 825c1e9aad5ad28f1b5a6eabac322b0177d42b9c    "
          "commit_tree.py\n"
          "100644 blob db20d72c5a23ae8bf41d661131c6b2bf271f5dc6    "
          "gyat_clone.py\n"
          "100644 blob c344fb43f58a448fedeb5db6f0775b800116c343    "
          "hash_object.py\n"
          "100644 blob 95d1b3293d71b1042d53e7b3fe79494735e52ac1    init.py\n"
          "100644 blob 8fb097c5090ad085c332d2a82c28d22518ca924a    "
          "ls_files.py\n"
          "100644 blob 4090eb3c8b19c4c4d1e34107c2770512814ce2e3    "
          "ls_tree.py\n"
          "100644 blob 7c115e52ff815b62dca57c86b392c8c7d372d09f    rm.py\n"
          "100644 blob 3d8fa7330c14e8ca459eb83de6a19886513d0b87    "
          "show_ref.py\n"
          "100644 blob 12bf3120afc3339dc5230377c6c41617359e0510    status.py\n"
          "100644 blob 16c856c01642d8031d1b513cc60983ea683eebb6    tag.py\n"
          "100644 blob 8cb39d66b32429960df3289258570555e968c0ae    "
          "write_tree.py\n"),
         ("full_tree", "8a41243101f6aa67a9c52f7b852a05320c99a9b7",
          "100644 blob e69de29bb2d1d6434b8b29ae775ad8c2e48c5391    "
          "__init__.py\n"
          "100644 blob a9fec71f1345b2b3c253efaeda1d8db709eb2cae    "
          "abstr_command.py\n"
          "100644 blob 290223d492a125e047dff8b4679f30a5644bdc39    "
          "argparser_class.py\n"
          "100644 blob 2460df53be680d0daeca5dc203cb3bbb203e0949    "
          "args_parser.py\n"
          "100644 blob 10e8cf0ea992c08e62ea284302b0dfb812fc80c0    "
          "cmd_with_do_nothing.py\n"
          "040000 tree 1d42605abcb9df3388d6d4a44d8cc82a6f13b7be    commands\n"
          "100644 blob 6f0f3c63bddbe5b0c39d441cf9c80bc602f4ff39    const.py\n"
          "040000 tree 5dab7a48c19b10cace75c466f48724dd61f61d9f    graphic\n"
          "100644 blob 74c85348f0eaeff18f31a0b4d9bfd5d0dc12ebc1    "
          "gyat_exceptions.py\n"
          "100644 blob 75b74f30509b9f0e396ba1d681d4bf1ab61eb127    "
          "gyat_index_entry_class.py\n"
          "100644 blob b9c7481ef0bee8c709fd486ae746f695a55eb630    main.py\n"
          "100644 blob fb03ec6bf62283446582c31870720367d184da30    utils.py\n"
          "100644 blob 2384ce92b73227efd3fd5a0e02c76a49ec87cdce    "
          "utils_utils.py\n")]
    ]


def test_gyat_ls_tree(setup_data, capsys):
    '''
    Verifies `gyat_ls_tree' if func print out correct structure of tree.
    '''

    for base_path, sha, frmt, answer in setup_data:
        gyat_ls_tree(base_path, sha, frmt)
        assert capsys.readouterr().out == answer
