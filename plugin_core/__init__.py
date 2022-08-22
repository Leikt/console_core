from argparse import Namespace, ArgumentParser
from typing import Optional, Any

from terminal import ReturnCode, PCommand


def plugin_commands() -> PCommand:
    yield CommandQuit()


class CommandQuit:
    """Quit the program."""

    @staticmethod
    def get_keyword() -> str:
        return 'quit'

    def setup_argument_parser(self, argument_parser: ArgumentParser, depth: int = 0) -> None:
        return

    def execute(self, _arguments: Namespace) -> tuple[ReturnCode, Optional[Any]]:
        return ReturnCode.QUIT, None
