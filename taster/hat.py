import time
import RPi.GPIO as GPIO

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN)

while 1:
 
  # GPIO lesen
  if GPIO.input(11) == GPIO.HIGH:
    # Taste gedrueckt
    print "HAT"
