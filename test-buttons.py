#!/usr/bin/python3
import RPi.GPIO as GPIO


RIGHT = 11
LEFT = 15
MIDDLE = 13

GPIO.setmode(GPIO.BOARD)

GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MIDDLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def left_button_pressed(param):
    print(param)
    print("Left Button")


def middle_button_pressed(param):
    print(param)
    print("Middle Button")


h = 'This is a test'
GPIO.add_event_detect(LEFT, GPIO.FALLING, callback=lambda x: left_button_pressed(h), bouncetime=300)
GPIO.add_event_detect(MIDDLE, GPIO.FALLING, callback=lambda x: middle_button_pressed(b), bouncetime=300)

b = 'empty'
try:
    print("Waiting for rising edge on port %d" % (RIGHT))
    GPIO.wait_for_edge(RIGHT, GPIO.FALLING)
    print("Rising edge detected on port %d. Here ends the third lesson." % (RIGHT))
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
