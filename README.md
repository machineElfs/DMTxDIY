README.md

This code runs the DMT extended state machine
Hardware consists of Rpi connected to a Evolv DNA200 board 
which fires up the RDTA inside the face mask.
The firing is controlled by the program and takes input 
from two barometric sensors inside the face mask to make sure
that the vaporization is only triggered during inhalations.

#### General description of a typical run ####
1. the RDTA/RTA is filled with PG/VG/Spice mixture

2. user calibrates the sensors with the mask on the table

3. after positioning the mask on the face user starts the experience 

4. nothing happens for the duration of initial warm up perriod

5. Three seconds before the innitial burn the buzzer will beep

6. user inhales vapor for the duration of the initial burn

7. the program will wait (time between firing) for next burn (automated)

8. Three seconds before the automated burn the pressure sensors start
detecting inhalations (user can choose to hear a 3 second beep)

9. to trigger the automated burn, succesful inhalation must be detected.
the code waits (atom.py line 139) seconds for inhalation detection.
IF inhalation is detected the code will burn the coils in 0.4 second
increments until the inhalation is not detected anymore

10. the automated loop will continue for (NumberOfFirings) times going
back to step 7.

11. code will go back to the main menu



#### Files and their description: ####

dmtx.py - This is the launch script for all the other scripts. 
          It includes a simple text menu with options
          
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

atom.py - script called to change the setting for the experience 
	which will be saved in config.json
	this script also contains all the subprocess events
	that will be triggered when the run option is chosen from
	the main menu

sensorsRun.py - This script contains multiple important processes. 
	The first is the maskTest process which gets called from the
	main menu to test the accurate detection of inhalaions. 
	The other scripts are called whenever the automated loop
	calls for checking inhalation and if detected calls the burn
	subprocess. This script also contains the manual adjustment
	for more precise inhalation detection (line 78 - for masktest 
	and line 152 - for automated runs). Here the multiplier 
	for diffOfAvg is set to 0.87 . 
	This number tells the code to ignore the small 
	pressure fluctuations and only consider larger pressure drops 
	inside the mask assembly for determining when the inhalatation 
	is happening.
	The lower this multiplier the higher the pressure drop has
	to be for it to be detected as a inhalation.




####  bellow is the deatailed description of config.json####
############################################################
config.json - this file contains the configuration for the experience. 
              the configuration settings can be changed from the main 
              menu by choosing the g option. 
            
Firing_time - Number of seconds that the code will wait to
              detect an inhalation during automated mode

TimeBetweenFirings - Number of seconds that the code will sleep
                     between each automated burns

Temperature - Temperature of the coils during firings in (F)

Power - Power in watts for automated burns. Poer for the initial
         burn should be less because the lenghts of it is higher.

InitialWarmup - Time in seconds that the code will wait bafore the 
                 starting the first burn. (be mindfull)

NumberOfFirings - the total number of automated burns that will 
		execute autamatically with pauses between them 

InitialBurn - Time in seconds for the first burn (this burn should be 
		ten seconds)

RegularBurn - Lenght in seconds of all of the automated burns once
		which trigger once inhale is detected
