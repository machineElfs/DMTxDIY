#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 18:32:52 2022

@author: Elf Machine
"""

##Main program
import readFactoryData as RFD
import calibrateSensors as calS
import sensorsRun, atom
import time,json

b = True

def menu():
    print ("")
    print ("                    - - - DMTxDIY - - -")
    print ("f - read factory sensor data into file")
    print ("c - calibrate sensors !!! PLACE MASK ON THE TABLE !!!")
    print ("s - show settings for The Experience")
    print ("g - change settings for The Experience")
    print ("b - beeper is "+ str(b)+" for 3-2-1 countdown before each firing")
    print ("h - help with settings")
    print ("")
    print ("m - Test the masks function (mask must be on the face) ")
    print ("r - Run !!!")
    print ("t - Test Run ! no actual burns! buzzer will beep!")
    print ("to exit press Ctrl+c")
    print ("")

while True:
    menu()
    value = raw_input("option: ")
    if value == "h":
        atom.Help()
    if value == "b":
        b = not b
    if value =="m":
        print ("Testing mask sensors. Put mask on the face and breathe calmly")
        print ("Test will start in")
        for i in range(10):
            print 10-i
            time.sleep(1)
        sensorsRun.maskTest(300)
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
        calS.calibrate(20)
        print ("Calibration data saved !")
    if value =="s":
        print ("")
        print ("Current Experience settings: ")
        print ("")
        atom.showSet()
    if value == "g":
        atom.Help()
        atom.rewriteSet()
    if value == "r":
        print("running")  
        atom.main(b)
        exit()
    if value == "t":
        print ("Test Run initiated")
        atom.testRun("on","on") ## test=on buzzer=on