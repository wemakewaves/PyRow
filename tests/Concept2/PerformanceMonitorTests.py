"""
tests.PyRow.Concept2.PerformanceMonitorTests
"""
# coding=utf-8
__author__ = 'UVD'

import unittest
import sys

import mock

from PyRow.tests.Concept2.Device import PM3
from PyRow.tests.Concept2.CsafeCmd import CsafeCmd

sys.modules['usb'] = mock.Mock()
sys.modules['usb.util'] = mock.Mock()
sys.modules['PyRow.Concept2.CsafeCmd'] = mock.Mock()  # Mocking the file
sys.modules['PyRow.Concept2.CsafeCmd'].CsafeCmd = CsafeCmd()

def usb_util_get_string_side_effect(device, key):
    """
    :param device:
    :param key:
    :return:
    """
    return device.get_usb_util_string(key)

sys.modules['usb'].util.get_string = mock.Mock(side_effect=usb_util_get_string_side_effect)

sys.modules['Lock'] = mock.Mock()
sys.modules['Lock'].acquire = mock.Mock()

from PyRow.Concept2.PerformanceMonitor import PerformanceMonitor
from PyRow.Concept2.Response import Response


class PerformanceMonitorTests(unittest.TestCase):
    """
    Tests for PerformanceMonitor
    """

    def setUp(self):
        """
        Set up the instance before each test
        :return:
        """
        self.device = PM3()
        sys.modules['PyRow.Concept2.CsafeCmd'].CsafeCmd.set_responses([
            {
                'CSAFE_GETSTATUS_CMD': [1]  # Ready state
            },
            {
                'CSAFE_GETSTATUS_CMD': [2]  # Idle state
            },
            {
                'CSAFE_GETSTATUS_CMD': [2]
            },
            {
                'CSAFE_GETSTATUS_CMD': [1]
            },
            {
                'CSAFE_GETSTATUS_CMD': [1]
            }
        ])
        self.performance_monitor = PerformanceMonitor(self.device)

    def test_get_manufacturer(self):
        """
        PerformanceMonitor.get_manufacturer - it should return the name of the manufacturer
        :return:
        """
        self.assertEqual(
            self.performance_monitor.get_manufacturer(),
            "Concept2"
        )

    def test_get_product(self):
        """
        PerformanceMonitor.get_product - it should the name of the product
        :return:
        """
        self.assertEqual(
            self.performance_monitor.get_product(),
            "Concept2 Performance Monitor 3 (PM3)"
        )

    def test_serial_number(self):
        """
        PerformanceMonitor.get_serial_number - it should return the serial number
        :return:
        """
        self.assertEqual(
            self.performance_monitor.get_serial_number(),
            "400124190"
        )

    def test_get_pm_version(self):
        """
        PerformanceMonitor.get_pm_version - it should return the PM Version
        :return:
        """
        self.assertEqual(
            self.performance_monitor.get_pm_version(),
            "PM3"
        )

    def test_send_commands(self):
        """
        PerformanceMonitor.send_commands - it should send commands to the Ergometer and return the response
        :return:
        """
        # It should block any other requests to the device by locking the object


        # It should return a Response object
        sys.modules['PyRow.Concept2.CsafeCmd'].CsafeCmd.set_responses([
            {
                'CSAFE_GETSTATUS_CMD': [2]  # Idle state
            }
        ])
        self.assertEqual(
            self.performance_monitor.send_commands([PerformanceMonitor.GET_STATUS]).__class__,
            Response
        )

    def test_get_status(self):
        """
        PerformanceMonitor.get_status - it should return a Response with the PM's status in
        :return:
        """
        pass