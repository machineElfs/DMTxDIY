#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 18:32:52 2022

@author: pi
"""

##beeper
import RPi.GPIO as GPIO
import time

def beep(o,x):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)
    GPIO.output(24, True)
    time.sleep(o)
    GPIO.output(24, False)
    time.sleep(x)
    GPIO.cleanup()
