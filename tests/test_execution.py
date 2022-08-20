import unittest

from src import console
from src.console import ReturnCode
from tests import plugin_test


class TestExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        console.reset()
        console.register_plugin(plugin_test)

    def test_execution_success(self):
        self.assertEqual(console.execute(args=['test', 'success']), ReturnCode.SUCCESS)

    def test_execution_failure(self):
        self.assertEqual(console.execute(args=['test', 'failure']), ReturnCode.FAILURE)

    def test_execution_quit(self):
        self.assertEqual(console.execute(args=['test', 'quit']), ReturnCode.QUIT)
