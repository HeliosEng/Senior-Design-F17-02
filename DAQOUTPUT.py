#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 13:04:44 2018

@author: svaughn
"""

import nidaqmx
from nidaqmx.constants import AcquisitionType, Edge
import numpy as np
import matplotlib.pyplot as plt
import h5py
import datetime

def Take_Data():
    Samples_Per_Sec = 1000000 # This is just hertz.
    Samples_Per_Ch_To_Read = 1000 # This number divided by Samples_Per_Second is the seconds of data that you collect. This is also the TOTAL number of samples you will end up with.
    SPCTR = Samples_Per_Ch_To_Read
# xSpacing = np.linspace(0,Samples_Per_Ch_To_Read,Samples_Per_Sec) Commented out incase we need for plotting usage.
    with nidaqmx.Task() as task: # creating task from NIDAQMX
        task.ai_channels.add_ai_voltage_chan("Dev1/ai1") # calling the channel we are reading from, in this case "Dev1/ai1"
        task.timing.cfg_samp_clk_timing(Samples_Per_Sec,"",Edge.RISING,AcquisitionType.FINITE,Samples_Per_Ch_To_Read) #setup timing parameters

        data_read = task.read(Samples_Per_Ch_To_Read) #Still gotta pass SPCTR into the read
        plt.plot(data_read, 'ro' , linewidth=2, markersize=12) # plotting data
        plt.axis([0,SPCTR,0,12])
        plt.show()
    '''  
    timestamp = str(datetime.datetime.now()) #this creates a timestamped data name called in p_data
    f = h5py.File("dataTEST.hdf5", "w")
    grp1 = f.create_group('SPIFI')
    subgrp1 = grp1.create_group('SPIFI/photodiode_data')
    p_data = subgrp1.create_dataset(timestamp, data=data_read)
'''
Take_Data()
