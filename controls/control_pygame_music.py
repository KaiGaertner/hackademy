
INDEX = 0
sound_files = ['../sounds/temp4.wav','../sounds/temp7.wav','../sounds/temp12.wav']

### GPIO callbacks
import RPi.GPIO as GPIO
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
	mixer.music.stop()
	print('right button pressed')

def on_middle_button_pressed():
	print('middle button pressed')
	

def on_left_button_pressed():
	print('left button pressed')

def play_files(start_index):
	try:
		PAUSE = False
		for idx, soundfile in enumerate(sound_files, start=start_index):
			INDEX = idx
			mixer.music.load(soundfile)
			mixer.music.play()
			while mixer.music.get_busy() or PAUSE:
				if GPIO.event_detected(MIDDLE):
					if not PAUSE:
						mixer.music.pause()
						PAUSE = True
					else:
						mixer.music.unpause()
						PAUSE = False						
				time.delay(100)
	except KeyboardInterrupt:  
		mixer.music.stop()



# play sound with pygame
from pygame import mixer, time, error

if __name__ == '__main__':
	mixer.init()
	play_files(INDEX)
