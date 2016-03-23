# PyRow

*NOTE: This code has not been thoroughly tested and may not function as advertised.
This documentation my contain mistakes or incomplete information.
Please report and findings to the author so that they may be addressed in a stable release.*

## ABOUT
PyRow is python code that allows one to interact with a Concept 2 Rowing Ergometer PM3 or PM4 monitor using python.  PyRow sends and receives information from the Ergometer using csafe commands or built in functions (listed below).  The goal of PyRow is to allow for multiple platforms to have easy access to the Ergometer.

For an explanation of the csafe commands please use the following documentation:
- [Concept2 PM Communication Interface Definition](http://www.concept2.com/service/software/software-development-kit)


*Need to download the SDK to get the document*


- [Communications Specification for Fitness Equipment](http://www.fitlinxx.com/CSAFE/)


Site: http://www.newhavenrowingclub.org/pyrow/

## LICENSE
Copyright (c) 2011 - 2015, Sam Gambrell

Licensed under the Simplified BSD License.


## REQUIREMENTS
PyRow has been tested on an Ubuntu machine with the software versions listed below, PyRow should be able to work on any machine that can run Python & PyUSB but this has not been tested and confirmed.

- [Python](http://python.org/) (Tested with 2.7.2)
- [libusb](http://www.libusb.org/)

        sudo apt-get install libudev-dev libusb-dev python

- [Walac's PyUSB](http://walac.github.io/pyusb)

        git clone git@github.com:walac/pyusb.git
        cd pyusb
        sudo python setup.py install

Other versions of the PyRow library have been tested on Windows.


## INSTALLING
After the software has become stable the software will be packaged as a module.  For now copying `pyrow.py`, `csafe_cmd.py`, and `csafe_dic.py` into the same directory as your code will work.

Include PyRow in your code with the following line of code:
`import pyrow`


## RUNNING
`pyrow.find()` - returns an array of all the ergs currently connected to the computer

---------------------------------------

`pyrow.pyrow(erg)` - creates an object for communicating with the erg, erg is obtained from the pyrow.find() function
 ex: creating a pyrow object from the first erg found
   ergs = pyrow.find()
   erg = pyrow.pyrow(ergs[0])

---------------------------------------

`pyrow.pyrow.getStatus()` - returns status of machine as a number
  - 0 = 'Error'
  - 1 = 'Ready'
  - 2 = 'Idle'
  - 3 = 'Have ID'
  - 4 = 'N/A'
  - 5 = 'In Use'
  - 6 = 'Pause'
  - 7 = 'Finished'
  - 8 = 'Manual'
  - 9 = 'Offline'

---------------------------------------

`pyrow.pyrow.getMonitor(forceplot=False)` - returns data from the monitor in dictionary format, keys listed below with descriptions
  - time = Monitor time in seconds
  - distance = Monitor distance in meters
  - spm = Strokes per Minute
  - power = Power in watts
  - pace = /500m pace
  - calhr = Calories Burned per Hours
  - calories = Total Calories Burned
  - heartrate = Current Heart Rate
  - status = Machine Status
 If keyvalue forceplot is set to true
  - forceplot = Force Plot Data
  - strokestate = Stroke State

---------------------------------------

`pyrow.pyrow.getForcePlot()` - returns force plot data and stroke state in dictionary format, keys listed below with descriptions
  - forceplot = Force Plot Data (array varying in length from 0 to 16)
  - strokestate = Stroke State
  - status = Machine status

---------------------------------------

`pyrow.pyrow.getWorkout()` - returns data related to the overall workout in dictionary format, keys listed below with descriptions
  - userid = User ID
  - type = Workout Type
  - state = Workout State
  - inttype = Interval Type
  - intcount = Workout Interval Count
  - status = Machine Status

---------------------------------------

`pyrow.pyrow.getErg()` - returns non workout related data about the erg in dictionary format, keys listed below with descriptions
  - mfgid = Manufacturing ID
  - cid = CID
  - model = Erg Model
  - hwversion = Hardware Version
  - swversion = Software Version
  - serial = Ascii Serial Number
  - maxrx = Max Rx Frame
  - maxtx = Max Tx Frame
  - mininterframe = Min Interframe
  - status = Machine status

---------------------------------------

`pyrow.pyrow.setClock()` - sets the clock on the erg equal to the clock on the computer

---------------------------------------

`pyrow.pyrow.setWorkout()` - if machine is in the ready state function will set the workout and display the start workout screen, allowable parameters are listed below (the current PM SDK does not allow for setting invervaled workouts)

**Choose one**

  `program=programNumber` - number from 0 to 10 (15 if the log card is installed), 1 thru 10 relate to workouts saved in the monitor.

  `time=[hours, minutes, seconds]` - Min allowable is 20 sec & max allowable is 9:59:59.

  `distance=meters` - Min allowable is 100 and max allowable is 20000.

 **Not required, can only chose if time or distance is set**

  `split=seconds` - If time is set or meters if distance is set, must be less than the total goal and greater
         than or equal to 20 seconds or 100 meters, cannot occur more then 30 times during the workout, time
         has a resolution of .01 sec

 **Not required, chose one**

  `pace=seconds` - Seconds for pace boat to complete 500 meters (/500m)
  `powerpace=watts` - Watts for pace boat to generate
  `calpace=cal` - Calories per hour for pace boat to burn

 ex: set a 2000m workout with a 500m split and a pace boat with a 2 minute pace (120 seconds)

  `erg.setWorkout(distance=2000, split=500, pace=120)`

---------------------------------------

`pyrow.pyrow.send(command)` - sends a csafe command to the rowing machine and returns the result. The command is an array and
 results are returned as a dictionary with the key being the csafe command name

 ex: setting a workout of 10 minutes with a split of 1 minute (60 seconds)

    command = ['CSAFE_SETTWORK_CMD', 0, 10, 0,'CSAFE_PM_SET_SPLITDURATION', 0, 60]
    erg.send(command)

 ex: getting pace and printing it out

    command = ['CSAFE_GETPACE_CMD',]
    result = erg.send(command)
    print "Stroke Pace = " + str(result['CSAFE_GETPACE_CMD'][0])
    print "Stroke Units = " + str(result['CSAFE_GETPACE_CMD'][1])

## FILES
`strokelog.py` - an example program that records time, distance, strokes per min, pace, and force plot data for each stroke to a csv file

`statshow.py` - an example program that displays the current machine, workout, and stroke status

`pyrow.py` - file to be loaded by user, used to connect to erg and send/receive data

`csafe_cmd.py` - converts between csafe commands and byte arrays for pyrow.py, user does not need to load this file directly

`csafe_dic.py` - contains dictionaries of the csafe commands to be used by csafe_cmd.py, user does not need to load this file directly
