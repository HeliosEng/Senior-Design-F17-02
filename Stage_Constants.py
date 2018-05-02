#------------------------------------------------------------------------------------------------------------------------------------------
## Version 07.13.01
#------------------------------------------------------------------------------------------------------------------------------------------

#This Code was written by Keith Mody on Jan. 26th, 2018 and is designed to create
    #a reference of constants to use for the stage code files
#Reference .txt file labeled "Stage_Constants_Log.txt" for Changelog
#Changelog: For documenting changes follow this format: Version xx.xx date intitials: Changes to code

#------------------------------------------------------------------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------------------------------------------------------------------
from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply
import math

# Constants used between codes should be documented here

sl_YZ = int(500)                                   #sl = Stage Length; Total Stage Length 500 [mm]
sl_X = int(750)                                     #sl = Stage Length; Total Stage Length 750 [mm]

X_step_increment = 17 #This values is in [mm]
Y_step_increment = 0.5 #this valuye is in [mm]



Xabsolutemax = int(6047244) #The absolute max step position that the stage can reach
YZstagemax = int(4031496) #YZ Stage maxmum microstep
YZstagehalf = int(YZstagemax/2)
Xstagemax = int(4837795) #X Stage maximum so the mounting breadboard does not hit the stages This is 20% from the absoulte max
Xstagemin = int(1209448) #X Stage minimum so the mounting breadboard does not hit the stages this is 20% from the absoulte min or zero location



conv_YZ = YZstagemax/sl_YZ   #Conversion between distacne [metric mm] to zaber stage step size [unitless]
conv_X = Xabsolutemax/sl_X        #Conversion between distance [metric mm]
Xstagehalf = int((Xabsolutemax)/2)
Xalignedtostage = int(Xstagehalf + 46 * conv_X)

x_step_ms = int(X_step_increment * conv_X)
y_step_ms = int(Y_step_increment * conv_YZ)

Ystagelevel = YZstagemax - int(375*conv_YZ)
working_dist = 150                                      #working distance of laser [mm]
Z_stage_15cm = int(YZstagemax)

Xserial = int(49624) 
Yserial = int(49508)
Zserial = int(49507)
Rserial = int(49451)

deviceXmaxspeed = 153600    #default value 153600
deviceXmaxspeed = 153600    #default value 153600
deviceXmaxspeed = 153600    #default value 153600
deviceXmaxspeed = 153600    #default value 153600







