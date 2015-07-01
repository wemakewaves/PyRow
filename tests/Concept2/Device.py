"""
tests.Concept2.Device
"""
# coding=utf-8
__author__ = 'UVD'

import mock

class PM3(mock.Mock):
    """
    PM3 Device Mock
    """

    def __init__(self):
        """
        :return:
        """
        mock.Mock.__init__(self)

        self.iManufacturer = 0x1
        self.iProduct = 0x2
        self.iSerialNumber = 0x3

        self.idProduct = 0x0001

    def get_usb_util_string(self, key):
        """
        :param int key:
        :return:
        """
        if self.iManufacturer == key:
            return "Concept2"
        elif self.iProduct == key:
            return "Concept2 Performance Monitor 3 (PM3)"
        elif self.iSerialNumber == key:
            return "400124190"

        raise Exception("Unknown descriptor: {0}".format(key))
