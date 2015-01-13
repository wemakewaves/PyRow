#!/usr/bin/python2

import pyrow
import time

if __name__ == "__main__":
    ergs = list(pyrow.find())
    erg = pyrow.pyrow(ergs[0])
    print pyrow.pyrow.getStatus(erg)
    print pyrow.pyrow.getWorkout(erg)
    erg.setWorkout(distance=2000, split=100, pace=120)
    status = erg.getStatus()
    print status['status']
    while status['status'] == 5:
        command = ['CSAFE_GETPACE_CMD',]
        result = erg.send(command)
        print "Stroke Pace = " + str(result['CSAFE_GETPACE_CMD'][0])
        print "Stroke Units = " + str(result['CSAFE_GETPACE_CMD'][1])
        time.sleep(5);
        status = erg.getStatus()

    print "Workout Complete."
