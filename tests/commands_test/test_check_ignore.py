
from MyGyat.commands import (gyat_commit_tree, gyat_hash_object, gyat_ls_tree,
    gyat_write_tree, gyat_init, gyat_show_ref, gyat_tag, gyat_ls_files,
    gyat_check_ignore, gyat_status, gyat_rm, gyat_add, gyat_clone_rep)


def test_check_ignore(setupe_data):
    gyat_check_ignore()
