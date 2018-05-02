#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 20:21:05 2018
This code takes the x y positional data from a single scan, rotates it per the 
known theta of the part in relation to the cylindrical lens. It then appends 
the newly calculated x_prime and y_prime data to the existing array to be 
processed later. 
@author: svaughn
"""
def linerotate(theta_stage, data_points, x_width, y_height, line_width, z_intensity):
    import numpy as np
    import math
    
    theta = theta_stage                # angle of cylindrical lens in degrees from ground
    theta = math.radians(theta) # converts to radians to use in math.cos/sin func
    num = data_points                  # numbers of points
    height_val = y_height       # takes the y value from stage, before conversion
    
    x = np.linspace(x_width,(x_width+line_width),num)   # this will ultimately take x and y line info from stage 
    y = np.full((1, num), height_val) 
    x_prime = np.append(x * math.cos(theta) - y * math.sin(theta)) #applies angle to x values
    y_prime = np.append(x * math.sin(theta) + y * math.cos(theta)) # applies angle to y values
    
    return x_prime
    return y_prime
