import unittest

import terminal
from terminal import ReturnCode


class TestComplete(unittest.TestCase):
    def test_full_execution(self):
        terminal.reset()
        terminal.load_plugins('data/plugins.txt')
        self.assertEqual(terminal.execute(['test', 'success']), ReturnCode.SUCCESS)
        self.assertEqual(terminal.execute(['test', 'failure']), ReturnCode.FAILURE)
