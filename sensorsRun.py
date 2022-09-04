#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 18:32:52 2022

@author: Elf Machine
"""

import time,json,smbus,serial
import RPi.GPIO as GPIO
bus = smbus.SMBus(1)

   
def readCalib(sensor):
    with open(sensor, "rb") as f:
        calibData=json.load(f)
    return calibData


def readSensor(busN,calibData): #BusN is the sensor address
        
    #bus.write_byte(busN, 0x1E) #reset sensor
    #time.sleep(0.01)
    # MS5611_01BXXX address, 0x77(118)
    # 0x40(64) Pressure conversion(OSR = 256) command
    time.sleep(0.01)
    bus.write_byte(busN, 0x42)
    time.sleep(0.01)
    # Read digital pressure value
    # Read data back from 0x00(0), 3 bytes
    # D1 MSB2, D1 MSB1, D1 LSB
    value = bus.read_i2c_block_data(busN, 0x00, 3)
    D1 = value[0] * 65536 + value[1] * 256 + value[2]
    # MS5611_01BXXX address, 0x76(118)
    # 0x50(64) Temperature conversion(OSR = 256) command
    time.sleep(0.01)
    bus.write_byte(busN, 0x52)
    time.sleep(0.01)
    # Read digital temperature value
    # Read data back from 0x00(0), 3 bytes
    # D2 MSB2, D2 MSB1, D2 LSB
    value = bus.read_i2c_block_data(busN, 0x00, 3)
    
    D2 = value[0] * 65536 + value[1] * 256 + value[2]
    dT = D2 - calibData[4] * 256
    OFF =  calibData[1]* 65536 + ((calibData[3]) * dT) / 128
    SENS = calibData[0] * 32768 + (calibData[2] * dT ) / 256
    pressure = ((((D1 * SENS) / 2097152) - OFF) / 32768.0) / 10 - 10100
    return pressure


def maskTest(cycles):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.output(14, True)
    GPIO.output(24, False)
    SensorInt = 0x77
    SensorExt = 0X76
    with open("sensorsCalibrationData.json", "rb") as f:
        diffOfAvg = json.load(f)
    InternalCalib = readCalib("sensorInt.json")
    ExternalCalib = readCalib("sensorExt.json")
    time.sleep(0.02)
    bus.write_byte(SensorInt, 0x1E) #reset sensor
    time.sleep(0.01)
    bus.write_byte(SensorExt, 0x1E) #reset sensor
    time.sleep(0.01)
    l=[0,0,0,0,0]
    m=[0,0,0]
    x=0
    y=0
    GPIO.output(24, False)
    for i in range(cycles):
        
        In = readSensor(SensorInt,InternalCalib)
        Ext = readSensor(SensorExt,ExternalCalib)
        if ( In - diffOfAvg*0.87) < (Ext):##pressure drop
            x = 1
        else: ## pressure rise
            x = 0 
        l.append(x)
        l.pop(0)
        #print(l)
        one = 0
        two = 0
        
        for j in range(3):
            one = one + l[(len(l)-1-j)]
        for j in range(len(l)):
            two = two + l[(len(l)-1-j)]
 
        if one == 3 or two == 4:
            #print("inhale")
            y=1
        else:
            y=0
         #   GPIO.output(24, False)
        
        m.append(y)
        m.pop(0)
        #print (m)
            #print ("inhale")
        one = 0
        two = 0
        #print m
        
        for k in range(len(m)):
            
            one = one + m[k]

        if one == 3 :
            GPIO.output(24, True)
            print ("inhale")
        else:
            print ""
            GPIO.output(24, False)
           
    GPIO.output(14, False)
    GPIO.cleanup()

def autoBurn(t):
    print ("CoilOn")
    ser = serial.Serial('/dev/ttyACM0',baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=0, rtscts=False, dsrdtr=False)
    cmd=("F="+str(t)+" S\r")
    ser.write(cmd.encode())

def run(cycles):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    GPIO.output(14, True)
    SensorInt = 0x77
    SensorExt = 0X76
    with open("sensorsCalibrationData.json", "rb") as f:
        diffOfAvg = json.load(f)
    InternalCalib = readCalib("sensorInt.json")
    ExternalCalib = readCalib("sensorExt.json")
    time.sleep(0.02)
    bus.write_byte(SensorInt, 0x1E) #reset sensor
    time.sleep(0.01)
    bus.write_byte(SensorExt, 0x1E) #reset sensor
    time.sleep(0.01)
    l=[0,0,0,0,0]
    m=[0,0,0]
    x=0
    y=0
    
    for i in range(cycles):
        
        In = readSensor(SensorInt,InternalCalib)
        Ext = readSensor(SensorExt,ExternalCalib)
        if ( In - diffOfAvg*0.87) < (Ext):##pressure drop
            x = 1
        else: ## pressure rise
            x = 0 
        l.append(x)
        l.pop(0)
        one = 0
        two = 0
        for j in range(3):
            one = one + l[(len(l)-1-j)]
        for j in range(len(l)):
            two = two + l[(len(l)-1-j)]
        if one == 3 or two == 4:
            y=1
        else:
            y=0
        m.append(y)
        m.pop(0)
        one = 0
        two = 0

        for k in range(len(m)):
            one = one + m[k]

        if i > 30 :
            if one == 3:
                autoBurn(0.4)
            
                ## add counter of consequitive burns here !!!
    
    GPIO.output(14, False)
    GPIO.cleanup()






    