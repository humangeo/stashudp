#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

"""Tests for StashUDP."""

import unittest
from humangeo.stashudp import StashUdpHandler

class StashUDPTestCase(unittest.TestCase):
    """
    Simple test cases to ensure the library is installed and capable of emitting
    packets on the network.
    """

    def setUp(self):
        """Initialize a handler"""
        TARGET_IP = '172.20.9.20'
        ES_UDP_PORT = 9700
        stasher = StashUdpHandler()
        stasher.udp_host = TARGET_IP
        stasher.udp_port = ES_UDP_PORT
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(stasher)

    def tearDown(self):
        """Nothing to see here."""
        pass

    def test_debug(self):
        logger = self.logger
        logger.debug("This is a witty message from inside the unit test (test_debug)")
        assert True

if __name__ == '__main__':
    unittest.main()