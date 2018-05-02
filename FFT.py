#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 17:33:08 2018

@author: calebschelle Edited by: Keaton Scheffler
"""

#This section of Code will import all the nessicary modules that will be used for FFTing Data NOTE: CSV will be changed for HDF5
from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import csv
from scipy.signal import hanning



def Import_Data_Into_FFT(File_Name):

    return SOME_ARRAY
    
'''
This code is ment for importing a .csv that contains our test data this will be substituted for a .HDF5 file
#%% Import Data
# Import .csv file, convert to floats, turn 2D to 1D array
with open('TestData1.csv', newline='', encoding='utf_8') as f:
    reader = csv.reader(f)
    content =list(reader) #look up string to integer

list_str = np.array(content)
list_float = np.asfarray(list_str, dtype = 'float')# This is a numpy float array
c = list_float.flatten()

This section of code is only to FFT the data
#%% Fast Fourier Transform of Data
#start to end is half assed trimmed data
#transformed = np.fft.fft(c[start:end], norm='ortho')
transformed = np.fft.fft(c, norm='ortho')
im = plt.plot(transformed[:len(transformed)//2])
ylim = 0.1
plt.ylim(ymin=-ylim, ymax=ylim)
plt.show()
'''


#%% Trim data peaks
# Look for backward differences (trim peaks with big slopes)

def Cut_data():
#First we are going to import our data in this case it will be a file with the extension .HDF5 default this file will be called Signal_Data.HDF5
    Import_Data_Into_FFT(FILE_NAME)

#Here we will define a variable called Start_Point which is based on the first large peak so we make sure we get a full period of Data
    Start_Locs = detect_peaks(SOME_ARRAY, mph=4.5, mpd=1000, show=False, edge='rising')
    Start_Points = Start_Locs[0]
#Create an endding location for the period that is offset 400,000 points from the start location covering a full period MIGHT NEED TO BE ADJUSTED
    End_Point = Start_Point + 400000
#Now we will cut our data set and return it
    
    Cut_Data_Set = SOME_ARRAY[Start_Point:End_Point]
    return Cut_Data_Set
    

def Cut_data_iteration(i):
#First we are going to import our data in this case it will be a file with the extension .HDF5 default this file will be called Signal_Data.HDF5
    Import_Data_Into_FFT(FILE_NAME)

#Here we will define a variable called Start_Point which is based on the first large peak so we make sure we get a full period of Data
    Start_Locs = detect_peaks(SOME_ARRAY, mph=4.5, mpd=1000, show=False, edge='rising')
    Start_Points = Start_Locs[i]
#Create an endding location for the period that is offset 400,000 points from the start location covering a full period MIGHT NEED TO BE ADJUSTED
    End_Point = Start_Point + 400000
#Now we will cut our data set and return it
    
    Cut_Data_Set = SOME_ARRAY[Start_Point:End_Point]
    return Cut_Data_Set
    

def Average_Cut_Data():
    Data_Set_Iteration = np.empty(10,400000)
# This function will average 10 or so periods of the data to make sure that we have a good data set.
    for i in range(0, 9, 1):
        Data_Set_Iteration[i,:] = Cut_data_iteration(i)

#Averages out the Data_Set_Iteration data set and returns it

    Averaged_Data = np.mean(Data_Set_Iteration, axis = 0)
    return Averaged_Data
        

def FFT_Data():
#First we need to further refine the data that we rough cut before this is also using the Detect Peaks to cut the data

#This first section will take import the cut data from the Cut_Data function and will find the peak and valley values for this data set
    Cut_Data()
        
    Peak_Locs = detect_peaks(Cut_Data_Set, mph=4.5, mpd=1000, show=False, edge='both') #mph=min peak height, mpd=min peak dist
    Valley_Locs = detect_peaks(Cut_Data_Set, mpd=10000, valley=True, show=False, edge='both') #mph=min peak height, mpd=min peak dist
    Peak_Locs=np.asarray(Peak_Locs)
    Valley_Locs=np.asarray(valleylocs)

#Here we will take the peak and valley locations and find the values of the data at those points

#This section will further refine the data so only the data set that we want is used

#This section of code minimizes the peak to valley distance finding our inital data point to use for our data
    
    distance_1 = Valley_Locs[:] - Peak_Locs[1] # Find distance between first falling peak value and all valley locations
    min_pos_dist = min(i for i in distance_1 if i > 0) # Locate minimum positive distance to determine valley directly beyond peak
    min_pos_location = (np.where(distance_1 == min_pos_dist)) # Array position of minimum positive distance
    min_x_value = Valley_Locs[min_pos_location[0]] # Store value of array position as a variable

#This section of code minimizes the peak to valley distance finding our ending data point to use for our data
    
    distance_2 = Valley_Locs[:]-Peak_Locs[2] # Find distance between second rising peak value and all valley locations
    max_neg_dist = max(i for i in distance_2 if i < 0) # Locate maximum negative distance to determine valley directly before peak
    max_neg_location = (np.where(distance_2 == max_neg_dist)) # Array position of maximum negative distance
    max_x_value = Valley_Locs[max_neg_location[0]] # Store value of array position as a variable

#is the final refinement to the data set 
    Final_Cut_Data = Cut_Data_Set[min_x_value[0]:max_x_value[0]] # Plot the data we care about (trims off motor timing peaks)
    
#Plots the data set to show pre fft data
    plt.plot(Final_Cut_data)
    plt.show()

#Transforms the preFFT data into FFT data
    
    Transformed_Data = np.fft.fft(Final_Cut_Data, norm='ortho') # Perform a Fast Fourier Transform (FFT) on trimmed data
    im = plt.plot(Transformed_Data[:len(Transformed_Data)//2]) # Plot FFT data
    ylim = 0.1
    plt.ylim(ymin=-ylim, ymax=ylim)
    plt.show()
#Convolutes the FFT data into a hanning window
    
    window = np.hanning(51) # Create a Hanning window (weighted cosine curve) to reduce noise in signal
    conv = np.convolve(Transformed_Data, window) # Convolve the Hanning function with our FFT function
    plt.plot(Transformed_Data[:len(Transformed_Data)//2]) # Plot FFT data
    plt.plot(conv[:len(Transformed_Data)//2]) # Plot convolved data
    ylim = 2
    plt.xlim(xmin=0, xmax=5000)
    plt.ylim(ymin=-ylim, ymax=ylim)
    plt.show()

    return Transformed_Data

'''
#%% Generate SPIFI Signal
# From Jeff's Ideal SPIFI Signal in Mathematica

i = np.linspace(10,20,10000)
#sindata = np.sin(10*t)
#FFTData = abs(np.fft.fft(sindata))
#plt.plot(sindata)
#plt.plot(FFTData)

q = np.linspace(-100,100,10000)
#g = np.cos(i*q)

#for j in i:
for time in q:
    data = np.cos(1)
    plt.plot(data)
'''

'''This is the Detect_Peaks.py Code that was written by Marcos Duarte'''

__author__ = "Marcos Duarte, https://github.com/demotu/BMC"
__version__ = "1.0.4"
__license__ = "MIT"


def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None):

    """Detect peaks in data based on their amplitude and other features.

    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    ind : 1D array_like
        indeces of the peaks in `x`.

    Notes
    -----
    The detection of valleys instead of peaks is performed internally by simply
    negating the data: `ind_valleys = detect_peaks(-x)`
    
    The function can handle NaN's 

    See this IPython Notebook [1]_.

    References
    ----------
    .. [1] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

    Examples
    --------
    >>> from detect_peaks import detect_peaks
    >>> x = np.random.randn(100)
    >>> x[60:81] = np.nan
    >>> # detect all peaks and plot data
    >>> ind = detect_peaks(x, show=True)
    >>> print(ind)

    >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    >>> # set minimum peak height = 0 and minimum peak distance = 20
    >>> detect_peaks(x, mph=0, mpd=20, show=True)

    >>> x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
    >>> # set minimum peak distance = 2
    >>> detect_peaks(x, mpd=2, show=True)

    >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    >>> # detection of valleys instead of peaks
    >>> detect_peaks(x, mph=0, mpd=20, valley=True, show=True)

    >>> x = [0, 1, 1, 0, 1, 1, 0]
    >>> # detect both edges
    >>> detect_peaks(x, edge='both', show=True)

    >>> x = [-2, 1, -2, 2, 1, 1, 3, 0]
    >>> # set threshold = 2
    >>> detect_peaks(x, threshold = 2, show=True)
    """

    x = np.atleast_1d(x).astype('float64')
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan-1, indnan+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size-1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                    & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind


def _plot(x, mph, mpd, threshold, edge, valley, ax, ind):
    """Plot results of the detect_peaks function, see its help."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
    else:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(8, 4))

        ax.plot(x, 'b', lw=1)
        if ind.size:
            label = 'valley' if valley else 'peak'
            label = label + 's' if ind.size > 1 else label
            ax.plot(ind, x[ind], '+', mfc=None, mec='r', mew=2, ms=8,
                    label='%d %s' % (ind.size, label))
            ax.legend(loc='best', framealpha=.5, numpoints=1)
        ax.set_xlim(-.02*x.size, x.size*1.02-1)
        ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
        yrange = ymax - ymin if ymax > ymin else 1
        ax.set_ylim(ymin - 0.1*yrange, ymax + 0.1*yrange)
        ax.set_xlabel('Data #', fontsize=14)
        ax.set_ylabel('Amplitude', fontsize=14)
        mode = 'Valley detection' if valley else 'Peak detection'
        ax.set_title("%s (mph=%s, mpd=%d, threshold=%s, edge='%s')"
                     % (mode, str(mph), mpd, str(threshold), edge))
        # plt.grid()
        plt.show()
