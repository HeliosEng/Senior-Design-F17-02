#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#https://media.readthedocs.org/pdf/nidaqmx-python/latest/nidaqmx-python.pdf
"""
Created on Thu Mar  8 09:05:13 2018

@author: svaughn
"""

import nidaqmx
from nidaqmx.constants import AcquisitionType, Edge
import numpy as np
import matplotlib.pyplot as plt
import csv



Samples_Per_Sec = 2000000 # This is just hertz.
Samples_Per_Ch_To_Read = 500000 # This number divided by Samples_Per_Second is the seconds of data that you collect. This is also the TOTAL number of samples you will end up with.
SPCTR = Samples_Per_Ch_To_Read
# xSpacing = np.linspace(0,Samples_Per_Ch_To_Read,Samples_Per_Sec) Commented out incase we need for plotting usage.
with nidaqmx.Task() as task: # creating task from NIDAQMX
	task.ai_channels.add_ai_voltage_chan("Dev1/ai0") # calling the channel we are reading from, in this case "Dev1/ai1"
	task.timing.cfg_samp_clk_timing(Samples_Per_Sec,"",Edge.RISING,AcquisitionType.FINITE,Samples_Per_Ch_To_Read) #setup timing parameters

	data = task.read(Samples_Per_Ch_To_Read) #Still gotta pass SPCTR into the read

	plt.plot(data, 'ro' , linewidth=2, markersize=1) # plotting data
	plt.axis([0,SPCTR,0,1])
plt.show()
np.savetxt('test1.txt', data, delimiter=' ')
