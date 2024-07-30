import os
import cmd
from pprint import pprint
from pathlib import Path

from gyat_exceptions import NecessaryArgsError
from args_parser import arparser_settings
from abstr_command import (
    cmd_add, cmd_cat_file, cmd_check_ignore, cmd_checkout, cmd_commit,
    cmd_commit_tree, cmd_hash_object, cmd_init, cmd_log, cmd_ls_files,
    cmd_ls_tree, cmd_rev_parse, cmd_rm, cmd_show_ref, cmd_status, cmd_tag,
    cmd_write_tree
)


class GyatConsole(cmd.Cmd):
    intro = 'Welcome to Gyat. Type help to list commands.\n'
    prompt = '$gyat '
    arg_parser = arparser_settings()

    def do_pwd(self, args):
        '''show current directory'''
        print(f"{os.getcwd()}")

    def do_ls(self, args):
        '''List all directories in current directory'''
        pprint(f'{" -".join(os.listdir())}', width=77)

    def do_cd(self, args):
        '''Move to a new directory'''
        if args:
            try:
                os.chdir(args)
                print(f'Changed directory to: {os.getcwd()}')
            except FileNotFoundError:
                print(f'Directory not found: {args}')
            except NotADirectoryError:
                print(f'Not a directory: {args}')
            except PermissionError:
                print(f'Permission denied: {args}')

    def do_mkdir(self, args):
        '''Create directory'''
        os.makedirs(Path(os.getcwd() + '/' + args), exist_ok=True)

    def do_rms(self, args):
        '''Remove directory/file'''
        os.remove(Path(os.getcwd() + '/' + args))

    def do_mkfil(self, args):
        '''Cretate file'''
        if not args:
            print('File name coudnt be empty')
        else:
            open(file=args, mode='w', encoding='utf-8')

    def do_init(self, args):
        '''Initialize a new repository'''
        try:
            args = self.arg_parser.parse_args(["cat-file" + args])
            cmd_init(args)
        except NecessaryArgsError as e:
            print(e)
        print("Initialized empty Git repository")

    def do_cat_file(self, args):
        '''Retrieve information or content of a Git object.'''
        try:
            args = self.arg_parser.parse_args(["cat-file" + args])
            cmd_cat_file(args)
        except NecessaryArgsError as e:
            print(e)

    def do_hash_object(self, args):
        '''Compute the SHA-1 hash of a file's content'''
        try:
            args = self.arg_parser.parse_args(["cat-file" + args])
            cmd_hash_object(args)
        except NecessaryArgsError as e:
            print(e)

    def do_ls_tree(self, args):
        '''List the contents of a Git tree object.'''
        try:
            args = self.arg_parser.parse_args(["cat-file" + args])
            cmd_ls_tree(args)
        except NecessaryArgsError as e:
            print(e)

    def do_write_tree(self, args):
        '''Create a new tree object from the current index.'''
        try:
            args = self.arg_parser.parse_args(["cat-file" + args])
            cmd_write_tree(args)
        except NecessaryArgsError as e:
            print(e)

    def do_commit_tree(self, args):
        '''
        Create a new commit object from a tree object
        and optional parent commits.
        '''
        try:
            args = self.arg_parser.parse_args(["cat-file" + args])
            cmd_commit_tree(args)
        except NecessaryArgsError as e:
            print(e)

    def do_clone(self, args):
        '''Clone a repository into a new directory'''
        print(f"Cloning into {args}...")

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
