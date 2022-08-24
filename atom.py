#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import serial,json

# Settings:
def Help():
    print ("1 Temperature - temperature for repeated firing(F) ")
    print ("2 Firing_time - length of time the coils are burning (Seconds)")
    print ("3 Power - power settings for firings (Watts)")
    print ("4 InitialWarmup  - time before the program starts running (Seconds)")
    print ("5 InitialFire - length of the first burn (Seconds)")
    print ("6 RegularFire - lenght of time for all following automated burns (Seconds)")
    print ("7 TimeBetweeenFirings - lenght of time between automated burns (Seconds)")
    print ("8 NumberOfFirings - hom many rounds of automated delivery burns are desired")
    print ("x - exit,      p - print settings")

def showSet():
    f = open('config.json','r')
    global settings
    settings=json.load(f)
    for k,v in settings.items():
        print (k,v)
    f.close()    

def writeConfig(c,v):
    settings[c] = int(v)
    f = open('config.json','w')
    json.dump(settings,f)
    f.close()
    return()
    
def rewriteSet():
    showSet()
    # write settings into file f
    value = raw_input(" Enter settings number to change or enter x to return to main menu:  ")
    if value == ("x"):
        return()
    if value == ("p"):
        showSet()
        Help()
    if value == ("1"):
        t = raw_input(" Enter Temperature in (F) range(90-300): ")
        if (int(t)<301) and (int(t)>89):
            c="Temperature"
            writeConfig(c,t)
        
    if value == "2":
        t = raw_input(" Enter Firing Time in (seconds) range(1-5): ")
        if (int(t)>0) and (int(t)<6):
            c = "Firing_time"
            writeConfig(c,t)
    if value == "3":
        t = raw_input(" Enter Power in (W) range(40-100): ")
        if (int(t)>39) and (int(t)<101):
            c= "Power"
            writeConfig(c,t)
    
    if value =="4":
        t = raw_input(" Enter Initial warmup in (s) range(5-60): ")
        if (int(t)>4) and (int(t)<61):
            c="InitialWarmup"
            writeConfig(c,t)
    if value =="5":
        t = raw_input(" Enter Initial burn lenght in (s) range(4-10): ")
        if (int(t)>3) and (int(t)<11):
            c="InitialFire"
            writeConfig(c,t)
    
    if value =="6":
        t = raw_input(" Enter Regular burn lenght in (s) range(1-10): ")
        if (int(t)>0) and (int(t)<11):
            c="RegularFire"
            writeConfig(c,t)

    if value =="7":
        t = raw_input(" Enter Time between burns in (s) range(10-240): ")
        if (int(t)>9) and (int(t)<241):
            c="TimeBetweenFirings"
            writeConfig(c,t)
            
    if value =="8":
        t = raw_input(" Number of total burns range(1-20): ")
        if (int(t)>0) and (int(t)<21):
            c="NumberOfFirings"
            writeConfig(c,t)

def fire():
    ser = serial.Serial('/dev/ttyACM0',baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=False, dsrdtr=False)

    #Send settings to DNA200
    cmd=("T="+str(settings["Temperature"])+" F\r")
    ser.write(cmd.encode())
    cmd=("P="+str(settings["Power"])+" W\r")
    ser.write(cmd.encode())
    ser.close()
    
    
