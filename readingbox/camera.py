#from time import sleep             # lets us have a delay  
import RPi.GPIO as GPIO				# import RPi.GPIO module  
	
def lightswitch(trigger=False):
	GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
	GPIO.setup(26, GPIO.OUT)           # set GPIO26 as an output   
	try:
		if trigger:
			print('Turn on')
			GPIO.output(26, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
		else: 
			print('Turn off')
			GPIO.output(26, 1)         # set GPIO24 to 0/GPIO.LOW/False  
	except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
		GPIO.cleanup()                 # resets all GPIO ports used by this program  


from picamera import PiCamera
def take_picture(path='../pics/', name='test.png', flash=False):
	if  flash:
		lightswitch(True)
	camera = PiCamera()
	if not name.endswith('png') and not name.endswith('jpg'):
		name = name+'.png'
	camera.capture(path+name)
	if flash:
			lightswitch(False)
	camera.close()
	return path+name
