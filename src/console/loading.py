import importlib
import warnings
from typing import List, Any

from .exceptions import PluginNotFoundError, PluginNotFoundWarning
from .registration import register_plugin


def import_module(name: str) -> Any:
    """Import a module."""
    return importlib.import_module(name)


def read_plugins_file(filename: str) -> List[str]:
    """Read the file where the plugin list is defined and return a list of modules names."""
    with open(filename, 'r') as file:
        plugin_names = file.read().splitlines()
    return plugin_names


def load_plugins(filename: str, ignore_errors: bool = False) -> bool:
    """Load the plugin using the list in the file."""
    plugin_names = read_plugins_file(filename)
    for plugin_name in plugin_names:
        try:
            plugin = import_module(plugin_name)
            register_plugin(plugin)
        except ModuleNotFoundError:
            if not ignore_errors:
                raise PluginNotFoundError(plugin_name)
            else:
                warnings.warn(PluginNotFoundWarning(plugin_name))
    return True
