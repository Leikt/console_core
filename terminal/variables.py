from __future__ import annotations

from argparse import ArgumentParser, Namespace
from enum import Enum, auto
from typing import Dict, Optional, Protocol

commands: Dict[str, PCommand] = {}
argument_parser: ArgumentParser = ArgumentParser()
command_parser = argument_parser.add_subparsers(dest='command')


class ReturnCode(Enum):
    """Exit code of an execution."""
    # noinspection PyArgumentList
    SUCCESS = auto()

    # noinspection PyArgumentList
    FAILURE = auto()

    # noinspection PyArgumentList
    QUIT = auto()

    @classmethod
    def from_name(cls, name: str) -> Optional[ReturnCode]:
        return cls.__members__.get(name, None)


class PCommand(Protocol):
    KEYWORD: str

    @staticmethod
    def setup_parser(parser: ArgumentParser) -> bool:
        """Set up the argument parser for the command."""

    def execute(self, args: Namespace) -> ReturnCode:
        """Execute the command and return a code."""
