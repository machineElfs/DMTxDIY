#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 18:32:52 2022

@author: Elf Machine
"""
import smbus,json
import time
bus = smbus.SMBus(1)
import RPi.GPIO as GPIO

def readCalib(sensor):
    with open(sensor, "rb") as f:
        calibData=json.load(f)
    return calibData

def calibSensor(busN,calibData): #BusN is the sensor address
        
    bus.write_byte(busN, 0x1E) #reset sensor
    time.sleep(0.02)
    # MS5611_01BXXX address, 0x77(118)
    # 0x40(64) Pressure conversion(OSR = 256) command
    bus.write_byte(busN, 0x42)
    time.sleep(0.02)
    # Read digital pressure value
    # Read data back from 0x00(0), 3 bytes
    # D1 MSB2, D1 MSB1, D1 LSB
    value = bus.read_i2c_block_data(busN, 0x00, 3)
    D1 = value[0] * 65536 + value[1] * 256 + value[2]
    # MS5611_01BXXX address, 0x76(118)
    # 0x50(64) Temperature conversion(OSR = 256) command
    time.sleep(0.02)
    bus.write_byte(busN, 0x52)
    time.sleep(0.02)
    # Read digital temperature value
    # Read data back from 0x00(0), 3 bytes
    # D2 MSB2, D2 MSB1, D2 LSB
    value = bus.read_i2c_block_data(busN, 0x00, 3)
    time.sleep(0.02)
    D2 = value[0] * 65536 + value[1] * 256 + value[2]
    dT = D2 - calibData[4] * 256
    OFF =  calibData[1]* 65536 + ((calibData[3]) * dT) / 128
#    TEMP = 2000 + dT * calibData[5] / 8388608
    SENS = calibData[0] * 32768 + (calibData[2] * dT ) / 256
    pressure = ((((D1 * SENS) / 2097152) - OFF) / 32768.0) / 10.0 - 10100
    return pressure

def calibrate(samples):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    SensorInt = 0x77
    SensorExt = 0X76
    GPIO.output(14, True)
    time.sleep(0.2)
       
    global InternalCalib
    InternalCalib = readCalib("sensorInt.json")
    global ExternalCalib
    ExternalCalib = readCalib("sensorExt.json")
    InternalSensor = []
    ExternalSensor = []

    for i in range(samples):
        InternalSensor.append(round(calibSensor(SensorInt,InternalCalib),3))
        time.sleep(0.2)
        ExternalSensor.append(round(calibSensor(SensorExt,ExternalCalib),3))
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
    with open("sensorsCalibrationData.json", "w") as f:
        json.dump(diffOfAvg,f)
    GPIO.output(14, False)    
    GPIO.cleanup()
