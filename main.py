#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 13:06:11 2018

@author: svaughn
"""
import FFT
import Stage_2D_Scan_Pattern
import Stage_Constants
import Stage_Controls
#mport Stage_Move
#import Stage_Safety
#import Stage_Scan
import Stage_Settings
import h5py
import time
FOO = 0

#SC.Home_All_Devices(deviceY, deviceZ, deviceR)

f = open('DataScan.txt', 'a')
deviceX, deviceY, deviceZ, deviceR, portZ, portYXR = Stage_Controls.init_system() #
##reply = deviceY.send(AsciiCommand("get pos"))
##Stage_Controls.ccs(reply)
Stage_Controls.abs_move(deviceX, Stage_Constants.Xalignedtostage + int(5 * Stage_Constants.conv_X)) #
Stage_Controls.abs_move(deviceY, (Stage_Constants.Ystagelevel + int(85*Stage_Constants.conv_YZ) )) # add  "+ int(85*Stage_Constants.conv_YZ" for mirror height 
Stage_Controls.abs_move(deviceZ, Stage_Constants.Z_stage_15cm)#
print(int(85*Stage_Constants.conv_YZ))

question = input('Do you want to load up the part? Y/N: ')
print(question)
if question == "Y":
    #Stage_Controls.Mount_All_Devices(deviceX, deviceY, deviceZ, deviceR)
    
    Stage_Controls.abs_move(deviceX, Stage_Constants.Xalignedtostage + int(5 * Stage_Constants.conv_X)) #
    Stage_Controls.abs_move(deviceY, (Stage_Constants.Ystagelevel + int(5 * Stage_Constants.conv_X))) # add  "+ int(85*Stage_Constants.conv_YZ" for mirror height 
    Stage_Controls.abs_move(deviceZ, 0)
    Stage_Controls.abs_move(deviceR, 1152000)
   
    question = input('Do you want to begin stage scan? Y/N: ')
    if question == "Y":

        Stage_Controls.abs_move(deviceR, 0)
        time.sleep(0.5)
        Stage_Controls.abs_move(deviceY, (Stage_Constants.Ystagelevel)) # add  "+ int(85*Stage_Constants.conv_YZ" for mirror height '''+ int(85*Stage_Constants.conv_YZ)''' 
        Stage_Controls.abs_move(deviceZ, Stage_Constants.Z_stage_15cm - int(5*Stage_Constants.conv_YZ))
        

        
        Approximate_X_Distance = input('What is the Approximate length of the part in cm: ')
        Approximate_Y_Distance = input('What is the Approximate Height of the part in cm: ')
        X_Dist_Shifted = (float(Approximate_X_Distance) + 0.5)*10
        Y_Dist_Shifted = (float(Approximate_Y_Distance) + 0.5)*10
        Stage_2D_Scan_Pattern.scan(X_Dist_Shifted,Y_Dist_Shifted,deviceX, deviceY, deviceZ, deviceR, f)
        
        #1152000
        #need to implement DAQ in scan
        
    else:
        print("Well fine then")
else:
   print(FOO)

print("Scan Complete")
f.close()
#h5py.close(data.h5py)
Stage_Controls.close_port(portZ)
Stage_Controls.close_port(portYXR)
