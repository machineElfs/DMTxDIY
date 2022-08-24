#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 20:26:09 2022

@author: pi
"""

import smbus,json
import time

bus = smbus.SMBus(1)

def readCalib(sensor):
    with open(sensor, "rb") as f:
        calibData=json.load(f)
    return calibData


def readSensor(busN,calibData): #BusN is the sensor address
        
    bus.write_byte(busN, 0x1E) #reset sensor
    time.sleep(0.05)
    # MS5611_01BXXX address, 0x77(118)
    # 0x40(64) Pressure conversion(OSR = 256) command
    bus.write_byte(busN, 0x42)
    time.sleep(0.05)
    # Read digital pressure value
    # Read data back from 0x00(0), 3 bytes
    # D1 MSB2, D1 MSB1, D1 LSB
    value = bus.read_i2c_block_data(busN, 0x00, 3)
    D1 = value[0] * 65536 + value[1] * 256 + value[2]
    # MS5611_01BXXX address, 0x76(118)
    # 0x50(64) Temperature conversion(OSR = 256) command
    time.sleep(0.05)
    bus.write_byte(busN, 0x52)
    time.sleep(0.05)
    # Read digital temperature value
    # Read data back from 0x00(0), 3 bytes
    # D2 MSB2, D2 MSB1, D2 LSB
    value = bus.read_i2c_block_data(busN, 0x00, 3)
    time.sleep(0.05)
    D2 = value[0] * 65536 + value[1] * 256 + value[2]
    dT = D2 - calibData[4] * 256
    OFF =  calibData[1]* 65536 + ((calibData[3]) * dT) / 128
    TEMP = 2000 + dT * calibData[5] / 8388608
    SENS = calibData[0] * 32768 + (calibData[2] * dT ) / 256
    T2 = 0
    OFF2 = 0
    SENS2 = 0
    if TEMP >= 2000 :
        T2 = 0
        OFF2 = 0
        SENS2 = 0
    elif TEMP < 2000 :
            T2 = (dT * dT) / 2147483648
            OFF2 = 5 * ((TEMP - 2000) * (TEMP - 2000)) / 2
            SENS2 = 5 * ((TEMP - 2000) * (TEMP - 2000)) / 4
            if TEMP < -1500 :
                OFF2 = OFF2 + 7 * ((TEMP + 1500) * (TEMP + 1500))
                SENS2 = SENS2 + 11 * ((TEMP + 1500) * (TEMP + 1500)) / 2
    TEMP = TEMP - T2
    OFF = OFF - OFF2
    SENS = SENS - SENS2
    pressure = ((((D1 * SENS) / 2097152) - OFF) / 32768.0) / 100.0 - 1000
    return pressure
#    print "Pressure : %.2f mbar" %pressure
#    print "Temperature in Celsius : %.2f C" %cTemp