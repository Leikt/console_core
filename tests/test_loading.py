import unittest

from src import console
from src.console import PluginNotFoundError, PluginNotFoundWarning


class TestLoading(unittest.TestCase):
    def setUp(self) -> None:
        console.reset()

    def test_loading(self):
        self.assertTrue(console.load_plugins('data/plugins.txt'))

    def test_loading_failure(self):
        with self.assertRaises(PluginNotFoundError):
            console.load_plugins('data/plugin_not_found.txt')

    def test_loading_warning(self):
        with self.assertWarns(PluginNotFoundWarning):
            console.load_plugins('data/plugin_not_found.txt', ignore_errors=True)
