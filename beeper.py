#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 18:32:52 2022

@author: pi
"""

##beeper
import RPi.GPIO as GPIO
import time

def beep(o,x): #o time beeper is ON , x - time beeper is Off
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)
    GPIO.output(24, True)
    time.sleep(o)
    GPIO.output(24, False)
    time.sleep(x)
    GPIO.cleanup()

def beep3(on): #m-mute 
    if on=="on":
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(24, GPIO.OUT)
        for i in range(3):
            print (3-i)
            GPIO.output(24, True)
            time.sleep(0.1)
            GPIO.output(24, False)
            time.sleep(0.9)
        GPIO.cleanup()
    else:
        for i in range(3):
            print (3-i)
            time.sleep(1)


