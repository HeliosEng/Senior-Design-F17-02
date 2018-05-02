#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 09:16:43 2018
This 
@author: svaughn
"""

import matplotlib.pyplot as plt
import numpy as np
import math

theta = 10                  # angle of cylindrical lens in degrees
theta = math.radians(theta) # converts to radians to use in math.cos/sin
num = 100                 # numbers of points
delta = 1/10               # width of the intensity grid
m = num 
n = num
height_val = 7              # takes the y value from stage, before conversion

x = np.linspace(2,10,num)   # this will ultimately take x and y line info from stage 
y = np.full((1, num), height_val) 
intensity = 255*(np.random.rand(1,num))             # scales intensity values 
x_prime = x * math.cos(theta) - y * math.sin(theta) #applies angle to x values
x_max = np.amax(x_prime)
y_prime = x * math.sin(theta) + y * math.cos(theta) # applies angle to y values

count = np.zeros((m,n))
pixel = np.zeros((m,n))
i = (x_prime/delta).astype(int)
j = (y_prime/delta).astype(int)
count[i,j] += 1
#count = np.rot90(np.fliplr(count),-2)

for x in range(0,len(i[0])):
    pixel[i[0][x],j[0][x]] = intensity[0,x]

#pixel[i,j] /= count[i,j]

x_size = x_prime.size 
y_size = y_prime.size      


plt.imshow(count)


#data = np.array([[7, 4, 6], [7, 7, 6], [4, 7, 9]])
#
#plt.imshow(data, 'gray', origin='lower')