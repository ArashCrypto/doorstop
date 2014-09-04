"""Integration tests for the doorstop.server package."""

import os
import time
import unittest
from unittest.mock import patch
from multiprocessing import Process
import logging

from doorstop import server
from doorstop.server import main
from doorstop import settings

from doorstop.server.test import ENV, REASON


@unittest.skipUnless(os.getenv(ENV), REASON)
@patch('doorstop.settings.SERVER_HOST', 'localhost')
class TestServer(unittest.TestCase):

    """Integration tests for the client/server feature."""

    @classmethod
    def setUpClass(cls):
        assert settings.SERVER_PORT == 7867
        cls.process = Process(target=main.main, kwargs={'args': []})
        cls.process.start()
        logging.info("delaying for the server to initialize...")
        time.sleep(3)
        assert cls.process.is_alive()

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        logging.info("delaying for the server to shutdown...")
        time.sleep(1)

    def test_check(self):
        """Verify the server can be checked."""
        server.check()

    def test_get_next_number(self):
        """Verify the next number can be requested from the server."""
        number = server.get_next_number('req')
        number2 = server.get_next_number('req')
        self.assertIsNot(None, number)
        self.assertIsNot(None, number2)
        self.assertGreater(number, number2)
