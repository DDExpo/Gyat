import os
import cmd
import argparse
from argparse import ArgumentError, Namespace
from pathlib import Path

from const import GYAT_COMMANDS
from utils_utils import find_repo_gyat
from gyat_exceptions import NecessaryArgsError, IsNotGyatDirError
from args_parser import arparser_settings


class CmdWithDoNothnglLogic(cmd.Cmd):
    '''
    Implementation of Cmd with do nothing logic
    So in some scenarios we shouldnt return or do anything
    For example when we computing command we catch exception and print error
    thats all, we dont go deeper.
    '''

    arg_parser = arparser_settings()
    base_dir: Path = ""

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
            isinstance(act, argparse._SubParsersAction)
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
