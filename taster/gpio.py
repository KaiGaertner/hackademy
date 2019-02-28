import time
import RPi.GPIO as GPIO

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Pin 40 (21) auf Input setzen
GPIO.setup(40, GPIO.IN)
#GPIO.setup(12, GPIO.IN)


# Dauersschleife
while 1:
 
  # GPIO lesen
  if GPIO.input(40)==GPIO.LOW:
    print "PRESSED"
    time.sleep(0.5)
#  elif GPIO.input(12)==GPIO.HIGH:
#    print "PLAY"
#    time.sleep(0.5)

