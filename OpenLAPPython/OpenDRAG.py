## OpenLAP Laptime Simulation Project
#
# OpenDRAG
#
# Straight line acceleration and braking simulation using a simple point
# mass model for a racing vehicle.
# Instructions:
# 1) Select a vehicle file created by OpenVEHICLE by assigning the full
#    path to the variable "vehiclefile".
# 2) Run the script.
# 3) The results will appear on the command window and inside the folder
#    "OpenDRAG Sims". You can choose to include the date and time of each
#    simulation in the result file name by changing the
#    "use_date_time_in_name" variable to true.
#
# More information can be found in the "OpenLAP Laptime Simulator"
# videos on YouTube.
#
# This software is licensed under the GPL V3 Open Source License.
#
# Open Source MATLAB project created by:
#
# Michael Chalkiopoulos
# Cranfield University Advanced Motorsport MSc Engineer
# National Technical University of Athens MEng Mechanical Engineer
#
# LinkedIn: https://www.linkedin.com/in/michael-chalkiopoulos/
# email: halkiopoulos_michalis@hotmail.com
# MATLAB file exchange: https://uk.mathworks.com/matlabcentral/fileexchange/
# GitHub: https://github.com/mc12027
#
# April 2020.
# 
# Converted to Python by Ben Simpson
# University of Warwick Mechanical BEng Engineer
# Mercedes AMG HPP
#
# LinkedIn: 
# email: bensimpsonwarwick@gmail.com
# GitHub: https://gitbub.com/B3NJ4M1N0
#
# April 2022.
#

import time
import math
import os
from datetime import datetime

import numpy as np
import pandas as pd

## Timer start

# total timer start
totalTimer = time.time()

## Loading vehicle

# filename
vehicleFile = ''

## Simulation settings

# date and time in simulation name
BUseDateTimeInName = False
# time step
dt = 1e-3
# maximum simulation time for memory preallocation
tMax = 60
# acceleration sensitivity for drag limitation
axSens = 0.05 #[m/s2]
# speed traps
speedTrap = np.array([50,100,150,200,250,300,350]) / 3.6

# track data
bank = 0
incl = 0

## Vehicle data pre processing

#loading file
veh = 
# mass
M = veh[M]
# gravity constant
g = 9.81
#longitudinal tyre coefficients
dmx = veh[factorGrip] * veh[sens_x]
mux = veh[factorGrip] * veh[mu_x]
Nx = veh[mu_x_M] * g
# normal load on all wheels
Wz = M*g*np.cos(np.deg2rad(bank))*np.cos(np.deg2rad(incl))
# induced weight from banking and inclination
Wy = M*g*np.sin(np.deg2rad(bank))
Wx = M*g*np.sin(np.deg2rad(incl))
# ratios
rFinal = veh[ratioFinal]
rGearbox = veh[ratioGearbox]
rPrimary = veh[ratioPrimary]
# tyre radius
Rt = veh[tyreRadius]
# drivetrain efficiency
nFinal = veh[nFinal]
nGearbox = veh[nGearbox]
nPrimary = veh[nPrimary]
# engine curves
rpmCurve = np.array([0,veh[enSpeedCurve]])
torqueCurve = veh[factorPower]*np.array([veh[enTorqueCurve][0], veh[enTorqueCurve]])
# shift points
shiftPoints = np.array(veh[shifting], veh[enSpeedCurve[-1]])

## Acceleration preprocessing

# memory preallocation
N = tMax/dt
T = np.ones(N)
X = np.ones(N)
V = np.ones(N)
A = np.ones(N)
RPM = np.ones(N)
TPS = np.ones(N)
BPS = np.ones(N)
GEAR = np.ones(N)
MODE = np.ones(N)
# initial time
t = 0
tStart = 0
# initial distance
x = 0
xStart = 0
# initial velocity
v = 0
# inital acceleration
a = 0
# initial gears
gear = 1
gearPrev = 1
# shifting condition
BShifting = False
# initial rpm
rpm = 0
# initial tps
tps = 0
# initial bps
bps = 0
# initial trap number
trapNumber = 1
# speed trap checking condition
BCheckSpeedTraps = True
# iteration number
i = 1

## HUD display

# folder
if os.path.isdir('OpenDRAGSims') == False:
    os.mkdir('OpenDRAGSims')
# diary
if BUseDateTimeInName:
    now = datetime.now()
    dateTime = now.strftime(%y_%m_%d_%H_%M_%S)
else:
    dateTime = ''
simName = 'OpenDRAG Sims/OpenDRAG_' + veh[name] + dateTime
os.remove(simname + '.log')
