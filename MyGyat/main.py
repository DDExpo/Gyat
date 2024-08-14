from pathlib import Path

from const import GYAT_OBJECTS_FILES, GYAT_REFS
from utils import valid_tag_name
from utils_utils import get_all_files_name
from cmd_with_do_nothing import CmdWithDoNothnglLogic
from abstr_command import (
    cmd_add, cmd_cat_file, cmd_check_ignore, cmd_commit, cmd_clone,
    cmd_commit_tree, cmd_hash_object, cmd_init, cmd_ls_files,
    cmd_ls_tree, cmd_rm, cmd_show_ref, cmd_status, cmd_tag,
    cmd_write_tree
)


class GyatConsole(CmdWithDoNothnglLogic):

    intro = 'Welcome to Gyat. Type help to list commands.\n'
    prompt = '$gyat '

    def do_init(self, args):
        '''Initialize a new repository'''
        args = self._parse_args("init", args)
        if args:
            cmd_init(Path(args.path).absolute())
            print("Initialized empty Git repository")

    def do_ls_tree(self, args):
        '''List the contents of a Gyat tree object.'''
        args = self._parse_args("ls_tree", args)
        if args:
            if self._pre_command_execution_validation(sha=args,
                                                      obj_type="tree"):
                cmd_ls_tree(self.base_dir, args.sha, args.f)

    def do_write_tree(self, args):
        '''Create a new tree object from the current index.'''
        args = self._parse_args("write_tree", args)
        if args:
            if self._pre_command_execution_validation():
                cmd_write_tree(self.base_dir, args.w, args.w_blobs)

    def do_commit_tree(self, args):
        '''
        Create a new commit object from a tree object
        with optional parent commits.
        '''
        args = self._parse_args("commit_tree", args)
        if args:
            if self._pre_command_execution_validation(sha=args,
                                                      obj_type="tree"):
                cmd_commit_tree(self.base_dir, args.sha,
                                args.p, args.m, args.w)

    def do_hash_object(self, args):
        '''Compute the SHA-1 hash of the given file'''
        args = self._parse_args("hash_object", args)
        if args:
            obj_path = Path(args.path).resolve()
            if self._pre_command_execution_validation():
                if args.t in GYAT_OBJECTS_FILES and not obj_path.is_file():
                    print("Path should be to a file!")
                else:
                    cmd_hash_object(obj_path, self.base_dir, args.t, args.w)

    def do_cat_file(self, args):
        '''Retrieve information or content of a Gyat object.'''
        args = self._parse_args("cat_file", args)
        if args:
            if self._pre_command_execution_validation(args):
                cmd_cat_file(args.sha, self.base_dir)

    def do_show_ref(self, args):
        '''List all referencies and tags'''
        args = self._parse_args("show_ref", args)
        if self._pre_command_execution_validation():
            cmd_show_ref(self.base_dir, args.t)

    def do_tag(self, args):
        '''Create tags'''
        args = self._parse_args("tag", args)
        if args:
            tag_name = args.name
            if valid_tag_name(tag_name):
                if tag_name not in self.unique_names_ref_tags:
                    if self._pre_command_execution_validation():
                        cmd_tag(
                            self.base_dir, tag_name, args.m, args.obj, args.a)
                        self.unique_names_ref_tags.add(tag_name)
                else:
                    print("Tag name shoud be unique!")
                    self.unique_names_ref_tags.union(get_all_files_name(
                        self.base_dir / GYAT_REFS / "tags"))

    def do_status(self, args):
        '''Show the working tree status'''
        args = self._parse_args("status", args)
        if args:
            if self._pre_command_execution_validation():
                cmd_status(self.base_dir)

    def do_ls_files(self, args):
        '''Displays inforamtion of files in the staging area.'''
        args = self._parse_args("ls_files", args)
        if args:
            if self._pre_command_execution_validation():
                cmd_ls_files(self.base_dir, args.v)

    def do_check_ignore(self, args):
        '''
        check-ignore command, takes a list of paths and outputs back
        those of those paths that should be ignored.
        '''
        args = self._parse_args("check_ignore", args)
        if args:
            if self._pre_command_execution_validation():
                cmd_check_ignore(args.path, self.base_dir)

    def do_rm(self, args):
        '''Remove files from the working tree and the index.'''
        args = self._parse_args("rm", args)
        if args:
            if self._pre_command_execution_validation():
                cmd_rm(args.path, self.base_dir)

    def do_add(self, args):
        '''Add file contents to the index'''
        args = self._parse_args("add", args)
        if args:
            if self._pre_command_execution_validation():
                cmd_add(args.path, self.base_dir)

    def do_commit(self, args):
        '''Record changes to the repository'''
        args = self._parse_args("commit", args)
        if args:
            if self._pre_command_execution_validation():
                cmd_commit(args.message, self.base_dir)

    def do_clone(self, args):
        '''Clone remote repository to c urrent dir, by url'''
        args = self._parse_args("clone", args)
        if args:
            cmd_clone(args.url, args.name)


if __name__ == "__main__":
    GyatConsole().cmdloop()
