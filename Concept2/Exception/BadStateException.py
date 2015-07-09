"""
PyRow.Concept2.Exception.BadStateException
"""

# coding=utf-8
__author__ = 'UVD'


class BadStateException(Exception):
    """
    BadStateException
    """

    def __init__(self, device, state):
        """
        :param PerformanceMonitor device:
        :param string state:
        :return:
        """
        self.__device = device
        self.__state = state

    def get_device(self):
        """
        :return PerformanceMonitor:
        """
        return self.__device

    def __str__(self):
        """
        :return string:
        """
        return "{0} has state: {1}".format(self.__device.get_serial_number(), self.__state)
