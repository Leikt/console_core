from argparse import Namespace, ArgumentParser
from typing import Optional, Any

from terminal import ReturnCode
from terminal import PCommand


def plugin_commands() -> PCommand:
    yield CommandTest()


class CommandTest:
    @staticmethod
    def get_keyword() -> str:
        return 'test'

    def setup_argument_parser(self, argument_parser: ArgumentParser, depth: int = 0) -> None:
        argument_parser.add_argument('value', type=str, choices=('success', 'failure', 'quit'))

    def execute(self, arguments: Namespace) -> tuple[ReturnCode, Optional[Any]]:
        return ReturnCode.from_name(arguments.value.upper()), None
