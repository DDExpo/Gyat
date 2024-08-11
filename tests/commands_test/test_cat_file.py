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
        [("blob", "5c36c9827f6e8dc98b37d962b4a1ecdfe3340d38",
            (b"blob 11", "test blob 1")),
         ("commit", "f98d4b00d3303e853bc0089b4138339894555ffd",
          (b"commit 178",
           ("tree 3ab177a92a9069e100d579db6b39c8c83f17ab68\n"
            "author DDExpo <f8ck.th1sm3n@gmail.com> 1723236585 +0600\n"
            "committer DDExpo <f8ck.th1sm3n@gmail.com> 1723236585 +0600\n"
            "commit_test_one\n")
           )),
         ("tree", "3ab177a92a9069e100d579db6b39c8c83f17ab68",
          (b"tree 175",
           ("100644 blob 31c24a15282c974108049ad8b01a95589b9ab4d2"
            "    .gitignore\n"
            "100644 blob 28c33c1f96b8fe1b49d05d41632d48b0fb4616d6    LICENSE\n"
            "040000 tree e9a9c78fe87d536c9fe1d08353365ded4a93a8ef    MyGyat\n"
            "100644 blob 4a25dbba0a6b4b3a61bbfd12242064994a7cdc33"
            "    README.md\n"
            "040000 tree 9d1dcfdaf1a6857c5f83dc27019c7600e1ffaff8    tests\n")
           )),
         ("tag", "772493498dc9f21ddce8b617f1834bf9c844f745",
          (b"tag 150",
           ("object f98d4b00d3303e853bc0089b4138339894555ffd\n"
            "type commit\ntag tag_test\n"
            "tagger DDExpo <f8ck.th1sm3n@gmail.com> 1723236825 +0600\n"
            "tag_commit_test_one\n")
           ))]
        ]


def test_gyat_cat_file(setup_data):
    '''
    Verifies `gyat_cat_file` processes checks if the function return header and
    content of the objects[blob, tree, commit, tag] as expected.
    '''

    for base_path, sha, answer in setup_data:
        assert gyat_cat_file(parent_repo=base_path, shas_file=sha) == answer
