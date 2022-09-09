README.md

This code runs the DMT extended state machine
Hardware consists of Rpi connected to a Evolv DNA200 board 
which fires up the RDTA inside the face mask.
The firing is controlled by the program and takes input 
from two barometric sensors inside the face mask to make sure
that the vaporization is only triggered during inhalations.


Files and their description:
dmtx.py - This is the launch script for all the other scripts. 
          It includes a simple text manu with options
          
readFactoryData.py - scripts reads the hard coded factory calibation
                    numbers from both sansors and saves the data
                    in two separate files. sensorExt.json and 
                    sensorInt.json

sensorExt.json, sensorInt.json - two data files that contain the
                    hardcoded calibration numbers for both sensors

calibrateSensors.py - This script is called from the main menu
                      It reads the two (sensorExt.json and 
                    sensorInt.json) files into memory and reads 
                    spicified amount of values of pressure from both
                    sensors to determine their avarage difference and
                    saves this number into sensorsCalibrationData.json

sensorsCalibrationData.json - contains a single number which is the 
                            avarage difference of the two sensors

beeper.py - script which runs the 3 short beeps with the buzzer

config.json - this file contains the configuration for the experience 
              the configuration settings can be changed from the main 
              manu by choosing the g option. Options and descriptopns
            Firing_time - Number of seconds that the code will wait to
                          detect an inhalation during automated mode
            TimeBetweenFirings - Number of seconds that the code will sleep
                              between each automated burns
            Temperature - Temperature of the coils during firings in (F)
            Power - Power in watts for automated burns. Poer for the initial
                    burn should be less because the lenghts of it is higher.
            InitialWarmup - Time in seconds that the code will wait bafore the 
                            starting the first burn. (be mindfull)
            NumberOfFirings - the total nomber of automated burns that the 
                            determines the length of the whole experience
            

             
