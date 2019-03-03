#!/usr/bin/python3

from blinzel import Blinzler
import RPi.GPIO as GPIO

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN) # Escape
GPIO.setup(12, GPIO.IN) # Play
# GPIO.setwarnings(False)
blinzler = Blinzler()
read = True
# say hello to user
# subprocess.call(['aplay', 'sounds/hello.wav'])
blinzler.play_audio('sounds/hello.wav')
while True:
	GPIO.wait_for_edge(40, GPIO.FALLING)
	blinzler.take_picture()
	blinzler.make_ocr()
	blinzler.read_ocr()
	blinzler.speak_text()
	print("Lesen beendet")

