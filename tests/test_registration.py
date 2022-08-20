import unittest

import terminal
from terminal import CommandRegistrationConflict
import plugin_test


class TestRegistration(unittest.TestCase):
    def setUp(self) -> None:
        terminal.reset()

    def test_command_registration(self):
        terminal.register_command(plugin_test.CommandTest())

    def test_command_registration_conflict(self):
        terminal.register_command(plugin_test.CommandTest())
        with self.assertRaises(CommandRegistrationConflict):
            terminal.register_command(plugin_test.CommandTest())

    def test_plugin_registration(self):
        terminal.register_plugin(plugin_test)

    def test_plugin_registration_conflict(self):
        terminal.register_plugin(plugin_test)
        with self.assertRaises(CommandRegistrationConflict):
            terminal.register_plugin(plugin_test)

