from typing import Dict

from .base_commands import CommandQuit
from .exceptions import CommandRegistrationConflict
from .variables import command_parser, commands
from .command import PCommand


def initialize():
    register_command(CommandQuit())


def register_plugin(module):
    """Register the commands of the given module."""
    command: PCommand
    for command in module.plugin_registration():
        register_command(command)


def register_command(command: PCommand, command_set: Dict[str, PCommand] = None) -> bool:
    """Register the given command."""
    if command_set is None:
        command_set = commands
    keyword = command.KEYWORD
    if keyword in commands:
        raise CommandRegistrationConflict(keyword)

    parser = command_parser.add_parser(command.KEYWORD)
    command.setup_parser(parser)
    command_set[keyword] = command
    return True


def unregister_command(keyword: str, command_set: Dict[str, PCommand] = None):
    """Remove the command from the known ones. Warning: it does not reset the argument parser."""
    if command_set is None:
        command_set = commands
    if keyword in commands:
        del command_set[keyword]


def reset():
    commands.clear()
