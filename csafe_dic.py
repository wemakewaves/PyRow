#!/usr/bin/env python
#Copyright (c) 2011, Sam Gambrell
#Licensed under the Simplified BSD License.
#NOTE: This code has not been thoroughly tested and may not function as advertised.
# Please report and findings to the author so that they may be addressed in a stable release.

#Unique Frame Flags
Extended_Frame_Start_Flag = 0xF0
Standard_Frame_Start_Flag = 0xF1
Stop_Frame_Flag = 0xF2
Byte_Stuffing_Flag = 0xF3

#cmds['COMMAND_NAME'] = [0xCmd_Id, [Bytes, ...]]

cmds = {}

#Short Commands
cmds['CSAFE_GETSTATUS_CMD'] = [0x80, []]
cmds['CSAFE_RESET_CMD'] = [0x81, []]
cmds['CSAFE_GOIDLE_CMD'] = [0x82, []]
cmds['CSAFE_GOHAVEID_CMD'] = [0x83, []]
cmds['CSAFE_GOINUSE_CMD'] = [0x85, []]
cmds['CSAFE_GOFINISHED_CMD'] = [0x86, []]
cmds['CSAFE_GOREADY_CMD'] = [0x87, []]
cmds['CSAFE_BADID_CMD'] = [0x88, []]
cmds['CSAFE_GETVERSION_CMD'] = [0x91, []]
cmds['CSAFE_GETID_CMD'] = [0x92, []]
cmds['CSAFE_GETUNITS_CMD'] = [0x93, []]
cmds['CSAFE_GETSERIAL_CMD'] = [0x94, []]
cmds['CSAFE_GETODOMETER_CMD'] = [0x9B, []]
cmds['CSAFE_GETERRORCODE_CMD'] = [0x9C, []]
cmds['CSAFE_GETTWORK_CMD'] = [0xA0, []]
cmds['CSAFE_GETHORIZONTAL_CMD'] = [0xA1, []]
cmds['CSAFE_GETCALORIES_CMD'] = [0xA3, []]
cmds['CSAFE_GETPROGRAM_CMD'] = [0xA4, []]
cmds['CSAFE_GETPACE_CMD'] = [0xA6, []]
cmds['CSAFE_GETCADENCE_CMD'] = [0xA7, []]
cmds['CSAFE_GETUSERINFO_CMD'] = [0xAB, []]
cmds['CSAFE_GETHRCUR_CMD'] = [0xB0, []]
cmds['CSAFE_GETPOWER_CMD'] = [0xB4, []]

#Long Commands
cmds['CSAFE_AUTOUPLOAD_CMD'] = [0x01, [1,]] #Configuration (no affect)
cmds['CSAFE_IDDIGITS_CMD'] = [0x10, [1,]] #Number of Digits
cmds['CSAFE_SETTIME_CMD'] = [0x11, [1, 1, 1]] #Hour, Minute, Seconds
cmds['CSAFE_SETDATE_CMD'] = [0x12, [1, 1, 1]] #Year, Month, Day
cmds['CSAFE_SETTIMEOUT_CMD'] = [0x13, [1,]] #State Timeout
cmds['CSAFE_SETUSERCFG1_CMD'] = [0x1A, [0,]] #PM3 Specific Command (length computed)
cmds['CSAFE_SETTWORK_CMD'] = [0x20, [1, 1, 1]] #Hour, Minute, Seconds
cmds['CSAFE_SETHORIZONTAL_CMD'] = [0x21, [2, 1]] #Distance, Units
cmds['CSAFE_SETCALORIES_CMD'] = [0x23, [2,]] #Total Calories
cmds['CSAFE_SETPROGRAM_CMD'] = [0x24, [1, 1]] #Workout ID, N/A
cmds['CSAFE_SETPOWER_CMD'] = [0x34, [2, 1]] #Stroke Watts, Units
cmds['CSAFE_GETCAPS_CMD'] = [0x70, [1,]] #Capability Code

#PM3 Specific Short Commands
cmds['CSAFE_PM_GET_WORKOUTTYPE'] = [0x89, [], 0x1A]
cmds['CSAFE_PM_GET_DRAGFACTOR'] = [0xC1, [], 0x1A]
cmds['CSAFE_PM_GET_STROKESTATE'] = [0xBF, [], 0x1A]
cmds['CSAFE_PM_GET_WORKTIME'] = [0xA0, [], 0x1A]
cmds['CSAFE_PM_GET_WORKDISTANCE'] = [0xA3, [], 0x1A]
cmds['CSAFE_PM_GET_ERRORVALUE'] = [0xC9, [], 0x1A]
cmds['CSAFE_PM_GET_WORKOUTSTATE'] = [0x8D, [], 0x1A]
cmds['CSAFE_PM_GET_WORKOUTINTERVALCOUNT'] = [0x9F, [], 0x1A]
cmds['CSAFE_PM_GET_INTERVALTYPE'] = [0x8E, [], 0x1A]
cmds['CSAFE_PM_GET_RESTTIME'] = [0xCF, [], 0x1A]

#PM3 Specific Long Commands
cmds['CSAFE_PM_SET_SPLITDURATION'] = [0x05, [1, 4], 0x1A] #Time(0)/Distance(128), Duration
cmds['CSAFE_PM_GET_FORCEPLOTDATA'] = [0x6B, [1,], 0x1A] #Block Length
cmds['CSAFE_PM_SET_SCREENERRORMODE'] = [0x27, [1,], 0x1A] #Disable(0)/Enable(1)
cmds['CSAFE_PM_GET_HEARTBEATDATA'] = [0x6C, [1,], 0x1A] #Block Length


#resp[0xCmd_Id] = [COMMAND_NAME, [Bytes, ...]]
#negative number for ASCII
#use absolute max number for variable, (getid & getcaps)
resp = {}

#Response Data to Short Commands
resp[0x80] = ['CSAFE_GETSTATUS_CMD', [0,]] #Status
resp[0x81] = ['CSAFE_RESET_CMD', [0,]]
resp[0x82] = ['CSAFE_GOIDLE_CMD', [0,]]
resp[0x83] = ['CSAFE_GOHAVEID_CMD', [0,]]
resp[0x85] = ['CSAFE_GOINUSE_CMD', [0,]]
resp[0x86] = ['CSAFE_GOFINISHED_CMD', [0,]]
resp[0x87] = ['CSAFE_GOREADY_CMD', [0,]]
resp[0x88] = ['CSAFE_BADID_CMD', [0,]]
resp[0x91] = ['CSAFE_GETVERSION_CMD', [1, 1, 1, 2, 2]] #Mfg ID, CID, Model, HW Version, SW Version
resp[0x92] = ['CSAFE_GETID_CMD', [-5,]] #ASCII Digit (variable)
resp[0x93] = ['CSAFE_GETUNITS_CMD', [1,]]  #Units Type
resp[0x94] = ['CSAFE_GETSERIAL_CMD', [-9,]] #ASCII Serial Number
resp[0x9B] = ['CSAFE_GETODOMETER_CMD', [4, 1]] #Distance, Units Specifier
resp[0x9C] = ['CSAFE_GETERRORCODE_CMD', [3,]] #Error Code
resp[0xA0] = ['CSAFE_GETTWORK_CMD', [1, 1, 1]] #Hours, Minutes, Seconds
resp[0xA1] = ['CSAFE_GETHORIZONTAL_CMD', [2, 1]] #Distance, Units Specifier
resp[0xA3] = ['CSAFE_GETCALORIES_CMD', [2,]] #Total Calories
resp[0xA4] = ['CSAFE_GETPROGRAM_CMD', [1,]] #Program Number
resp[0xA6] = ['CSAFE_GETPACE_CMD', [2, 1]] #Stroke Pace, Units Specifier
resp[0xA7] = ['CSAFE_GETCADENCE_CMD', [2, 1]] #Stroke Rate, Units Specifier
resp[0xAB] = ['CSAFE_GETUSERINFO_CMD', [2, 1, 1, 1]] #Weight, Units Specifier, Age, Gender
resp[0xB0] = ['CSAFE_GETHRCUR_CMD', [1,]] #Beats/Min
resp[0xB4] = ['CSAFE_GETPOWER_CMD', [2, 1]] #Stroke Watts

#Response Data to Long Commands
resp[0x01] = ['CSAFE_AUTOUPLOAD_CMD', [0,]]
resp[0x10] = ['CSAFE_IDDIGITS_CMD', [0,]]
resp[0x11] = ['CSAFE_SETTIME_CMD', [0,]]
resp[0x12] = ['CSAFE_SETDATE_CMD', [0,]]
resp[0x13] = ['CSAFE_SETTIMEOUT_CMD', [0,]]
resp[0x1A] = ['CSAFE_SETUSERCFG1_CMD', [0,]] #PM3 Specific Command ID
resp[0x20] = ['CSAFE_SETTWORK_CMD', [0,]]
resp[0x21] = ['CSAFE_SETHORIZONTAL_CMD', [0,]]
resp[0x23] = ['CSAFE_SETCALORIES_CMD', [0,]]
resp[0x24] = ['CSAFE_SETPROGRAM_CMD', [0,]]
resp[0x34] = ['CSAFE_SETPOWER_CMD', [0,]]
resp[0x70] = ['CSAFE_GETCAPS_CMD', [11,]] #Depended on Capability Code (variable)

#Response Data to PM3 Specific Short Commands
resp[0x1A89] = ['CSAFE_PM_GET_WORKOUTTYPE', [1,]] #Workout Type
resp[0x1AC1] = ['CSAFE_PM_GET_DRAGFACTOR', [1,]] #Drag Factor
resp[0x1ABF] = ['CSAFE_PM_GET_STROKESTATE', [1,]] #Stroke State
#Work Time (seconds * 100), Fractional Work Time (1/100)
resp[0x1AA0] = ['CSAFE_PM_GET_WORKTIME', [4, 1]]
#Work Distance (meters * 10), Fractional Work Distance (1/10)
resp[0x1AA3] = ['CSAFE_PM_GET_WORKDISTANCE', [4, 1]]
resp[0x1AC9] = ['CSAFE_PM_GET_ERRORVALUE', [2,]] #Error Value
resp[0x1A8D] = ['CSAFE_PM_GET_WORKOUTSTATE', [1,]] #Workout State
resp[0x1A9F] = ['CSAFE_PM_GET_WORKOUTINTERVALCOUNT', [1,]] #Workout Interval Count
resp[0x1A8E] = ['CSAFE_PM_GET_INTERVALTYPE', [1,]] #Interval Type
resp[0x1ACF] = ['CSAFE_PM_GET_RESTTIME', [2,]] #Rest Time

#Response Data to PM3 Specific Long Commands
resp[0x1A05] = ['CSAFE_PM_SET_SPLITDURATION', [0,]] #No variables returned !! double check
resp[0x1A6B] = ['CSAFE_PM_GET_FORCEPLOTDATA', [
    1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]] #Bytes read, data ...
resp[0x1A27] = ['CSAFE_PM_SET_SCREENERRORMODE', [0,]]  #No variables returned !! double check
resp[0x1A6C] = ['CSAFE_PM_GET_HEARTBEATDATA', [
    1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]] #Bytes read, data ...
