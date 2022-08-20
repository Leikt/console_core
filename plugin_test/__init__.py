from argparse import Namespace, ArgumentParser

from terminal import ReturnCode
from terminal import PCommand


def plugin_registration() -> PCommand:
    """Iterate the commands object to add to the system."""
    yield CommandTest()


class CommandTest:
    KEYWORD = 'test'

    @staticmethod
    def setup_parser(parser: ArgumentParser) -> bool:
        parser.add_argument('value', type=str, choices=('success', 'failure', 'quit'))
        return True

    @staticmethod
    def execute(args: Namespace) -> ReturnCode:
        a = ReturnCode.SUCCESS == ReturnCode.from_name(args.value.upper())
        return ReturnCode.from_name(args.value.upper())
