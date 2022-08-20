import unittest

from src import console
from src.console import ReturnCode


class TestComplete(unittest.TestCase):
    def test_full_execution(self):
        console.reset()
        console.load_plugins('data/plugins.txt')
        self.assertEqual(console.execute(['test', 'success']), ReturnCode.SUCCESS)
        self.assertEqual(console.execute(['test', 'failure']), ReturnCode.FAILURE)