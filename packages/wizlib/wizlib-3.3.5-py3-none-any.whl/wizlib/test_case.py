# Patch inputs and outputs for easy testing

from io import StringIO
from unittest import TestCase
from unittest.mock import Mock, patch


class WizLibTestCase(TestCase):
    """Wrap your test cases in this class to use the patches correctly"""

    def setUp(self):
        self.notty = patch('wizlib.io.isatty', Mock(return_value=False))
        self.notty.start()

    def tearDown(self):
        self.notty.stop()

    @staticmethod
    def patch_stream(val: str):
        """Patch stream input such as pipes for stream handler"""
        mock = Mock(return_value=val)
        return patch('wizlib.io.stream', mock)

    @staticmethod
    def patch_ttyin(val: str):
        """Patch input typed by a user in shell ui"""
        mock = Mock(side_effect=val)
        return patch('wizlib.io.ttyin', mock)

    @staticmethod
    def patcherr():  # pragma: nocover
        return patch('sys.stderr', StringIO())

    @staticmethod
    def patchout():  # pragma: nocover
        return patch('sys.stdout', StringIO())
