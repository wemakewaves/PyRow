#!/usr/bin/env python
#Copyright (c) 2011, Sam Gambrell
#Licensed under the Simplified BSD License.

#This is an example file to show how to make use of pyrow
#Have the rowing machine on and plugged into the computer before starting the program
#The program will display any changes to the machine status, stroke state, or workout state

#NOTE: This code has not been thoroughly tested and may not function as advertised.
#Please report and findings to the author so that they may be addressed in a stable release.

import pyrow
import time

if __name__ == '__main__':
    #Connecting to erg
    ergs = list(pyrow.find())
    if len(ergs) == 0:
        exit("No ergs found.")
    erg = pyrow.pyrow(ergs[0])
    print "Connected to erg."

    #Create a dictionary of the different status states
    state = ['Error', 'Ready', 'Idle', 'Have ID', 'N/A', 'In Use',
             'Pause', 'Finished', 'Manual', 'Offline']

    stroke = ['Wait for min speed', 'Wait for acceleration', 'Drive', 'Dwelling', 'Recovery']

    workout = ['Waiting begin', 'Workout row', 'Countdown pause', 'Interval rest',
               'Work time inverval', 'Work distance interval', 'Rest end time', 'Rest end distance',
               'Time end rest', 'Distance end rest', 'Workout end', 'Workout terminate',
               'Workout logged', 'Workout rearm']

    command = ['CSAFE_GETSTATUS_CMD', 'CSAFE_PM_GET_STROKESTATE', 'CSAFE_PM_GET_WORKOUTSTATE']

    #prime status number
    cstate = -1
    cstroke = -1
    cworkout = -1


    erg.set_workout(distance=2000, split=100, pace=120)

    #Inf loop
    while 1:
        results = erg.send(command)
        if cstate != (results['CSAFE_GETSTATUS_CMD'][0] & 0xF):
            cstate = results['CSAFE_GETSTATUS_CMD'][0] & 0xF
            print "State " + str(cstate) + ": " + state[cstate]
        if cstroke != results['CSAFE_PM_GET_STROKESTATE'][0]:
            cstroke = results['CSAFE_PM_GET_STROKESTATE'][0]
            print "Stroke " + str(cstroke) + ": " + stroke[cstroke]
        if cworkout != results['CSAFE_PM_GET_WORKOUTSTATE'][0]:
            cworkout = results['CSAFE_PM_GET_WORKOUTSTATE'][0]
            print "Workout " + str(cworkout) + ": " + workout[cworkout]
        time.sleep(1)
