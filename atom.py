#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import serial,json,time
import beeper,sensorsRun


# Settings:
def Help():
    print ("1 Temperature - temperature for repeated firing(F) ")
    print ("2 Firing_time - length of time the coils are burning (Seconds)")
    print ("3 Power - power settings for firings (Watts)")
    print ("4 InitialWarmup  - time before the program starts running (Seconds)")
    print ("5 InitialBurn - length of the first burn (Seconds)")
    print ("6 RegularBurn - lenght of time for all following automated burns (Seconds)")
    print ("7 TimeBetweeenFirings - lenght of time between automated burns (Seconds)")
    print ("8 NumberOfFirings - hom many rounds of automated delivery burns are desired")
    print ("x - exit,      s - print settings")

def showSet():
    print ("- - - Current settings:  - - -")
    print ("")
    f = open('config.json','r')
    global settings
    settings=json.load(f)
    for k,v in settings.items():
        print (k,v)
    f.close()
    print ("- - - - - - - - - - - - - - -")
    ##send setting to DNA
    ser = serial.Serial('/dev/ttyACM0',baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=False, dsrdtr=False)
    #Send settings to DNA200
    cmd=("T="+str(settings["Temperature"])+" F\r")
    ser.write(cmd.encode())
    cmd=("P="+str(settings["Power"])+" W\r")
    ser.write(cmd.encode())
    ser.close()    

def writeConfig(c,v):
    settings[c] = int(v)
    f = open('config.json','w')
    json.dump(settings,f)
    f.close()
    showSet()
    
        
def rewriteSet():
    showSet()
    # write settings into file f
    value = raw_input(" Enter settings number to change or enter x to return to main menu:  ")
    if value == ("x"):
        return()
    if value == ("s"):
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
            c="InitialBurn"
            writeConfig(c,t)
    
    if value =="6":
        t = raw_input(" Enter Regular burn lenght in (s) range(1-10): ")
        if (int(t)>0) and (int(t)<11):
            c="RegularBurn"
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

def burn(test,length):
    if test=="on":
        print ("Test Burning")
        sensorsRun.maskTest(length)
        #beeper.beep(length,0)
    
    else:
        ser = serial.Serial('/dev/ttyACM0',baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=False, dsrdtr=False)
        cmd=("F="+str(length)+" S\r")
        ser.write(cmd.encode())
        print ("Burning")
        for i in range (length):
            print length-i
            time.sleep(1)

    
    
def fire(test,buzz): 
    showSet()    
    if test=="on":
        print ("Test run in progress")
    else:
        print ("Countdown for lift-off")
    for i in range ((settings["InitialWarmup"])-4):
        print (settings["InitialWarmup"] - i - 1)
        time.sleep(1)
        
    if test=="on":
        beeper.beep3("on")
        burn(test,settings["InitialBurn"])
    else:
        if buzz=="on":
            beeper.beep3("on")
        else:
            beeper.beep3("off")
        burn(test,settings["InitialBurn"])
    print ("automated burns staring now")
    
    for i in range (settings["NumberOfFirings"])   :
        for j in range ((settings["TimeBetweenFirings"])-4):
            print ((settings["TimeBetweenFirings"])-j -1)
            time.sleep(1)
        if buzz=="on":
            beeper.beep3("on")
        else:
            beeper.beep3("off")  
             
        print ("Automatic burn #"+str(i+1))
        burn(test,settings["RegularBurn"])
            
fire("on","on")
#fire("off","on")
                
        