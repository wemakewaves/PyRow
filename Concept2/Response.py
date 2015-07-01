# coding=utf-8
__author__ = 'UVD'

class Response:
    """
    Response
    """

    rower_state = ["Error", "Ready", "Idle", "Have ID", "N/A", "In Use", "Pause", "Finished", "Manual", "Offline"]

    rower_stroke = ["Wait for min speed", "Wait for acceleration", "Drive", "Dwelling", "Recovery"]

    def __init__(self, results):
        self.__results = results
        pass

    def get_time(self):
        """
        Get time remaining
        :return:
        """
        if 'CSAFE_PM_GET_WORKTIME' in self.__results.keys():
            return (self.__results['CSAFE_PM_GET_WORKTIME'][0] + self.__results['CSAFE_PM_GET_WORKTIME'][1])/100.
        return None

    def get_distance(self):
        """
        Distance in metres
        :return:
        """
        if 'CSAFE_PM_GET_WORKDISTANCE' in self.__results.keys():
            return (self.__results['CSAFE_PM_GET_WORKDISTANCE'][0] + self.__results['CSAFE_PM_GET_WORKDISTANCE'][1])/10.
        return None

    def get_pace(self):
        if 'CSAFE_GETPACE_CMD' in self.__results.keys():
            return float(self.__results['CSAFE_GETPACE_CMD'][0])/1000
        return None

    def get_pace_500(self):
        if self.get_pace():
            return self.get_pace() * 500
        return None

    def get_calories(self):
        if 'CSAFE_GETCALORIES_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETCALORIES_CMD'][0]
        return None

    def get_stroke_state(self):
        """
        :return int:
        """
        if 'CSAFE_PM_GET_STROKESTATE' in self.__results.keys():
            return self.__results['CSAFE_PM_GET_STROKESTATE'][0]
        return None

    def get_stroke_state_message(self):
        """
        :return String:
        """
        if self.get_stroke_state():
            return self.rower_stroke[self.get_stroke_state()]
        return None

    def get_status(self):
        """
        :return int:
        """
        if 'CSAFE_GETSTATUS_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETSTATUS_CMD'][0] & 0xF
        return None

    def get_status_message(self):
        """
        :return String:
        """
        if self.get_status():
            return self.rower_state[self.get_status()]
        return None

    def get_spm(self):
        """
        Strokes per minute
        :return:
        """
        if 'CSAFE_GETSTATUS_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETCADENCE_CMD'][0]
        return None

    def get_power(self):
        """
        Power in Watts:
        :return:
        """
        if 'CSAFE_GETPOWER_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETPOWER_CMD'][0]
        return None

    def get_heartrate(self):
        """
        Beats per minute
        :return:
        """
        if 'CSAFE_GETHRCUR_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETHRCUR_CMD'][0]
        return None

    def get_force_plot(self):
        """
        :return:
        """
        if 'CSAFE_PM_GET_FORCEPLOTDATA' in self.__results.keys():
            force_plot_data = self.__results['CSAFE_PM_GET_FORCEPLOTDATA']
            datapoints = force_plot_data[0] / 2

            return force_plot_data[1:(datapoints+1)]
        return None

    def get_force_plot_strokestate(self):
        """
        :return:
        """
        if 'CSAFE_PM_GET_STROKESTATE' in self.__results.keys():
            return self.__results['CSAFE_PM_GET_STROKESTATE'][0]
        return None

    def get_user_id(self):
        """
        :return:
        """
        if 'CSAFE_GETID_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETID_CMD'][0]
        return None
    
    def get_workout_type(self):
        """
        :return:
        """
        if 'CSAFE_PM_GET_WORKOUTTYPE' in self.__results.keys():
            return self.__results['CSAFE_PM_GET_WORKOUTTYPE'][0]
        return None

    def get_workout_state(self):
        if 'CSAFE_PM_GET_WORKOUTSTATE' in self.__results.keys():
            return self.__results['CSAFE_PM_GET_WORKOUTSTATE'][0]
        return None

    def get_workout_int_type(self):
        if 'CSAFE_PM_GET_INTERVALTYPE' in self.__results.keys():
            return self.__results['CSAFE_PM_GET_INTERVALTYPE'][0]
        return None

    def get_workout_int_count(self):
        if 'CSAFE_PM_GET_WORKOUTINTERVALCOUNT' in self.__results.keys():
            return self.__results['CSAFE_PM_GET_WORKOUTINTERVALCOUNT'][0]
        return None
        
    def get_erg_mfgid(self):
        if 'CSAFE_GETVERSION_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETVERSION_CMD'][0]
        return None
        
    def get_erg_cid(self):
        if 'CSAFE_GETVERSION_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETVERSION_CMD'][1]
        return None
        
    def get_erg_model(self):
        if 'CSAFE_GETVERSION_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETVERSION_CMD'][2]
        return None
        
    def get_erg_hwversion(self):
        if 'CSAFE_GETVERSION_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETVERSION_CMD'][3]
        return None
        
    def get_erg_swversion(self):
        if 'CSAFE_GETVERSION_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETVERSION_CMD'][4]
        return None
        
    def get_erg_serial(self):
        if 'CSAFE_GETSERIAL_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETSERIAL_CMD'][0]
        return None
        
    def get_erg_maxrx(self):
        if 'CSAFE_GETCAPS_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETCAPS_CMD'][0]
        return None
        
    def get_erg_maxtx(self):
        if 'CSAFE_GETCAPS_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETCAPS_CMD'][1]
        return None
        
    def get_erg_mininterframe(self):
        if 'CSAFE_GETCAPS_CMD' in self.__results.keys():
            return self.__results['CSAFE_GETCAPS_CMD'][2]
        return None

