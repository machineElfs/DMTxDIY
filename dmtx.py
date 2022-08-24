#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 21:44:22 2022

@author: pi
"""

##Main program
import readFactoryData as RFD
import sensorsCalibrate as sCal
import sensorsRun, atom
import time,json

b = True

def menu():
    print (" - - - DMTxDIY - - -")
    print ("f -read factory sensor data into file")
    print ("c -calibrate sensors !!! PLACE MASK ON THE TABLE !!!")
    print ("s - show settings for The Experience")
    print ("g - change settings for The Experience")
    print ("b - beeper is "+ str(b)+" for 3-2-1 countdown before each firing")
    print("")
    print ("r - Run !!!")
    print ("to exit press Ctrl+c")
    print ("")




while True:
    menu()
    value = raw_input("option: ")
    
    if value == "b":
        b = not b
    if value == "f":
        print (" Reading factory data - - - - ")
        with open("sensorInt.json", "w") as f:
            json.dump(RFD.readFactoryData(0x77),f)
        with open("sensorExt.json", "w") as f:
            json.dump(RFD.readFactoryData(0x76),f)
        print("Factory data saved !")
    if value == "c":
        print (" MASK MUST BE PLACED ON THE TABLE ! ! !")
        print (" Reading calibration data - - - -")
        sCal.Calibrate(20)
        print ("Calibration data saved !")
    if value =="s":
        print ("Current Experience settings: ")
        atom.showSet()
    if value == "g":
        atom.Help()
        atom.rewriteSet()
    if value == "r":
        print("running")  
        sensorsRun.run(20)
        exit()
        