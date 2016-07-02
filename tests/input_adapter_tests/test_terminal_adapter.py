from unittest import TestCase
from samantha.conversation import Statement
from samantha.adapters.input import TerminalAdapter


class TerminalAdapterTests(TestCase):
    """
    The terminal adapter is designed to allow
    interaction with the chat bot to occur through
    a command line interface.
    """

    def setUp(self):
        self.adapter = TerminalAdapter()
