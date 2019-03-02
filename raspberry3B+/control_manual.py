from blinzel import Blinzler
import time, os, subprocess
import RPi.GPIO as GPIO

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(11, GPIO.IN) # Escape
#GPIO.setup(12, GPIO.IN) # Play
#GPIO.setwarnings(False)
blinzler = Blinzler()
#read = True
# say hello to user
subprocess.call(['aplay', 'sounds/hello.wav'])
#while True:
#	if GPIO.input(12)==GPIO.HIGH:
		#blinzler.make_ocr("test_image.jpg")
		#blinzler.read_ocr('test2.txt')
blinzler.take_picture(brightness=60, contrast=60)
blinzler.make_ocr()
blinzler.read_ocr()
blinzler.speak_text()		
		#print blinzler.speak_runtest()
		#time.sleep(2)
		#blinzler.stop_reading()
		#print "STOP reading"
		#time.sleep(2)
		#blinzler.continue_reading()
print "Lesen beendet"
	
		#print "runtest: " + str(blinzler.speak_runtest())
		#if not blinzler.speak_runtest():
		#	continue
#	time.sleep(0.5)
