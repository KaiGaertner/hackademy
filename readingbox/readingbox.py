#! /usr/bin/python3
# using systemd as start service
# https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/

import datetime, os, pygame
import RPi.GPIO as GPIO                
# own modules
from ocr import ocr_scan, write_textfile
from camera import take_picture
from text2speech import tts_create



# folders definition
PICS_PATH = '/home/pi/hackademy/pics/'
SOUNDS_PATH = '/home/pi/hackademy/sounds/'
TEXTS_PATH = '/home/pi/hackademy/texts/'
COMMANDS_PATH = '/home/pi/hackademy/command_sounds/'

# use 'flash light' for pictures
# TODO: use light sensor to do this automatically
FLASH =False 

### GPIO callbacks
RIGHT = 22
LEFT = 23
MIDDLE = 24
GPIO.setmode(GPIO.BCM)

START_READING = pygame.USEREVENT + 0
PAUSE_TRACK = pygame.USEREVENT + 1
RESUME_TRACK = pygame.USEREVENT + 2
NEXT_TRACK = pygame.USEREVENT + 3
PREVIOUS_TRACK = pygame.USEREVENT + 4
OCR_DONE = pygame.USEREVENT + 5
START_PLAYING = pygame.USEREVENT + 6
END_OF_QUEUE_REACHED = pygame.USEREVENT + 7

GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(MIDDLE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(LEFT, GPIO.FALLING, callback=lambda x: on_left_button_pressed(), bouncetime=300)
GPIO.add_event_detect(MIDDLE, GPIO.FALLING, callback=lambda x: on_middle_button_pressed(), bouncetime=300)
GPIO.add_event_detect(RIGHT, GPIO.FALLING, callback=lambda x: on_right_button_pressed(), bouncetime=300)



if __name__ == '__main__':
	run_name = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
	
	picture_name = take_picture(PICS_PATH, run_name,FLASH)
	textblob = ocr_scan(picture_name)
	
	write_textfile(TEXTS_PATH, run_name, textblob)
	sound_files = tts_create(sounds_path,run_name,textblob)
	
