#!/usr/bin/env python
#Copyright (c) 2011, Sam Gambrell
#Licensed under the Simplified BSD License.

#This is an example file to show how to make use of pyrow
#Have the rowing machine on and plugged into the computer before starting the program
#The program will record Time, Distance, SPM, Pace, and Force Data for each stroke and save it to 'workout.csv'

#NOTE: This code has not been thoroughly tested and may not function as advertised.
#Please report and findings to the author so that they may be addressed in a stable release.

import pyrow
import time

#Connecting to erg
ergs = list(pyrow.find())
if len(ergs) == 0: exit("No ergs found.")
erg = pyrow.pyrow(ergs[0])
print "Connected to erg."

#Open and prepare file
file = open('workout.csv', 'w')
file.write('Time, Distance, SPM, Pace, Force Plot\n')

#Loop until workout has begun
workout = erg.getWorkout()
print "Waiting for workout to start ..."
while workout['state'] == 0:
    time.sleep(1)
    workout = erg.getWorkout()
print "Workout has begun"

#Loop until workout ends
while workout['state'] == 1:

    forceplot = erg.getForcePlot()
    #Loop while waiting for drive
    while forceplot['strokestate'] != 2 and workout['state']  == 1:
        #ToDo: sleep?
        forceplot = erg.getForcePlot()
        workout = erg.getWorkout()



    #Record force data during the drive
    force = forceplot['forceplot'] #start of pull (when strokestate first changed to 2)
    monitor = erg.getMonitor() #get monitor data for start of stroke
    #Loop during drive
    while forceplot['strokestate'] == 2:
        #ToDo: sleep?
        forceplot = erg.getForcePlot()
        force.extend(forceplot['forceplot'])
    else: #Get force data from end of stroke
        forceplot = erg.getForcePlot()
        force.extend(forceplot['forceplot'])


    #Write data to file
    workoutdata = str(monitor['time']) + "," + str(monitor['distance']) + "," + str(monitor['spm']) + "," + str(monitor['pace']) + ","
    forcedata = ",".join([str(f) for f in force])
    file.write(workoutdata + forcedata + '\n')

    #Get workout conditions
    workout = erg.getWorkout()

file.close()
print "Workout has ended"
