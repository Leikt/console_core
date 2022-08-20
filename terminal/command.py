from __future__ import annotations

from argparse import ArgumentParser, Namespace
from enum import Enum, auto
from typing import Protocol, Optional


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
    """Interface used to register and run the command."""
    KEYWORD: str

    @staticmethod
    def setup_parser(parser: ArgumentParser) -> bool:
        """Set up the argument parser for the command."""

    def execute(self, args: Namespace) -> ReturnCode:
        """Execute the command and return a code."""
