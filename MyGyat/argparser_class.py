import argparse

from MyGyat.gyat_exceptions import NecessaryArgsError


class ArgumentParserNotExit(argparse.ArgumentParser):
    '''overrided func error so it will not exit on error'''

    def error(self, message: str):
        raise NecessaryArgsError(message)
