import unittest
from argparse import ArgumentParser

from plugin_test import CommandTest
from terminal import CommandSet, CommandSetBuilder, PCommandSet, ReturnCode, CommandRegistrationConflict


class TestCommandSet(unittest.TestCase):
    def test_simple_build(self):
        builder = CommandSetBuilder('test')
        command_set: PCommandSet = builder.build()
        self.assertTrue(isinstance(command_set, CommandSet))
        self.assertEqual(command_set.get_keyword(), 'test')

    def test_simple_build_with_command(self):
        builder = CommandSetBuilder('test')
        builder.add_command(CommandTest())
        command_set: CommandSet = builder.build()
        self.assertTrue(isinstance(command_set.get_commands()[0], CommandTest))

    def test_argument_parsing(self):
        parser = ArgumentParser()

        builder = CommandSetBuilder('test')
        builder.add_command(CommandTest())
        command_set = builder.build()

        command_set.setup_argument_parser(parser)

        args = parser.parse_args(['test', 'success'])
        code, value = command_set.execute(args)
        self.assertEqual(code, ReturnCode.SUCCESS)
        self.assertEqual(value, None)

    def test_conflict_error(self):
        builder = CommandSetBuilder('test')
        builder.add_command(CommandTest())
        builder.add_command(CommandTest())
        with self.assertRaises(CommandRegistrationConflict):
            builder.build()
