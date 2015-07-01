"""
tests.PyRow.Concept2.PerformanceMonitorTests
"""
# coding=utf-8
__author__ = 'UVD'

import unittest
import mock


from tests.Concept2.Device import PM3

import sys
sys.modules['usb'] = mock.Mock()
sys.modules['usb.util'] = mock.Mock()
def usb_util_get_string_side_effect(device, key):
    """
    :param device:
    :param key:
    :return:
    """
    return device.get_usb_util_string(key)

sys.modules['usb'].util.get_string = mock.Mock(side_effect=usb_util_get_string_side_effect)

from PyRow.Concept2.PerformanceMonitor import PerformanceMonitor

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
        self.performance_monitor = PerformanceMonitor(self.device)

    def test_get_manufacturer(self):
        """
        PerformanceMonitor.get_manufacturer - it should return the name of the manufacturer
        :return:
        """
        self.assertEqual(
            self.performance_monitor.get_manufacturer(),
            "PyRow.Concept2"
        )

    def test_get_product(self):
        """
        PerformanceMonitor.get_product - it should the name of the product
        :return:
        """
        self.assertEqual(
            self.performance_monitor.get_product(),
            "PyRow.Concept2 Performance Monitor 3 (PM3)"
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
        PerformanceMonitory.get_pm_version - it should return the PM Version
        :return:
        """
        self.assertEqual(
            self.performance_monitor.get_pm_version(),
            "PM3"
        )
