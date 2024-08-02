from pathlib import Path

from args_parser import arparser_settings
from cmd_with_do_nothing import CmdWithDoNothnglLogic
from abstr_command import (
    cmd_add, cmd_cat_file, cmd_check_ignore, cmd_checkout, cmd_commit,
    cmd_commit_tree, cmd_hash_object, cmd_init, cmd_ls_files, cmd_show_ref,
    cmd_ls_tree, cmd_rev_parse, cmd_rm, cmd_show_ref, cmd_status, cmd_tag,
    cmd_write_tree
)


class GyatConsole(CmdWithDoNothnglLogic):

    intro = 'Welcome to Gyat. Type help to list commands.\n'
    prompt = '$gyat '
    arg_parser = arparser_settings()

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
            if self._pre_command_execution_validation(args, obj_type="tree"):
                cmd_ls_tree(args, self.base_dir)

    def do_write_tree(self, args):
        '''Create a new tree object from the current index.'''
        args = self._parse_args("write_tree", args)
        if args:
            obj_path = Path(args.path).absolute()
            if self._pre_command_execution_validation(args, obj_path=obj_path):
                cmd_write_tree(obj_path, self.base_dir, args.w)

    def do_commit_tree(self, args):
        '''
        Create a new commit object from a tree object
        with optional parent commits.
        '''
        args = self._parse_args("commit_tree", args)
        if args:
            if self._pre_command_execution_validation(args, obj_type="tree"):
                cmd_commit_tree(args, self.base_dir)

    def do_hash_object(self, args):
        '''Compute the SHA-1 hash of a file's content'''
        args = self._parse_args("hash_object", args)
        if args:
            obj_path = Path(args.path).absolute()
            if self._pre_command_execution_validation(args, obj_path=obj_path):
                cmd_hash_object(args.path, base_dir=self.base_dir)

    def do_cat_file(self, args):
        '''Retrieve information or content of a Gyat object.'''
        args = self._parse_args("cat_file", args)
        if args:
            cmd_cat_file(args, base_dir=self.base_dir)

    def do_show_ref(self, args):
        '''Clone a repository into a new directory'''
        cmd_show_ref()

    def do_tag(self, args):
        '''Clone a repository into a new directory'''
        args = self._parse_args("tag", args)
        if args:
            cmd_tag(args, base_dir=self.base_dir)

    def do_status(self, args):
        '''Show the working tree status'''
        print("On branch main\nnothing to commit, working tree clean")

    def do_add(self, args):
        '''Add file contents to the index'''
        print(f"Adding file {args}")

    def do_yapping(self, args):
        '''Record changes to the repository'''
        print(f"[main (root-commit) abcd123] {args}")

    def do_exit(self, args):
        '''Exit the console'''
        return True

    def do_quit(self, args):
        '''Exit the console'''
        return True

    def default(self, line):
        print(f'Unknown command: {line}')


if __name__ == "__main__":
    GyatConsole().cmdloop()
