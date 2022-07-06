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
import sys
from datetime import datetime
from turtle import end_fill

import numpy as np
import h5py
import pandas as pd

def hud(v, a, rpm, gear, t, x, tStart, xStart):
    return f'{v*3.6}, {a/9.81}, {round(rpm)}, {gear}, {t}, {x}, {t-tStart}, {x-xStart}'

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
# vehicleFile = 'OpenVEHICLE Vehicles/OpenVEHICLE_Formula 1_Open Wheel.mat'
vehicleFile = '/Users/Ben/Documents/Coding/OpenLAP/OpenLAP-Lap-Time-Simulator/OpenVEHICLE Vehicles/OpenVEHICLE_Formula 1_Open Wheel.mat'
f = h5py.File(vehicleFile,'r')
data = f.get('data/variable1')
veh = np.array(data) # For converting to a NumPy array
# mass
M = veh[M]
# gravity constant
g = 9.81
#longitudinal tyre coefficients
dmx = veh['factorGrip'] * veh['sens_x']
mux = veh['factorGrip'] * veh['mu_x']
Nx = veh['mu_x_M'] * g
# normal load on all wheels
Wz = M*g*np.cos(np.deg2rad(bank))*np.cos(np.deg2rad(incl))
# induced weight from banking and inclination
Wy = M*g*np.sin(np.deg2rad(bank))
Wx = M*g*np.sin(np.deg2rad(incl))
# ratios
rFinal = veh['ratioFinal']
rGearbox = veh['ratioGearbox']
rPrimary = veh['ratioPrimary']
# tyre radius
Rt = veh['tyreRadius']
# drivetrain efficiency
nFinal = veh['nFinal']
nGearbox = veh['nGearbox']
nPrimary = veh['nPrimary']
# engine curves
rpmCurve = np.array([0,veh['enSpeedCurve']])
torqueCurve = veh['factorPower']*np.array([veh['enTorqueCurve'][0], veh['enTorqueCurve']])
# shift points
shiftPoints = np.array(veh['shifting'], veh['enSpeedCurve'[-1]])

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
trapNumber = 0
# speed trap checking condition
BCheckSpeedTraps = True
# iteration number
i = 0

## HUD display

# folder
if os.path.isdir('OpenDRAGSims') == False:
    os.mkdir('OpenDRAGSims')
# diary
if BUseDateTimeInName:
    now = datetime.now()
    dateTime = now.strftime('%y_%m_%d_%H_%M_%S')
else:
    dateTime = ''
simName = f'OpenDRAG Sims/OpenDRAG_ {veh["name"]} _ {dateTime}'
os.remove(simName + '.log')
# create a python logging file
stdout = sys.stdout
sys.stdout = open(f'{simName} .log', 'w')
# HUD
print("""
    '               _______                    ________________________________';...
    '               __  __ \______________________  __ \__  __ \__    |_  ____/';...
    '               _  / / /__  __ \  _ \_  __ \_  / / /_  /_/ /_  /| |  / __  ';...
    '               / /_/ /__  /_/ /  __/  / / /  /_/ /_  _, _/_  ___ / /_/ /  ';...
    '               \____/ _  .___/\___//_/ /_//_____/ /_/ |_| /_/  |_\____/   ';...
    '                      /_/                                                 '...
    """)
print('=======================================================================================')
print(f'Vehicle: {veh["name"]}')
print(f'Date: {now.strftime("dd/mm/yyyy")}')
print(f'Time: {now.strftime("HH:MM:SS")}')
print('=======================================================================================')
print(f'Acceleration simulation started:')
print(f'Initial Speed: {v*3.6} km/h')
print('|_______Comment________|_Speed_|_Accel_|_EnRPM_|_Gear__|_Tabs__|_Xabs__|_Trel__|_Xrel_|')
print('|______________________|[km/h]_|__[G]__|_[rpm]_|__[#]__|__[s]__|__[m]__|__[s]__|_[m]__|')

## Acceleration

# acceleration timer startsys.stdout.close()
while True:
    # saving values
    MODE[i] = 1
    T[i] = t
    X[i] = x
    V[i] = v
    A[i] = a
    RPM[i] = rpm
    TPS[i] = tps
    BPS[i] = 0
    GEAR[i] = gear

    # checking if rpm limiter is on or if out of memory
    if v >= veh['vMax']:
        # HUD
        print(f'Engine speed limited')
        hud(v, a, rpm, gear, t, x, tStart, xStart)
        break
    elif i==N:
        print(f'Did not reach maximum speed at time {t}s')
    # check if drag limited
    if tps == 1 & ax + axDrag <= axSens:
        # HUD
        print('Drag Limited')
        hud(v, a, rpm, gear, t, x, tStart, xStart)
        break
    # checking speed trap
    if BCheckSpeedTraps:
        # checking if current speed is above trap speed
        if v >= speedTrap(trapNumber):
            print(f'Speed Trap #{trapNumber}, {round(speedTrap(trapNumber) * 3.6)}, km/h')
            hud(v, a, rpm, gear, t, x, tStart, xStart)
            # next speed trap
            trapNumber += 1
            # checking if speed traps are completed
            if trapNumber > len(speedTrap):
                BCheckSpeedTraps = False
    # aero forces
    aeroDf = 1/2 * veh['rho'] * veh['factorCl'] * veh['Cl'] * veh['A'] * v^2
    aeroDr = 1/2 * veh['rho'] * veh['factorCd'] * veh['Cd'] * veh['A'] * v^2
    # rolling resistance
    rollDr = veh['Cr'] * (-aeroDf + Wz)
    # normal load on driven wheels
    Wd = (veh['factorDrive'] * Wz + (-veh['factorAero'] * aeroDf))/veh['drivenWheels']
    # drag acceleration
    axDrag = (aeroDr + rollDr + Wx)/M
    # rpm calculation
    if gear == 0: # shifting gears
        rpm = rf*rg[gearPrev - 1] * rp * v/Rt * 60 / 2 / np.pi()
        rpmShift = shiftPoints[gearPrev - 1]
    else: # gear change finished
        rpm = rf * rg[gear - 1] * rp * v/Rt * 60 / 2 / np.pi()
        rpmShift = shiftPoints[gear - 1]
    # checking for gearshifts
    if rpm >= rpmShift & ~BShifting: # need to change gears
        if gear == veh['nog']: # maximum gear number
            # HUD
            print('Engine speed limited')
            hud(v, a, rpm, gear, t, x, tStart, xStart)
            break
        else: # higher gear available
            # shifting condition
            BShifting = True
            # shift initialisation time
            tShift = t
            # zeroing engine acceleration
            ax = 0
            # saving previous gear
            gearPrev = gear
            # setting gear to neutral for duration of gearshift
            gear = 0
    elif BShifting: # currently shifting gears
        # zeroing engine acceleration
        ax = 0
        # checking if gearshift duration has passed
        if t-tShift > veh['shiftTime']:
            # HUD
            print(f'Shifting to gear {gearPrev + 1}')
            hud(v, a, rpm, gearPrev + 1, t, x, tStart, xStart)
            # shifting condition
            BShifting = False
            # next gear
            gear = gearPrev + 1
    else: # no gearshift
        # max long acc available from tyres
        axTyreMaxAcc = 1/M*(mux + dmx * (Nx - Wd)) * Wd * veh['drivenWheels']
        # getting power limit from engine
        engineTorque = np.interp1(rpmCurve, torqueCurve, rpm)
        wheelTorque = engineTorque * rf * rg[gear - 1]
        axPowerLimit = 1/M * wheelTorque / Rt
        # final long acc
        ax = min(axPowerLimit, axTyreMaxAcc)
    # tps