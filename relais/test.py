import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(26, GPIO.OUT)           # set GPIO24 as an output   
 
try:
	print('Turn on')
	GPIO.output(26, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
	sleep(2)                 # wait half a second  
	print('Turn off')
	GPIO.output(26, 1)         # set GPIO24 to 0/GPIO.LOW/False  
	sleep(5)                 # wait half a second  
	print('Finish')
	GPIO.cleanup()
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
	GPIO.cleanup()                 # resets all GPIO ports used by this program  
