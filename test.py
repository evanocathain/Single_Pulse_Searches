#!/usr/bin/python

import numpy as np
from numpy.random import normal
import math as m
import matplotlib.pylab as plt
import sys
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-option', type=int, dest='option', help='choose kind of pulse (1=square, 2=Gaussian, equal area+equal FWHM, 3=Gaussian, equal area+equal height (default: 1)', default=1)
parser.add_argument('-height', type=float, dest='height', help='set the pulse height in units of sigma (default: 10.0)', default=10.0)
parser.add_argument('-width', type=float, dest='width', help='set pulse duration, i.e. width, in units of time samples (default: 16.0)', default=16.0)
parser.add_argument('-nsamps', type=int, dest='nsamps', help='set number of samples in output time series (default: 8192)', default=8192)
parser.add_argument('-period', type=int, dest='period', help='set period in units of time samples (default: 1000)', default=1000)
parser.add_argument('-seed', type=int, dest='seed', help='set random number generator seed explicitly (default: do not explicitly set)', default=0)
#parser.add_argument('--version', action='version', version='%(prog)s 0.0.3')
args = parser.parse_args()
option = args.option         # 1 - square pulses, 2 - Gaussian pulses, equal area + FWHM, 3 - Gaussian pulses, equal area + height
height = args.height
Nsamps = args.nsamps
period_bins = args.period
#dt = 0.001                        # in seconds, say
#Tobs = Nsamps*dt
#df = 1.0/Tobs
#period = period_bins*dt
#nperiods = int(Tobs/period)
nperiods = int(Nsamps/period_bins)

seed = args.seed
if (seed != 0):
    np.random.seed(seed)
noise = normal(0.0,1.0,Nsamps)
A = 1.0
#width = period*0.016               # Set the W/P
#width_bins = int(width/dt)
width_bins = int(args.width)
#sigma_bins = sigma/dt
offset_bins = period_bins*0.5 + 0.5

fac = m.sqrt(np.pi/np.log(2.0))*0.5 # = 1.0644670194 ... this ensures area under pulse is the same boxcar vs Gaussian Option2

prof = np.zeros(period_bins)
if (option == 1):
    outf = open("out1.ascii", "w")
    prof = np.hstack((np.zeros(period_bins-width_bins),np.ones(width_bins)))
if (option == 2):
    outf = open("out2.ascii", "w")
    sigma_bins = width_bins/(m.sqrt(8.0*m.log(2.0)))    
    for i in range(0,period_bins):
#        prof[i] = (A/fac)*m.exp(-(i - offset_bins)**2/(2*sigma_bins**2)) 
        prof[i] = (A/fac)*m.exp(-(i - offset_bins)**2/(2*sigma_bins**2)) 
if (option == 3):
    outf = open("out3.ascii", "w")
    sigma_bins = (A/fac)*width_bins/(m.sqrt(8.0*m.log(2.0)))    
    for i in range(0,period_bins):
        prof[i] = A*m.exp(-(i - offset_bins)**2/(2*sigma_bins**2)) 

print "Pulse Area: ",sum(prof)
pulsar = np.hstack(prof for i in range(nperiods))
time_series = height*pulsar + noise[0:pulsar.size]
print height*pulsar[490:510]
#print time_series[490:510]
#plt.plot(time_series)
#plt.show()

for i in range(0,pulsar.size):
#    print time_series[i]
    print >>outf, time_series[i]
