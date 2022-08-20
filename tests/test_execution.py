import unittest

import terminal
from terminal import ReturnCode
import plugin_test as plugin_test


class TestExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        terminal.reset()
        terminal.register_plugin(plugin_test)

    def test_execution_success(self):
        result = terminal.execute(args=['test', 'success'])
        self.assertEqual(result, ReturnCode.SUCCESS)

    def test_execution_failure(self):
        self.assertEqual(terminal.execute(args=['test', 'failure']), ReturnCode.FAILURE)

    def test_execution_quit(self):
        self.assertEqual(terminal.execute(args=['test', 'quit']), ReturnCode.QUIT)
