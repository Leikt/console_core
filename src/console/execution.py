from typing import List

from .exceptions import CommandNotFoundError
from .variables import ReturnCode, argument_parser, commands


def execute(args: List[str]) -> ReturnCode:
    """Execute the command and return a code."""
    args = argument_parser.parse_args(args)
    if args.command not in commands:
        raise CommandNotFoundError(args.command)
    return commands[args.command].execute(args)
