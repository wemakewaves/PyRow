"""
PyRow.Concept2.PerformanceMonitor
"""
# coding=utf-8
__author__ = 'UVD'

import usb.util
from usb import USBError
import sys
import time
from threading import Lock
from PyRow import csafe_cmd
from PyRow.Concept2.Response import Response
from PyRow.Concept2.Exception.BadStateException import BadStateException


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
    GO_IN_USE = 'CSAFE_GOINUSE_CMD'
    RESET = 'CSAFE_RESET_CMD'

    SET_WORKOUT = 'CSAFE_SETTWORK_CMD'
    SET_HORIZONTAL = 'CSAFE_SETHORIZONTAL_CMD'
    SET_SPLIT_DURATION = 'CSAFE_PM_SET_SPLITDURATION'
    SET_POWER = 'CSAFE_SETPOWER_CMD'
    SET_PROGRAM = 'CSAFE_SETPROGRAM_CMD'

    @staticmethod
    def find():
        ergs = usb.core.find(find_all=True, idVendor=PerformanceMonitor.VENDOR_ID)
        if ergs is None:
            raise ValueError('Ergs not found')
        return ergs

    def __init__(self, device):
        """
        :param Device device:
        :return:
        """
        self.__device = device
        if sys.platform != 'win32':
            if device.is_kernel_driver_active(0):
                device.detach_kernel_driver(0)
            else:
                print "DEBUG: usb kernel driver not on " + sys.platform

        usb.util.claim_interface(device, 0)

        try:
            device.set_configuration()
        except USBError as e:
            pass

        interface = device[0][(0, 0)]
        self.__in_address = interface[0].bEndpointAddress
        self.__out_address = interface[1].bEndpointAddress

        self.__manufacturer = usb.util.get_string(self.__device, self.__device.iManufacturer)
        self.__product = usb.util.get_string(self.__device, self.__device.iProduct)
        self.__serial_number = usb.util.get_string(self.__device, self.__device.iSerialNumber)

        self.__last_message = time.time()
        self.__lock = Lock()

        self.reset()

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
        if delta < PerformanceMonitor.MIN_FRAME_GAP:
            time.sleep(PerformanceMonitor.MIN_FRAME_GAP - delta)

        c_safe = csafe_cmd.write(commands)

        length = self.__device.write(self.__out_address, c_safe, timeout=PerformanceMonitor.TIMEOUT)
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
        response = self.get_status()
        print "Current Status: {0}".format(response.get_status_message())

        manual = response.get_status() == PerformanceMonitor.STATE_MANUAL
        offline = response.get_status() == PerformanceMonitor.STATE_OFFLINE

        if manual or offline:
            raise BadStateException(self, response.get_status_message())

        finished = response.get_status() == PerformanceMonitor.STATE_FINISHED
        ready = response.get_status() == PerformanceMonitor.STATE_READY

        if not finished and not ready:
            self.send_commands([PerformanceMonitor.GO_FINISHED])
            while self.get_status().get_status() != PerformanceMonitor.STATE_FINISHED:
                print "Waiting for Finish"

        self.send_commands([PerformanceMonitor.GO_IDLE])
        while self.get_status().get_status() != PerformanceMonitor.STATE_IDLE:
            print "Waiting for Idle"
        self.send_commands([PerformanceMonitor.GO_READY])
        while self.get_status().get_status() != PerformanceMonitor.STATE_READY:
            print "Waiting for Ready"

    def set_workout(self,
                    program=None,
                    workout_time=None,
                    distance=None,
                    split=None,
                    pace=None,
                    cal_pace=None,
                    power_pace=None):
        """
        If machine is in the ready state, function will set the
        workout and display the start workout screen
        """

        self.reset()
        command = []

        # Set Workout Goal
        program_num = 0
        if program is not None:
            self.__validate_value(program, "Program", 0, 15)
            program_num = program
        elif workout_time is not None:
            if len(workout_time) == 1:
                # if only seconds in workout_time then pad minutes
                workout_time.insert(0, 0)
            if len(workout_time) == 2:
                # if no hours in workout_time then pad hours
                workout_time.insert(0, 0)
            self.__validate_value(workout_time[0], "Time Hours", 0, 9)
            self.__validate_value(workout_time[1], "Time Minutes", 0, 59)
            self.__validate_value(workout_time[2], "Time Seconds", 0, 59)

            if workout_time[0] == 0 and workout_time[1] == 0 and workout_time[2] < 20:
                # checks if workout is < 20 seconds
                raise ValueError("Workout too short")

            command.extend([PerformanceMonitor.SET_WORKOUT, workout_time[0],
                            workout_time[1], workout_time[2]])

        elif distance is not None:
            self.__validate_value(distance, "Distance", 100, 50000)
            command.extend([PerformanceMonitor.SET_HORIZONTAL, distance, 36])  # 36 = meters

        # Set Split
        if split is not None:
            if workout_time is not None and program is None:
                split_time = int(split * 100)
                # total workout workout_time (1 sec)
                time_raw = workout_time[0] * 3600 + workout_time[1] * 60 + workout_time[2]
                # split workout_time that will occur 30 workout_times (.01 sec)
                min_split = int(time_raw/30*100+0.5)
                self.__validate_value(split_time, "Split Time", max(2000, min_split), time_raw*100)
                command.extend([PerformanceMonitor.SET_SPLIT_DURATION, 0, split_time])
            elif distance is not None and program is None:
                min_split = int(distance/30+0.5) # split distance that will occur 30 workout_times (m)
                self.__validate_value(split, "Split distance", max(100, min_split), distance)
                command.extend([PerformanceMonitor.SET_SPLIT_DURATION, 128, split])
            else:
                raise ValueError("Cannot set split for current goal")

        # Set Pace
        if pace is not None:
            power_pace = int(round(2.8 / ((pace / 500.) ** 3)))
        elif cal_pace is not None:
            power_pace = int(round((cal_pace - 300.)/(4.0 * 0.8604)))
        if power_pace is not None:
            command.extend([PerformanceMonitor.SET_POWER, power_pace, 88])  # 88 = watts

        command.extend([PerformanceMonitor.SET_PROGRAM, program_num, 0, PerformanceMonitor.GO_IN_USE])

        self.send_commands(command)

        if not self.__wait_for_workout(command, workout_time, distance):
            self.set_workout(
                program,
                workout_time,
                distance,
                split,
                pace,
                cal_pace,
                power_pace
            )

    @staticmethod
    def __validate_value(value, label, minimum, maximum):
        """
        Checks that value is an integer and within the specified range
        """
        if type(value) is not int:
            raise TypeError(label)
        if not minimum <= value <= maximum:
            raise ValueError(label + " outside of range")
        return True

    def __wait_for_workout(self, command, workout_time, distance, max_attempts=5):
        """
        :param command:
        :param workout_time:
        :param distance:
        :return:
        """
        attempts = 0
        while attempts < max_attempts:
            in_use = self.get_status().get_status() == PerformanceMonitor.STATE_IN_USE

            if PerformanceMonitor.SET_HORIZONTAL in command and in_use:
                if self.send_commands([PerformanceMonitor.GET_DISTANCE]).get_distance() == distance:
                    return True

            elif PerformanceMonitor.SET_WORKOUT in command and in_use:
                length = workout_time[0]*60*60 + workout_time[1]*60 + workout_time[2]
                if self.send_commands([PerformanceMonitor.GET_TIME]).get_time() == length:
                    return True

            attempts += 1
        return False
