import unittest
from argparse import ArgumentParser

import terminal
from terminal import PluginNotFoundError


class TestLoading(unittest.TestCase):
    def test_loading_core(self):
        argument_parser = ArgumentParser()
        commands = terminal.load_plugin('plugin_core')
        t: terminal.PTerminal = terminal.Terminal(argument_parser)
        t.initialize(commands)
        code, _ = t.execute('quit')
        self.assertEqual(code, terminal.ReturnCode.QUIT)

    def test_loading_other(self):
        argument_parser = ArgumentParser()
        commands = terminal.load_plugin('plugin_core')
        commands += terminal.load_plugin('plugin_test')
        t: terminal.PTerminal = terminal.Terminal(argument_parser)
        t.initialize(commands)
        code, _ = t.execute('quit')
        self.assertEqual(code, terminal.ReturnCode.QUIT)
        code, _ = t.execute('test success')
        self.assertEqual(code, terminal.ReturnCode.SUCCESS)

    def test_loading_from_file(self):
        argument_parser = ArgumentParser()
        commands = terminal.load_plugins_from_file('data/plugins.txt')
        t: terminal.PTerminal = terminal.Terminal(argument_parser)
        t.initialize(commands)
        code, _ = t.execute('math is_int 12')
        self.assertEqual(code, terminal.ReturnCode.SUCCESS)
        code, _ = t.execute('math is_int azezrty')
        self.assertEqual(code, terminal.ReturnCode.FAILURE)
        code, result = t.execute('math fibonacci 7')
        self.assertEqual(code, terminal.ReturnCode.SUCCESS)
        self.assertEqual(result, 13)

    def test_loading_errors(self):
        with self.assertRaises(PluginNotFoundError):
            terminal.load_plugins_from_file('data/plugin_not_found.txt')
