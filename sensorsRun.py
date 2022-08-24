#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 19:28:43 2022

@author: pi
"""
#import smbus
import time,json
import sensorDef
import RPi.GPIO as GPIO

    
def run(cycles):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    SensorInt = 0x77
    SensorExt = 0X76
    with open("sensorsCalibrated.json", "rb") as f:
        diffOfAvg = json.load(f)
    InternalCalib = sensorDef.readCalib("sensorInt.json")
    ExternalCalib = sensorDef.readCalib("sensorExt.json")
    
    
    GPIO.output(14, True)
    time.sleep(1)
    for i in range(cycles):
        In = sensorDef.readSensor(SensorInt,InternalCalib)
        Ext = sensorDef.readSensor(SensorExt,ExternalCalib)
    
        if (In-diffOfAvg) < Ext:
            print (str(round((In-diffOfAvg-Ext),2)) + ' * * in')
        else:
            print (str(round((In-diffOfAvg-Ext),2)) + ' * * out')
    GPIO.output(14, False)
    GPIO.cleanup()





    