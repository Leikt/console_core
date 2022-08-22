import importlib
from typing import List, Any

from .command_set import PCommand
from .exceptions import PluginNotFoundError


def import_module(name: str) -> Any:
    """Import a module."""
    return importlib.import_module(name)


def read_plugins_file(filename: str) -> List[str]:
    """Read the file where the plugin list is defined and return a list of modules names."""
    with open(filename, 'r') as file:
        plugin_names = file.read().splitlines()
    return plugin_names


def load_plugin(plugin_name: str) -> list[PCommand]:
    try:
        plugin = import_module(plugin_name)
    except ModuleNotFoundError:
        raise PluginNotFoundError(plugin_name)
    return [command for command in plugin.plugin_commands()]


def load_plugins(plugin_list: list[str]) -> list[PCommand]:
    commands: list[PCommand] = []
    for plugin_name in plugin_list:
        commands += load_plugin(plugin_name)
    return commands


def load_plugins_from_file(filename: str) -> list[PCommand]:
    return load_plugins(read_plugins_file(filename))
