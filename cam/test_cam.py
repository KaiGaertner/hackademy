import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
from picamera import PiCamera
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(26, GPIO.OUT)           # set GPIO24 as an output   
 
try:
	print('Turn on light')
	GPIO.output(26, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
	sleep(.2)			# wait for relais
	camera = PiCamera()
	camera.resolution = (1024, 768)
	camera.start_preview()
	# Camera warm-up time
	sleep(2)
	camera.capture('test.jpg')
	sleep(2)                 # wait 2 seconds
	GPIO.cleanup()                 # resets all GPIO ports used by this program 
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
	GPIO.cleanup()                 # resets all GPIO ports used by this program 
