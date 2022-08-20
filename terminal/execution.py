import argparse
import shlex
from typing import List

from .command import ReturnCode
from .decorators import clean_keyboard_interruption
from .exceptions import CommandNotFoundError
from .variables import argument_parser, commands


def execute(args: List[str]) -> ReturnCode:
    """Execute the command and return a code."""
    try:
        args = argument_parser.parse_args(args)
    except SystemExit:
        return ReturnCode.FAILURE
    except argparse.ArgumentError:
        return ReturnCode.FAILURE

    if args.command not in commands:
        raise CommandNotFoundError(args.command)
    return commands[args.command].execute(args)


def read_next_command() -> str:
    result = input('$> ')
    if result == 'help':
        return '--help'
    return result


@clean_keyboard_interruption
def mainloop():
    while True:
        cli = read_next_command()
        args = shlex.split(cli)
        if len(args) == 0:
            continue

        code = execute(args)
        if code == ReturnCode.QUIT:
            break
