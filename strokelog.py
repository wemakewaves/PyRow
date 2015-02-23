#!/usr/bin/env python
#Copyright (c) 2011, Sam Gambrell
#Licensed under the Simplified BSD License.

#This is an example file to show how to make use of pyrow
#Have the rowing machine on and plugged into the computer before starting the program
#The program will record Time, Distance, SPM, Pace, and Force Data for each
#stroke and save it to 'workout.csv'

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

    #Open and prepare file
    write_file = open('workout.csv', 'w')
    write_file.write('Time, Distance, SPM, Pace, Force Plot\n')

    #Loop until workout has begun
    workout = erg.get_workout()
    print "Waiting for workout to start ..."
    while workout['state'] == 0:
        time.sleep(1)
        workout = erg.get_workout()
    print "Workout has begun"

    #Loop until workout ends
    while workout['state'] == 1:

        forceplot = erg.get_force_plot()
        #Loop while waiting for drive
        while forceplot['strokestate'] != 2 and workout['state'] == 1:
            #ToDo: sleep?
            forceplot = erg.get_force_plot()
            workout = erg.get_workout()

        #Record force data during the drive
        force = forceplot['forceplot'] #start of pull (when strokestate first changed to 2)
        monitor = erg.get_monitor() #get monitor data for start of stroke
        #Loop during drive
        while forceplot['strokestate'] == 2:
            #ToDo: sleep?
            forceplot = erg.get_force_plot()
            force.extend(forceplot['forceplot'])

        forceplot = erg.get_force_plot()
        force.extend(forceplot['forceplot'])


        #Write data to write_file
        workoutdata = str(monitor['time']) + "," + str(monitor['distance']) + "," + \
            str(monitor['spm']) + "," + str(monitor['pace']) + ","

        forcedata = ",".join([str(f) for f in force])
        write_file.write(workoutdata + forcedata + '\n')

        #Get workout conditions
        workout = erg.get_workout()

    write_file.close()
    print "Workout has ended"
