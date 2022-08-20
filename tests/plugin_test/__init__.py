from argparse import Namespace, ArgumentParser

from src.console import ReturnCode, PCommand


def plugin_registration() -> PCommand:
    """Iterate the commands object to add to the system."""
    yield CommandTest()


class CommandTest:
    KEYWORD = 'test'

    def setup_parser(self, parser: ArgumentParser) -> bool:
        parser.add_argument('value', type=str)
        return True

    def execute(self, args: Namespace) -> ReturnCode:
        return ReturnCode.from_name(args.value.upper())
