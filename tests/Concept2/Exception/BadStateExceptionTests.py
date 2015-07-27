"""
tests.PyRow.Concept2.Exception.BadStateException
"""
# coding=utf-8
import unittest
from PyRow.Concept2.Exception.BadStateException import BadStateException
from PyRow.tests.Concept2.Device import PM3

__author__ = 'UVD'


class BadStateExceptionTests(unittest.TestCase):
    """
    Tests for BadStateException
    """

    def setUp(self):
        """
        :return:
        """
        self.device = PM3()
        self.bad_state_exception = BadStateException(Exception)

    def test_get_device(self):
        """
        :return:
        """
        self.assertEqual(
            self.bad_state_exception.get_device(),
            self.device
        )
