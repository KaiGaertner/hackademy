import time
import RPi.GPIO as GPIO

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Pin 18 (GPIO 24) auf Input setzen
GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(12, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(16, GPIO.IN)

# Dauersschleife
while 1:

  # GPIO lesen
  if GPIO.input(7) == GPIO.HIGH:
    # Taste gedrueckt
    print "BRAUN"
    time.sleep(0.5)
  elif GPIO.input(11) == GPIO.HIGH:
    print "ORANGE"
    time.sleep(0.5)
  elif GPIO.input(12) == GPIO.HIGH:
    print "WEISS"
    time.sleep(0.5)
  elif GPIO.input(13) == GPIO.HIGH:
    print "GELB"
    time.sleep(0.5)
  elif GPIO.input(15) == GPIO.HIGH:
    print "GRUEN"
    time.sleep(0.5)
  elif GPIO.input(16) == GPIO.HIGH:
    print "BLAU"
    time.sleep(0.5)
