from .commands import CommandQuit
from .exceptions import CommandRegistrationConflict
from .variables import command_parser, commands, PCommand


def initialize():
    register_command(CommandQuit())


def register_plugin(module):
    """Register the commands of the given module."""
    command: PCommand
    for command in module.plugin_registration():
        register_command(command)


def register_command(command: PCommand) -> bool:
    """Register the given command."""
    keyword = command.KEYWORD
    if keyword in commands:
        raise CommandRegistrationConflict(keyword)

    parser = command_parser.add_parser(command.KEYWORD)
    command.setup_parser(parser)
    commands[keyword] = command
    return True


def unregister_command(keyword: str):
    """Remove the command from the known ones. Warning: it does not reset the argument parser."""
    if keyword in commands:
        del commands[keyword]


def reset():
    commands.clear()
