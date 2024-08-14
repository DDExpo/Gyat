import os
import cmd
from pathlib import Path
from pprint import pprint
from argparse import ArgumentError, Namespace, _SubParsersAction

from const import GYAT_COMMANDS, GYAT_REFS
from utils import is_gyat_object, find_resolve_tag_ref
from utils_utils import find_repo_gyat, get_all_files_name
from gyat_exceptions import (
    NecessaryArgsError, IsNotGyatDirError, IsNotSameTypeError,)
from args_parser import arparser_settings


class CmdWithDoNothnglLogic(cmd.Cmd):
    '''
    Implementation of Cmd with do nothing logic. So in some scenarios
    we shouldnt return or do anything for example when we parse command
    we catch exception and print error so we return None thats all,
    we dont go deeper, or do some strange shit as execute last command.
    '''

    arg_parser = arparser_settings()
    base_dir: Path = ""
    # No comment
    try:
        unique_names_ref_tags: set[str] = get_all_files_name(
            find_repo_gyat() / GYAT_REFS)
    except IsNotGyatDirError:
        pass

    def precmd(self, line: str) -> str:
        try:
            if line.split()[0] in GYAT_COMMANDS:
                self.base_dir = find_repo_gyat(Path(os.getcwd()))
        except IsNotGyatDirError as e:
            print(f"error: {e}")
            return None
        else:
            return super().precmd(line)

    def parseline(
         self, line: str) -> tuple[str, str, str]:

        if line is None:
            return None, None, None
        return super().parseline(line)

    def onecmd(self, line: str) -> bool:

        if line is None:
            return None
        return super().onecmd(line)

    def do_help(self, arg: str) -> bool:
        '''Help'''
        if not arg:
            return super().do_help(arg)
        arg_com = arg.split()[0]

        # Getting helper of argparser to replace cmds
        commands = [
            act for act in self.arg_parser._actions if
            isinstance(act, _SubParsersAction)
        ][0].choices

        if arg_com in commands:
            commands[arg_com].print_help()
        else:
            print(f"No such command: {arg_com}")

    def _parse_args(self, command, args) -> Namespace:
        try:
            return self.arg_parser.parse_args([command] + args.split())
        except NecessaryArgsError as e:
            print(e)
        except ArgumentError as e:
            print(e)

    def _pre_command_execution_validation(
         self, sha="", obj_type: str = None) -> bool:
        '''
        func to validate data given by user and context, when input
        was parsed but not executed yet
        '''

        try:
            self.base_dir = find_repo_gyat(Path(os.getcwd()))
            if sha.sha in self.unique_names_ref_tags:
                sha.sha = find_resolve_tag_ref(self.base_dir, sha.sha)
            if obj_type:
                is_gyat_object(self.base_dir, sha.sha, obj_type)
            return True
        except PermissionError as e:
            print(f"error: {e}")
        except TypeError as e:
            print(f"error: {e}")
        except FileNotFoundError as e:
            print("sha key invalid or object does not exist\n"
                  f"error: {e}")
        except IsNotSameTypeError as e:
            print(f"error: {e}")
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            print(f"error: {e}")
        except IsNotGyatDirError as e:
            print(f"error {e}")
        except BaseException as e:
            print(f"Something went wrong {e}")

    def do_pwd(self, args):
        '''show current directory'''
        print(f"{os.getcwd()}")

    def do_ls(self, args):
        '''List all directories in current directory'''
        pprint(f'{" --".join(os.listdir())}', depth=78, width=78)

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

    def do_rm(self, args):
        '''Remove directory/file'''
        os.remove(Path(os.getcwd() + '/' + args))

    def do_mkfil(self, args):
        '''Cretate file'''
        if not args:
            print('File name coudnt be empty')
        else:
            open(file=args, mode='w', encoding='utf-8')

    def do_exit(self, args):
        '''Exit the console'''
        return True

    def do_quit(self, args):
        '''Exit the console'''
        return True

    def default(self, line):
        print(f'Unknown command: {line}')
