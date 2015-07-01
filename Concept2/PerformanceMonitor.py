"""
Concept2.PerformanceMonitor
"""
# coding=utf-8
__author__ = 'UVD'

import usb.util
import time


class PerformanceMonitor(object):
    """
    PerformanceMonitor
    This class provides an interface between PyRow and a Concept2 Performance Monitor device
    Example device:
    DEVICE ID 17a4:0001 on Bus 001 Address 004 =================
     bLength                :   0x12 (18 bytes)
     bDescriptorType        :    0x1 Device
     bcdUSB                 :  0x110 USB 1.1
     bDeviceClass           :    0x0 Specified at interface
     bDeviceSubClass        :    0x0
     bDeviceProtocol        :    0x0
     bMaxPacketSize0        :    0x8 (8 bytes)
     idVendor               : 0x17a4
     idProduct              : 0x0001
     bcdDevice              :  0x100 Device 1.0
     iManufacturer          :    0x1 Concept2
     iProduct               :    0x2 Concept2 Performance Monitor 3 (PM3)
     iSerialNumber          :    0x3 400124190
     bNumConfigurations     :    0x1
      CONFIGURATION 1: 98 mA ===================================
       bLength              :    0x9 (9 bytes)
       bDescriptorType      :    0x2 Configuration
       wTotalLength         :   0x29 (41 bytes)
       bNumInterfaces       :    0x1
       bConfigurationValue  :    0x1
       iConfiguration       :    0x0
       bmAttributes         :   0x80 Bus Powered
       bMaxPower            :   0x31 (98 mA)
        INTERFACE 0: Human Interface Device ====================
         bLength            :    0x9 (9 bytes)
         bDescriptorType    :    0x4 Interface
         bInterfaceNumber   :    0x0
         bAlternateSetting  :    0x0
         bNumEndpoints      :    0x2
         bInterfaceClass    :    0x3 Human Interface Device
         bInterfaceSubClass :    0x0
         bInterfaceProtocol :    0x0
         iInterface         :    0x0
          ENDPOINT 0x83: Interrupt IN ==========================
           bLength          :    0x7 (7 bytes)
           bDescriptorType  :    0x5 Endpoint
           bEndpointAddress :   0x83 IN
           bmAttributes     :    0x3 Interrupt
           wMaxPacketSize   :   0x40 (64 bytes)
           bInterval        :    0x2
          ENDPOINT 0x4: Interrupt OUT ==========================
           bLength          :    0x7 (7 bytes)
           bDescriptorType  :    0x5 Endpoint
           bEndpointAddress :    0x4 OUT
           bmAttributes     :    0x3 Interrupt
           wMaxPacketSize   :   0x40 (64 bytes)
           bInterval        :    0x1
    """
    VENDOR_ID = 0x17a4
    PM_VERSION = {
        0x0001: "PM3",
        0x0002: "PM4",
        0x0003: "PM5"
    }

    MIN_FRAME_GAP = .050

    GET_TIME = 'CSAFE_PM_GET_WORKTIME'
    GET_DISTANCE = 'CSAFE_PM_GET_WORKDISTANCE'
    GET_CADENCE = 'CSAFE_PM_GETCADENCE_CMD'
    GET_POWER = 'CSAFE_PM_GETCADENCE_CMD'

    def __init__(self, device):
        """
        :param Device device:
        :return:
        """
        self.__device = device
        print vars(device)

        self.__manufacturer = usb.util.get_string(self.__device, self.__device.iManufacturer)
        self.__product = usb.util.get_string(self.__device, self.__device.iProduct)
        self.__serial_number = usb.util.get_string(self.__device, self.__device.iSerialNumber)

        self.__last_message = time.time()

    def get_manufacturer(self):
        """
        :return string:
        """
        return self.__manufacturer

    def get_product(self):
        """
        :return string:
        """
        return self.__product

    def get_serial_number(self):
        """
        :return string:
        """
        return self.__serial_number

    def get_pm_version(self):
        """
        :return string:
        """
        return PerformanceMonitor.PM_VERSION[self.__device.idProduct]
