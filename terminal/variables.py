from __future__ import annotations

from argparse import ArgumentParser
from typing import Dict

from .command import PCommand

commands: Dict[str, PCommand] = {}
argument_parser: ArgumentParser = ArgumentParser()
command_parser = argument_parser.add_subparsers(dest='command')

