"""
tests.PyRow.Concept2.ResponseTests
"""
# coding=utf-8
__author__ = 'UVD'

import mock
import unittest
from PyRow.Concept2.Response import Response


class ResponseTests(unittest.TestCase):
    """
    ResponseTests
    """

    def test_get_raw(self):
        """
        Response.get_raw - it should return the data
        :return:
        """
        results = mock.Mock()
        response = Response(results)

        self.assertEqual(
            response.get_raw(),
            results
        )

    def test_get_time(self):
        """
        Response.get_time - it should return the time remaining if it exists
        :return:
        """
        results = {
            'CSAFE_PM_GET_WORKTIME': [
                100,
                100
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_time(),
            2
        )

        # Test for None
        response = Response({})

        self.assertEqual(
            response.get_time(),
            None
        )

    def test_get_distance(self):
        """
        Response.get_distance - it should return the distance if it exists
        :return:
        """
        results = {
            'CSAFE_PM_GET_WORKDISTANCE': [
                100,
                100
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_distance(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_distance(),
            None
        )

    def test_get_pace(self):
        """
        Response.get_pace - it should return the pace if it exists
        :return:
        """
        results = {
            'CSAFE_GETPACE_CMD': [
                100
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_pace(),
            0.1
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_pace(),
            None
        )

    def test_get_pace_500(self):
        """
        Response.get_pace_500 - it should return the pace * 500 if it exists
        :return:
        """
        results = {
            'CSAFE_GETPACE_CMD': [
                100
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_pace_500(),
            50
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_pace_500(),
            None
        )

    def test_get_calories(self):
        """
        Response.get_calories - it should return the calories if it exists
        :return:
        """
        results = {
            'CSAFE_GETCALORIES_CMD': [
                100
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_calories(),
            100
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_calories(),
            None
        )

    def test_get_stroke_state(self):
        """
        Response.get_stroke_state - it should return the stroke state if it exists
        :return:
        """
        results = {
            'CSAFE_PM_GET_STROKESTATE': [
                100
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_stroke_state(),
            100
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_stroke_state(),
            None
        )

    def test_get_stroke_state_message(self):
        """
        Response.get_stroke_state_message - it should return the stroke state message if it exists
        :return:
        """
        results = {
            'CSAFE_PM_GET_STROKESTATE': [
                2
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_stroke_state_message(),
            'Drive'
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_stroke_state_message(),
            None
        )

    def test_get_status(self):
        """
        Response.get_status - it should return the status if it exists
        :return:
        """
        results = {
            'CSAFE_GETSTATUS_CMD': [
                5
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_status(),
            5
        )

        results = {
            'CSAFE_GETSTATUS_CMD': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_status(),
            4
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_status(),
            None
        )

    def test_get_status_message(self):
        """
        Response.get_status_message - it should return the status message if it exists
        :return:
        """
        results = {
            'CSAFE_GETSTATUS_CMD': [
                5
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_status_message(),
            'In Use'
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_status_message(),
            None
        )

    def test_get_spm(self):
        """
        Response.get_spm - it should return the SPM if it exists
        :return:
        """
        results = {
            'CSAFE_GETCADENCE_CMD': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_spm(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_spm(),
            None
        )

    def test_get_power(self):
        """
        Response.get_power - it should return the power if it exists
        :return:
        """
        results = {
            'CSAFE_GETPOWER_CMD': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_power(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_power(),
            None
        )

    def test_get_heartrate(self):
        """
        Response.get_heartrate - it should return the BPM if it exists
        :return:
        """
        results = {
            'CSAFE_GETHRCUR_CMD': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_heartrate(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_heartrate(),
            None
        )

    def test_get_force_plot(self):
        """
        Response.get_force_plot() - it should return the force plot if it exists
        :return:
        """
        results = {
            'CSAFE_PM_GET_FORCEPLOTDATA': [
                4,
                3,
                2,
                1
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_force_plot(),
            [3, 2]
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_force_plot(),
            None
        )
        pass

    def test_get_force_plot_strokestate(self):
        """
        Response.get_force_plot_strokestate - it should return the force plot strokestate if it exists
        :return:
        """
        results = {
            'CSAFE_PM_GET_STROKESTATE': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_force_plot_strokestate(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_force_plot_strokestate(),
            None
        )

    def test_get_user_id(self):
        """
        Response.get_user_id - it should return the user id if it exists
        :return:
        """
        results = {
            'CSAFE_GETID_CMD': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_user_id(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_user_id(),
            None
        )

    def test_get_workout_type(self):
        """
        Response.get_workout_type - it should return the workout type if it exists
        :return:
        """
        results = {
            'CSAFE_PM_GET_WORKOUTTYPE': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_workout_type(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_workout_type(),
            None
        )

    def test_get_workout_state(self):
        """
        Response.get_workout_state - it should return the workout state if it exists
        :return:
        """
        results = {
            'CSAFE_PM_GET_WORKOUTSTATE': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_workout_state(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_workout_state(),
            None
        )

    def test_get_workout_int_type(self):
        """
        Response.get_workout_int_type - it should return the workout interval type if it exists
        :return:
        """
        results = {
            'CSAFE_PM_GET_INTERVALTYPE': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_workout_int_type(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_workout_int_type(),
            None
        )

    def test_get_workout_int_count(self):
        """
        Response.get_workout_int_count - it should return the workout interval type if it exists
        :return:
        """
        results = {
            'CSAFE_PM_GET_WORKOUTINTERVALCOUNT': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_workout_int_count(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_workout_int_count(),
            None
        )

    def __get_version(self):
        results = {
            'CSAFE_GETVERSION_CMD': [
                100,  # Erg manufacturing id
                200,  # Erg cid
                300,  # Model
                400,  # Hw version
                500   # Sw version
            ]
        }

        return results

    def test_get_erg_mfgid(self):
        """
        Response.get_erg_mfgid - it should return the erg manufacturing id if it exists
        :return:
        """
        results = self.__get_version()

        response = Response(results)

        self.assertEqual(
            response.get_erg_mfgid(),
            100
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_erg_mfgid(),
            None
        )

    def test_get_erg_cid(self):
        """
        Response.get_erg_cid - it should return the erg CID if it exists
        :return:
        """
        results = self.__get_version()

        response = Response(results)

        self.assertEqual(
            response.get_erg_cid(),
            200
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_erg_cid(),
            None
        )

    def test_get_erg_model(self):
        """
        Response.get_erg_model - it should return the model number if it exists
        :return:
        """
        results = self.__get_version()

        response = Response(results)

        self.assertEqual(
            response.get_erg_model(),
            300
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_erg_model(),
            None
        )

    def test_get_erg_hwversion(self):
        """
        Response.get_erg_hwversion - it should return the hardward version if it exists
        :return:
        """
        results = self.__get_version()

        response = Response(results)

        self.assertEqual(
            response.get_erg_hwversion(),
            400
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_erg_hwversion(),
            None
        )

    def test_get_erg_swversion(self):
        """
        Response.get_erg_swversion - it should return the software version if it exists
        :return:
        """
        results = self.__get_version()

        response = Response(results)

        self.assertEqual(
            response.get_erg_swversion(),
            500
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_erg_swversion(),
            None
        )

    def test_get_erg_serial(self):
        """
        Response.get_erg_serial - it should return the serial number if it exists
        :return:
        """
        results = {
            'CSAFE_GETSERIAL_CMD': [
                20
            ]
        }

        response = Response(results)

        self.assertEqual(
            response.get_erg_serial(),
            20
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_erg_serial(),
            None
        )

    def __get_caps(self):
        results = {
            'CSAFE_GETCAPS_CMD': [
                100,  # Max Rx Frame
                150,  # Max Tx Frame
                200   # Min Interframe
            ]
        }

        return results

    def test_get_erg_maxrx(self):
        """
        Response.get_erg_maxrx - it should return the max rx frame if it exists
        :return:
        """
        results = self.__get_caps()

        response = Response(results)

        self.assertEqual(
            response.get_erg_maxrx(),
            100
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_erg_maxrx(),
            None
        )

    def test_get_erg_maxtx(self):
        """
        Response.get_erg_maxtx - it should return the max tx frame if it exists
        :return:
        """
        results = self.__get_caps()

        response = Response(results)

        self.assertEqual(
            response.get_erg_maxtx(),
            150
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_erg_maxtx(),
            None
        )

    def test_get_erg_mininterframe(self):
        """
        Response.get_erg_mininterframe - it should return the min interframe if it exists
        :return:
        """
        results = self.__get_caps()

        response = Response(results)

        self.assertEqual(
            response.get_erg_mininterframe(),
            200
        )

        # Test for none
        response = Response({})

        self.assertEqual(
            response.get_erg_mininterframe(),
            None
        )
