"""
PyRow.Concept2.PerformanceMonitor
"""
# coding=utf-8
__author__ = 'UVD'

import usb.util
import time
from threading import Lock
from PyRow import csafe_cmd
from PyRow.Concept2.Response import Response


class PerformanceMonitor(object):
    """
    PerformanceMonitor
    This class provides an interface between PyRow and a PyRow.Concept2 Performance Monitor device
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
     iManufacturer          :    0x1 PyRow.Concept2
     iProduct               :    0x2 PyRow.Concept2 Performance Monitor 3 (PM3)
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
    TIMEOUT = 2000

    STROKE_WAIT_MIN_SPEED = 0
    STROKE_WAIT_FOR_ACCELERATION = 1
    STROKE_DRIVE = 2
    STROKE_DWELLING = 3
    STROKE_RECOVERY = 4

    STATE_ERROR = 0
    STATE_READY = 1
    STATE_IDLE = 2
    STATE_HAVE_ID = 3
    STATE_NA = 4
    STATE_IN_USE = 5
    STATE_PAUSE = 6
    STATE_FINISHED = 7
    STATE_MANUAL = 8
    STATE_OFFLINE = 9

    GET_STATUS = 'CSAFE_GETSTATUS_CMD'
    GET_TIME = 'CSAFE_PM_GET_WORKTIME'
    GET_DISTANCE = 'CSAFE_PM_GET_WORKDISTANCE'
    GET_CADENCE = 'CSAFE_PM_GETCADENCE_CMD'
    GET_POWER = 'CSAFE_GETPOWER_CMD'
    GET_STROKE_STATE = 'CSAFE_PM_GET_STROKESTATE'
    GET_PACE = 'CSAFE_GETPACE_CMD'
    GET_CALORIES = 'CSAFE_GETCALORIES_CMD'

    GO_FINISHED = 'CSAFE_GOFINISHED_CMD'
    GO_IDLE = 'CSAFE_GOIDLE_CMD'
    GO_READY = 'CSAFE_GOREADY_CMD'

    def __init__(self, device):
        """
        :param Device device:
        :return:
        """
        self.__device = device
        interface = device[0][(0, 0)]
        self.__in_address = interface[0].bEndpointAddress
        self.__out_address = interface[1].bEndpointAddress

        self.__manufacturer = usb.util.get_string(self.__device, self.__device.iManufacturer)
        self.__product = usb.util.get_string(self.__device, self.__device.iProduct)
        self.__serial_number = usb.util.get_string(self.__device, self.__device.iSerialNumber)

        self.__last_message = time.time()
        self.__lock = Lock()

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

    def send_commands(self, commands):
        """
        :param [] commands:
        :return Response:
        """
        self.__lock.acquire()
        now = time.time()
        delta = now - self.__last_message
        deltaraw = delta.seconds + delta.microseconds/1000000.
        if deltaraw < PerformanceMonitor.MIN_FRAME_GAP:
            time.sleep(PerformanceMonitor.MIN_FRAME_GAP - deltaraw)

        csafe = csafe_cmd.write(commands)

        length = self.__device.write(self.__out_address, csafe, timeout=PerformanceMonitor.TIMEOUT)
        self.__last_message = time.time()

        response = []
        while not response:
            try:
                transmission = self.__device.read(self.__in_address, length, timeout=2000)
                response = csafe_cmd.read(transmission)
            except Exception as e:
                raise e

        time.sleep(PerformanceMonitor.MIN_FRAME_GAP)
        self.__lock.release()

        return Response(response)

    def get_status(self):
        """
        Gets the current status from the Performance Monitor
        :return Response:
        """
        return self.send_commands([
            PerformanceMonitor.GET_STATUS
        ])

    def reset(self):
        """
        Resets the Performance Monitor or throws an Exception if unable to
        :return:
        """
        state = self.get_status()
        print "Current Status: {0}".format(state.get_status_message())

        manual = state.get_status() == PerformanceMonitor.STATE_MANUAL
        offline = state.get_status() == PerformanceMonitor.STATE_OFFLINE

        if manual or offline:
            # TODO: Make Exception class
            raise Exception("Ergometer is in: {0}".format(state.get_status_message()))

        finished = state.get_status() == PerformanceMonitor.STATE_FINISHED
        ready = state.get_status() == PerformanceMonitor.STATE_READY

        if not finished and not ready:
            self.send_commands([PerformanceMonitor.GO_FINISHED])

        self.send_commands([PerformanceMonitor.GO_IDLE])
        self.send_commands([PerformanceMonitor.GO_READY])
