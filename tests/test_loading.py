import unittest

import terminal
from terminal import PluginNotFoundError, PluginNotFoundWarning


class TestLoading(unittest.TestCase):
    def setUp(self) -> None:
        terminal.reset()

    def test_loading(self):
        self.assertTrue(terminal.load_plugins('data/plugins.txt'))

    def test_loading_failure(self):
        with self.assertRaises(PluginNotFoundError):
            terminal.load_plugins('data/plugin_not_found.txt')

    def test_loading_warning(self):
        with self.assertWarns(PluginNotFoundWarning):
            terminal.load_plugins('data/plugin_not_found.txt', ignore_errors=True)
