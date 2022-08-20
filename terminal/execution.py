import argparse
import shlex
from typing import List

from .decorators import clean_keyboard_interruption
from .exceptions import CommandNotFoundError
from .variables import ReturnCode, argument_parser, commands


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


@clean_keyboard_interruption
def mainloop(prompt: str = '$> '):
    while True:
        cli = input(prompt)
        args = shlex.split(cli)
        if len(args) == 0:
            continue

        code = execute(args)
        if code == ReturnCode.QUIT:
            break
