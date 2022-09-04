#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 18:32:52 2022

@author: Elf Machine
"""

import smbus,time
import RPi.GPIO as GPIO

def readFactoryData(busN):
    GPIO.setmode(GPIO.BCM)
    bus = smbus.SMBus(1)
    GPIO.setup(14, GPIO.OUT)
    GPIO.output(14, True)
    time.sleep(1)
    bus.write_byte(busN, 0x1E) #reset sensor
    time.sleep(0.2)
    data = bus.read_i2c_block_data(busN, 0xA2, 2)
    C1 = data[0] * 256 + data[1]
    # Read pressure offset
    data = bus.read_i2c_block_data(busN, 0xA4, 2)
    C2 = data[0] * 256 + data[1]
    # Read temperature coefficient of pressure sensitivity
    data = bus.read_i2c_block_data(busN, 0xA6, 2)
    C3 = data[0] * 256 + data[1]
    # Read temperature coefficient of pressure offset
    data = bus.read_i2c_block_data(busN, 0xA8, 2)
    C4 = data[0] * 256 + data[1]
    # Read reference temperature
    data = bus.read_i2c_block_data(busN, 0xAA, 2)
    C5 = data[0] * 256 + data[1]
    # Read temperature coefficient of the temperature
    data = bus.read_i2c_block_data(busN, 0xAC, 2)
    C6 = data[0] * 256 + data[1]
    calibData = [C1,C2,C3,C4,C5,C6]
    GPIO.output(14, False)
    time.sleep(0.2)
    GPIO.cleanup()
    return calibData
