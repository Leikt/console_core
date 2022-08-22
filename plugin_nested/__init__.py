from argparse import Namespace, ArgumentParser
from typing import Optional, Any

from terminal import ReturnCode, CommandSetBuilder
from terminal import PCommand


def plugin_commands() -> PCommand:
    yield CommandSetBuilder('math') \
        .add_command(CommandIsNumeric) \
        .add_command(CommandFibonacci) \
        .build()


class CommandIsNumeric:
    @staticmethod
    def get_keyword() -> str:
        return 'is_int'

    def setup_argument_parser(self, argument_parser: ArgumentParser, _depth: int = 0) -> None:
        argument_parser.add_argument('value', type=str, help='The value to test.')

    def execute(self, arguments: Namespace) -> tuple[ReturnCode, Optional[Any]]:
        value: str = arguments.value
        if value.isnumeric():
            return ReturnCode.SUCCESS, True
        return ReturnCode.FAILURE, False


class CommandFibonacci:
    @staticmethod
    def get_keyword() -> str:
        return 'fibonacci'

    def setup_argument_parser(self, argument_parser: ArgumentParser, depth: int = 0) -> None:
        argument_parser.add_argument('value', type=int, help='The start number of the fibonacci suite')

    def execute(self, arguments: Namespace) -> tuple[ReturnCode, Optional[Any]]:
        value: int = arguments.value
        return ReturnCode.SUCCESS, fibonacci(value)


def fibonacci(x: int) -> int:
    if x <= 1:
        return x
    return fibonacci(x - 1) + fibonacci(x - 2)
