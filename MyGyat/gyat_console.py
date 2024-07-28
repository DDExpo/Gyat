import cmd
import os
import argparse

from pathlib import Path

from commands import (
    gyat_cat_file, gyat_commit_tree, gyat_hash_object, gyat_ls_tree,
    gyat_write_tree, gyat_init)


class GyatConsole(cmd.Cmd):
    intro = 'Welcome to Gyat. Type help or ? to list commands.\n'
    prompt = '$gyat '

    def do_pwd(self, arg: str):
        '''show current directory'''
        print(f"{os.getcwd()}")

    def do_ls(self, arg: str):
        '''List all directories in current directory'''
        print(f'{" -".join(os.listdir())}')

    def do_cd(self, arg: str):
        '''Move to a new directory'''
        if arg:
            try:
                os.chdir(arg)
                print(f'Changed directory to: {os.getcwd()}')
            except FileNotFoundError:
                print(f'Directory not found: {arg}')
            except NotADirectoryError:
                print(f'Not a directory: {arg}')
            except PermissionError:
                print(f'Permission denied: {arg}')

    def do_mkdir(self, arg: str):
        '''Create directory'''
        os.makedirs(Path(os.getcwd() + '/' + arg), exist_ok=True)

    def do_rms(self, arg: str):
        '''Remove directory/file'''
        os.remove(Path(os.getcwd() + '/' + arg))

    def do_mkfil(self, arg: str):
        '''Cretate file'''
        if not arg:
            print('File name coudnt be empty')
        else:
            open(file=arg, mode='w', encoding='utf-8')

    def do_init(self):
        '''Initialize a new repository'''
        gyat_init()
        print("Initialized empty Git repository")

    def do_cat_file(self, arg: str):
        '''Retrieve information or content of a Git object.'''
        gyat_cat_file(arg)

    def do_hash_object(self, arg: str):
        '''Compute the SHA-1 hash of a file's content'''
        args = self.parser.parse_args(arg.strip().split())

        gyat_hash_object(path_file=arg[0], mkfile=args.w)

    def do_ls_tree(self, arg: str):
        '''List the contents of a Git tree object.'''
        args = self.parser.parse_args(arg.strip().split())
        gyat_ls_tree(args, args.)

    def do_write_tree(self, arg: str):
        '''Create a new tree object from the current index.'''
        user_input = arg.strip().split()
        gyat_write_tree(user_input[0])

    def do_commit_tree(self, arg: str):
        '''
        Create a new commit object from a tree object
        and optional parent commits.
        '''
        user_input = arg.strip().split()
        gyat_commit_tree(user_input[0], user_input[1:])

    def do_clone(self, arg: str):
        '''Clone a repository into a new directory'''
        print(f"Cloning into {arg}...")

    def do_status(self, arg: str):
        '''Show the working tree status'''
        print("On branch main\nnothing to commit, working tree clean")

    def do_add(self, arg: str):
        '''Add file contents to the index'''
        print(f"Adding file {arg}")

    def do_yapping(self, arg: str):
        '''Record changes to the repository'''
        print(f"[main (root-commit) abcd123] {arg}")

    def do_exit(self, arg: str):
        '''Exit the console'''
        return True

    def do_quit(self, arg: str):
        '''Exit the console'''
        return True

    def default(self, line):
        print(f'Unknown command: {line}')
