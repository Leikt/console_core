from argparse import Namespace, ArgumentParser

from .variables import ReturnCode


class CommandQuit:
    """Quit the program."""
    KEYWORD = 'quit'

    @staticmethod
    def setup_parser(_parser: ArgumentParser) -> bool:
        return True

    @staticmethod
    def execute(_args: Namespace) -> ReturnCode:
        return ReturnCode.QUIT
