import shlex
from argparse import ArgumentParser
from dataclasses import dataclass, field
from typing import Protocol, Any, Optional

from . import CommandNotFoundError
from .command_set import ReturnCode, PCommand
from .decorators import clean_keyboard_interruption


def read_command_line(prompt: str = '$> ') -> str:
    result = input(prompt)
    if result == 'help':
        return '--help'
    return result


class PTerminal(Protocol):
    """Interface to run commands."""

    def initialize(self, commands: list[PCommand]) -> None:
        """Register the commands and set up the argument parser."""

    def execute(self, command_line: str) -> tuple[ReturnCode, Optional[Any]]:
        """Execute the given command line."""

    def mainloop(self) -> None:
        """Run the terminal using the user input as command line source."""


@dataclass
class Terminal:
    argument_parser: ArgumentParser
    commands: dict[str, PCommand] = field(default_factory=dict)

    def initialize(self, commands: list[PCommand]) -> None:
        sub_parsers = self.argument_parser.add_subparsers(dest='command_0')
        for command in commands:
            self.commands[command.get_keyword()] = command
            sub_parser = sub_parsers.add_parser(name=command.get_keyword())
            command.setup_argument_parser(sub_parser)

    def execute(self, command_line: str) -> tuple[ReturnCode, Optional[Any]]:
        cli = shlex.split(command_line)
        arguments = self.argument_parser.parse_args(cli)
        if arguments.command_0 is None:
            return ReturnCode.EMPTY, None
        return self.commands[arguments.command_0].execute(arguments)

    @clean_keyboard_interruption
    def mainloop(self) -> None:
        while True:
            command_line = read_command_line()
            code = ReturnCode.FAILURE
            try:
                code, stdin = self.execute(command_line)
                if stdin is not None:
                    print(stdin)
            except SystemExit:
                continue
            except CommandNotFoundError as e:
                print(e.message)
                continue
            finally:
                if code == ReturnCode.QUIT:
                    break
