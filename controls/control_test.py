# play sound with pygame
from pygame import mixer, time, error
import pygame
import RPi.GPIO as GPIO



### GPIO callbacks
RIGHT = 22
LEFT = 23
MIDDLE = 24
GPIO.setmode(GPIO.BCM)

GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MIDDLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(LEFT, GPIO.FALLING, callback=lambda x: on_left_button_pressed(), bouncetime=300)
GPIO.add_event_detect(MIDDLE, GPIO.FALLING, callback=lambda x: on_middle_button_pressed(), bouncetime=300)
GPIO.add_event_detect(RIGHT, GPIO.FALLING, callback=lambda x: on_right_button_pressed(), bouncetime=300)	


def on_right_button_pressed():
	#current_sound.stop()
	mixer.music.stop()
	print('right button pressed')

def on_middle_button_pressed():
	PAUSE.toggle()
	print('middle button pressed')
	

def on_left_button_pressed():
	#mixer.music.rewind()
	print('left button pressed')

mixer.init()
class Pause(object):

    def __init__(self):
        self.paused = False

    def toggle(self):
        if self.paused:
            pygame.mixer.music.unpause()
        if not self.paused:
            pygame.mixer.music.pause()
        self.paused = not self.paused

PAUSE = Pause()

if __name__ == '__main__':
	sound_files = ['../sounds/temp4.wav','../sounds/temp7.wav','../sounds/temp12.wav']
	try:

		for soundfile in sound_files:
			try:
				pygame.mixer.music.load(soundfile)
				pygame.mixer.music.play()
				while mixer.music.get_busy():
					time.delay(100)
			except KeyboardInterrupt:  
				pygame.mixer.music.stop()
	except error:
		print(error)
	#except KeyboardInterrupt:  
	#	pygame.mixer.music.stop()
		
