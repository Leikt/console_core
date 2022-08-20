from .exceptions import CommandRegistrationConflict
from .variables import command_parser, PCommand, commands


def register_plugin(module):
    """Register the commands of the given module."""
    command: PCommand
    for command in module.plugin_registration():
        parser = command_parser.add_parser(command.KEYWORD)
        command.setup_parser(parser)
        register_command(command)


def register_command(command: PCommand) -> bool:
    """Register the given command."""
    keyword = command.KEYWORD
    if keyword in commands:
        raise CommandRegistrationConflict(keyword)
    commands[keyword] = command
    return True


def unregister_command(keyword: str):
    """Remove the command from the known ones. Warning: it does not reset the argument parser."""
    if keyword in commands:
        del commands[keyword]


def reset():
    commands.clear()
