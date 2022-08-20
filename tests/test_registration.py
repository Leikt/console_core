import unittest

from src import console
from src.console import CommandRegistrationConflict
from tests import plugin_test


class TestRegistration(unittest.TestCase):
    def setUp(self) -> None:
        console.reset()

    def test_command_registration(self):
        console.register_command(plugin_test.CommandTest())

    def test_command_registration_conflict(self):
        console.register_command(plugin_test.CommandTest())
        with self.assertRaises(CommandRegistrationConflict):
            console.register_command(plugin_test.CommandTest())

    def test_plugin_registration(self):
        console.register_plugin(plugin_test)

    def test_plugin_registration_conflict(self):
        console.register_plugin(plugin_test)
        with self.assertRaises(CommandRegistrationConflict):
            console.register_plugin(plugin_test)

