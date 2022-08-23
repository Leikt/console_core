from __future__ import annotations

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, Optional, Callable, Union

from .exceptions import CommandRegistrationConflict, CommandNotFoundError


class ReturnCode(Enum):
    """Exit code of an execution."""
    # noinspection PyArgumentList
    SUCCESS = "success"

    # noinspection PyArgumentList
    FAILURE = "failure"

    # noinspection PyArgumentList
    QUIT = "quit"

    @classmethod
    def from_name(cls, name: str) -> Optional[ReturnCode]:
        return cls.__members__.get(name, None)


class PCommand(Protocol):
    """Interface used to register and run the command."""

    @staticmethod
    def get_keyword() -> str:
        """Return the keyword of the command."""

    def setup_argument_parser(self, argument_parser: ArgumentParser, depth: int = 0) -> None:
        """Set up the argument parser for the command."""

    def execute(self, arguments: Namespace) -> tuple[ReturnCode, Optional[Any]]:
        """Execute the command and return a code."""


class PCommandSet(PCommand):

    def register_command(self, command: PCommand) -> bool:
        """Add the command to the set"""

    def unregister_command(self, keyword: str) -> bool:
        """Make the command inaccessible to execution."""


def default_custom_setup_argument_parser(_argument_parser: ArgumentParser, _depth: int = 0) -> None:
    return


def default_pre_exec(_arguments: Namespace) -> tuple[bool, ReturnCode, Optional[Any]]:
    return False, ReturnCode.SUCCESS, None


def default_post_exec(_arguments: Namespace) -> None:
    return


@dataclass
class CommandSet(PCommandSet):
    """Handle a command set registration"""
    __keyword: str
    custom_setup_argument_parser: Callable[[ArgumentParser, int], None] = field(
        default=default_custom_setup_argument_parser)
    pre_execution: Callable[[Namespace], tuple[bool, ReturnCode, Optional[Any]]] = field(default=default_pre_exec)
    post_execution: Callable[[Namespace], None] = field(default=default_post_exec)
    __command_argument_name: str = field(init=False)
    __command_set: dict[str, PCommand] = field(default_factory=dict)
    is_standlone: bool = field(default=False)

    def get_keyword(self) -> str:
        return self.__keyword

    def register_command(self, command: PCommand) -> bool:
        """Add the command to the set"""
        keyword = command.get_keyword()
        if keyword in self.__command_set:
            raise CommandRegistrationConflict(keyword)

        self.__command_set[keyword] = command
        return True

    def unregister_command(self, keyword: str) -> bool:
        """Make the command inaccessible to execution."""
        if keyword in self.__command_set:
            del self.__command_set[keyword]
            return True
        return False

    def setup_argument_parser(self, argument_parser: ArgumentParser, depth: int = 1) -> None:
        """Set up the argument parsers for the commands."""
        self.__command_argument_name = f'command_{depth}'
        sub_parsers = argument_parser.add_subparsers(dest=self.__command_argument_name,
                                                     required=(not self.is_standlone))
        for command in self.__command_set.values():
            sub_parser = sub_parsers.add_parser(name=command.get_keyword())
            command.setup_argument_parser(sub_parser, depth + 1)
        self.custom_setup_argument_parser(argument_parser, depth)

    def execute(self, arguments: Namespace) -> tuple[ReturnCode, Any]:
        """Execute the command and return the result."""
        abort, return_code, stdin = self.pre_execution(arguments)
        if abort:
            return return_code, stdin
        keyword = arguments.__getattribute__(self.__command_argument_name)
        if keyword not in self.__command_set:
            raise CommandNotFoundError(keyword)
        result = self.__command_set[keyword].execute(arguments)
        self.post_execution(arguments)
        return result

    def get_commands(self) -> list[PCommand]:
        """FOR TESTING PURPOSES ONLY"""
        return list(self.__command_set.values())


@dataclass
class CommandSetBuilder:
    __keyword: str
    __command_set_class: type = field(default=CommandSet)
    __custom_setup_argument_parsing: Callable[[ArgumentParser, int], None] = field(
        default=default_custom_setup_argument_parser)
    __custom_pre_exec: Callable[[Namespace], tuple[bool, ReturnCode, Optional[Any]]] = field(default=default_pre_exec)
    __custom_post_exec: Callable[[Namespace], None] = field(default=default_post_exec)
    __commands: list[PCommand] = field(default_factory=list)
    __is_standalone: bool = field(default=False)

    def add_command(self, command: Union[PCommand, type]) -> CommandSetBuilder:
        if isinstance(command, type):
            command = command()
        self.__commands.append(command)
        return self

    def set_custom_setup_argument_parsing(self, function: Callable[[ArgumentParser, int], None]) -> CommandSetBuilder:
        self.__custom_setup_argument_parsing = function
        return self

    def set_custom_pre_execution(self, function: Callable[
        [Namespace], tuple[bool, ReturnCode, Optional[Any]]]) -> CommandSetBuilder:
        self.__custom_pre_exec = function
        return self

    def set_custom_post_exec(self, function: Callable[[Namespace], None]) -> CommandSetBuilder:
        self.__custom_post_exec = function
        return self

    def set_standalone(self, value: bool = True) -> CommandSetBuilder:
        self.__is_standalone = value
        return self

    def build(self) -> PCommandSet:
        command_set: PCommandSet = self.__command_set_class(self.__keyword, self.__custom_setup_argument_parsing,
                                                            self.__custom_pre_exec, self.__custom_post_exec,
                                                            is_standalone=self.__is_standalone)
        for command in self.__commands:
            command_set.register_command(command)
        return command_set
