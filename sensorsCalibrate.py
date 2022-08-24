#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 21:35:22 2022

@author: pi
"""

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


def Calibrate(samples):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    SensorInt = 0x77
    SensorExt = 0X76
    GPIO.output(14, True)
    time.sleep(1)
       
    global InternalCalib
    InternalCalib = sensorDef.readCalib("sensorInt.json")
    global ExternalCalib
    ExternalCalib = sensorDef.readCalib("sensorExt.json")
    InternalSensor = []
    ExternalSensor = []

    for i in range(samples):
        InternalSensor.append(round(sensorDef.readSensor(SensorInt,InternalCalib),3))
        time.sleep(0.2)
        ExternalSensor.append(round(sensorDef.readSensor(SensorExt,ExternalCalib),3))
        time.sleep(0.2)

    avgInt = sum(InternalSensor)/len(InternalSensor)
    maxDevInt = round(max(InternalSensor)-avgInt,2)
    minDevInt = round(min(InternalSensor)-avgInt,2)

    avgExt = sum(ExternalSensor)/len(ExternalSensor)
    maxDevExt = round(max(ExternalSensor)-avgExt,2)
    minDevExt = round(min(ExternalSensor)-avgExt,2)

    global diffOfAvg
    diffOfAvg = abs(round(avgInt-avgExt,4))
    print ("Internal Avarage "+str(avgInt)+" Max V:"+str(maxDevInt)+" MinV:"+str(minDevInt))
    print ("External Avarage " + str(avgExt) + " Max V " +str(maxDevExt)+" MinV:"+str(minDevExt))
    print ('Difference of avarages :'+ str(diffOfAvg))
    with open("sensorsCalibrated.json", "w") as f:
        json.dump(diffOfAvg,f)
    GPIO.output(14, False)    
    GPIO.cleanup()




    