#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 13:44:47 2018

@author: svaughn
"""

from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply
import Stage_Controls as SC
import Stage_Constants as Const
import Stage_Safety as SF
import Stage_Settings as SS
import h5py
import DAQ
import time
import math
import sys
import h5py
import datetime

f = h5py.File('data.hdf5', 'w')
grp1 = f.create_group('SPIFI')
grp2 = f.create_group('Stage')
grp3 = f.create_group('Calculations')
subgrp1 = grp1.create_group('SPIFI/data')
subgrp2 = grp2.create_group('Stage/position')
subgrp3 = grp3.create_group('Calculations/surface_metrology')



#SC.Mount_All_Devices(deviceX, deviceY, deviceZ, deviceR)

data = []

#If X and Y are given as mm
#Scanning part left to right
def Stage_2D_Scan_LR(x,y):
    zmove = math.ceil(Const.YZstagemax - Const.working_dist*Const.conv_YZ)
    x_incr = math.ceil(x*Const.conv_X)
    y_incr = math.ceil(15*Const.conv_YZ)
    xmove = int(Const.Xstagehalf + x_incr/2)
    ymove = Const.YZstagemax
    rmove = 0
    
    # Moving to initial Position
    SC.Settup_Move(deviceX, deviceY, deviceZ, deviceR, xmove, ymove, zmove, rmove)
    positions = SC.read_all_pos(deviceX, deviceY, deviceZ, deviceR)
    newdata = SC.combine_data(positions, data)
    
    # Continuous Movement until loop finishes
    y = math.ceil(y*Const.conv_YZ)
    ymove -= y_incr
    print(y_incr)
    count = 1
    while ymove >= (Const.YZstagemax - y):
        if count%2 != 0:
            xmove -= x_incr
            SC.abs_move(deviceX, xmove)
        else:
            xmove += x_incr
            SC.abs_move(deviceX, xmove)

        positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
        newdata = SC.combine_data(positions, newdata)
        
        SC.abs_move(deviceY, ymove)
        deviceY.poll_until_idle()
        positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
        newdata = SC.combine_data(positions, newdata)
        
        ymove -= y_incr
        print(ymove, Const.YZstagemax - y)
        count += 1

    if count%2 != 0:
        xmove -= x_incr
        SC.abs_move(deviceX, xmove)
    else:
        xmove += x_incr
        SC.abs_move(deviceX, xmove)

    positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
    newdata = SC.combine_data(positions, newdata)
    print(newdata)
    SC.write_pos_to_file("test.txt", newdata)

#If X and Y are given as mm
#Scanning part up and down
def Stage_2D_Scan_UD(x,y):
    zmove = math.ceil(Const.YZstagemax - Const.working_dist*Const.conv_YZ)
    x_init_incr = math.ceil(x*Const.conv_X/2)
    x_incr = math.ceil(15*Const.conv_X)
    y_incr = math.ceil(y*Const.conv_YZ)
    xmove = int(Const.Xstagehalf + x_init_incr)
    ymove = Const.YZstagemax
    rmove = 0
    
    # Moving to initial Position
    SC.Settup_Move(deviceX, deviceY, deviceZ, deviceR, xmove, ymove, zmove, rmove)
    positions = SC.read_all_pos(deviceX, deviceY, deviceZ, deviceR)
    newdata = SC.combine_data(positions, data)
    
    # Continuous Movement until loop finishes
    x_start = xmove
    x = math.ceil(x*Const.conv_X)
    xmove -= x_incr
    print(y_incr)
    count = 1
    while xmove >= (x_start - x):
        if count%2 != 0:
            ymove -= y_incr

            SC.abs_move(deviceY, ymove)

            deviceY.poll_until_idle()
        else:
            ymove += y_incr

            SC.abs_move(deviceY, ymove)
            deviceY.poll_until_idle()
            
        positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
        newdata = SC.combine_data(positions, newdata)
        
        SC.abs_move(deviceX, xmove)
        positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
        newdata = SC.combine_data(positions, newdata)
        
        xmove -= x_incr
        print(xmove, x_start - x)
        count += 1

    if count%2 != 0:
        ymove -= y_incr
        SC.abs_move(deviceY, ymove)
        deviceY.poll_until_idle()
    else:
        ymove += y_incr
        SC.abs_move(deviceY, ymove)
        deviceY.poll_until_idle()
        
    positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
    newdata = SC.combine_data(positions, newdata)
    print(newdata)
    SC.write_pos_to_file("test.txt", newdata)

def Cont_Pos_Stage_2D_Scan_UD(x,y):
    zmove = math.ceil(Const.YZstagemax - Const.working_dist*Const.conv_YZ)
    x_init_incr = math.ceil(x*Const.conv_X/2)
    x_incr = math.ceil(15*Const.conv_X)
    y_incr = math.ceil(y*Const.conv_YZ)
    xmove = int(Const.Xstagehalf + x_init_incr)
    ymove = Const.Ystagelevel
    rmove = 0
    
    # Moving to initial Position
    SC.Settup_Move(deviceX, deviceY, deviceZ, deviceR, xmove, ymove, zmove, rmove)
    
    
    # Continuous Movement until loop finishes
    x_start = xmove
    x = math.ceil(x*Const.conv_X)
    xmove -= x_incr
    print(y_incr)
    count = 1
    while xmove >= (x_start - x):
        if count%2 != 0:
            ymove += y_incr

            SC.abs_move(deviceY, ymove)
        else:
            ymove -= y_incr

            SC.abs_move(deviceY, ymove)
            
        positions = SC.cont_read_all_pos(deviceX,deviceY,deviceZ,deviceR)
        newdata = SC.combine_data(positions, newdata)
        
        newdata = SC.abs_move_cont_X(xmove, newdata, deviceX, deviceY, deviceZ, deviceR)
        
        xmove -= x_incr
        print(xmove, x_start - x)
        count += 1

    if count%2 != 0:
        ymove += y_incr
        SC.abs_move(deviceY, ymove)
    else:
        ymove -= y_incr
        SC.abs_move(deviceY, ymove)
    
    positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
    newdata = SC.combine_data(positions, newdata)
    SC.write_pos_to_file("test.txt", newdata)


def scan(x,y, deviceX, deviceY, deviceZ, deviceR, file_name):
    
    zmove = math.ceil(Const.YZstagemax) 
    y_conv_to_microsteps = math.ceil(y*Const.conv_YZ) #Converts the Y distance or the height of the part into microsteps ceiling it so we hit all steps
    x_init_incr = math.ceil(x*Const.conv_X/2) #This is the x distance or the part width converted into microsteps then dividing it by two to allow us to find the xmin and max values
    x_incr = Const.x_step_ms # this is the x step size equal to 15 mm's then converted into micro steps
    y_incr = Const.y_step_ms #this is our Y step size which is equal to 0.001 mm or 1 micron then converted into microsteps and ceiled
    
    xmove = int(Const.Xalignedtostage) #+ x_init_incr) #thi sets our inital movement location of the x stage so that it is on the left side of our part. Xstagehalf is the center location of the x stage
    ymove = Const.Ystagelevel #+ int(85 * Const.conv_YZ) # this is the default height of the stage such that the bottom left corner of the part is aligned to the center of the spifi laser beam

    ymax = Const.Ystagelevel+y_conv_to_microsteps # this is the default height of the Y stage
    ymin = Const.Ystagelevel # This creates the smallest y stage microstep location equal to the default stage location minus the part height in microsteps
    xmax = Const.Xstagehalf - x_init_incr # offset from center of x stage by a value of the length of the part divided by 2
    xmin = Const.Xstagehalf + x_init_incr # offset from center of x stage by a value of the length of the part divided by 2

    print(ymax, ymin, xmax, xmin)
    print(ymove)
    print(xmove)
    rmove = 0 #Sets our Rotational stage inital condition
    count=0 # initalizes a counter

    
    #SC.Settup_Move(deviceX, deviceY, deviceZ, deviceR, xmax, ymax, zmove, rmove)#Moves the stages to their inital positon
    SC.abs_move(deviceX, xmove)
    SC.abs_move(deviceY, ymove)
    SC.abs_move(deviceZ, zmove)

    positions = SC.read_all_pos(deviceX, deviceY, deviceZ, deviceR)
    newdata = SC.combine_data(positions, data)
    #x_start = xmin
    #SC.abs_move(deviceX, xstart)
    
    xmove = xmax
    while xmove <= xmax+int(x_init_incr*2) + Const.x_step_ms:
        if count%2 != 0:
            
            positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
            newdata = SC.combine_data(positions, newdata)
            timestamp = str(datetime.datetime.now()) #this creates a timestamped name
            s_data = subgrp2.create_dataset(timestamp, data=newdata)
            DAQ.Take_Data(file_name)
            
            while ymove <= ymax:
                print(ymove)
                ymove += y_incr##################
                SC.abs_move(deviceY, ymove)
                
                positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
                newdata = SC.combine_data(positions, newdata)        
                timestamp = str(datetime.datetime.now()) #this creates a timestamped name
                s_data = subgrp2.create_dataset(timestamp, data=newdata)
                DAQ.Take_Data(file_name)
              
            count += 1
           # xmove += x_incr##################
            SC.abs_move(deviceX, xmove)
            
        else:
            
            
            positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
            newdata = SC.combine_data(positions, newdata)
            timestamp = str(datetime.datetime.now()) #this creates a timestamped name
            s_data = subgrp2.create_dataset(timestamp, data=newdata)
            DAQ.Take_Data(file_name)
            
            while ymove >= ymin:
                print(ymove)
                ymove -= y_incr
                SC.abs_move(deviceY, ymove)
                
                positions = SC.read_all_pos(deviceX,deviceY,deviceZ,deviceR)
                newdata = SC.combine_data(positions, newdata)
                timestamp = str(datetime.datetime.now()) #this creates a timestamped name
                s_data = subgrp2.create_dataset(timestamp, data=newdata)
                DAQ.Take_Data(file_name)
                
            count +=1
            xmove += x_incr##################
            SC.abs_move(deviceX, xmove)


        
        
        

