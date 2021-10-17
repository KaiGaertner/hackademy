
def take_picture(ID='test'):
	from picamera import PiCamera
	if DARKMODE:
		lightswitch(True)
	camera = PiCamera()
	camera.capture(pics_path+ID+".png")
	if DARKMODE:
			lightswitch(False)
	camera.close()
	print("Taken picture.")



def lightswitch(trigger=False):
	from time import sleep             # lets us have a delay  
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

# pytesseract
# https://pypi.org/project/pytesseract/
def ocr_scan(picture='test'):
	try:
		from PIL import Image
		from pytesseract import image_to_string
	except ImportError:
		import Image
	text = image_to_string(Image.open(pics_path+picture+'.png'))
	text = bytes(text, 'utf-8').decode('utf-8', 'ignore')
	text.replace("'''","'")
	text.replace('"',"'")
	return text

# write text to file for further scenarios
def write_textfile(name='text_test', text=''):
	with open(texts_path+name+'.txt', 'w') as outfile:
		outfile.write(text)


def tts_create(ID,text=''):
	sounds = []
	# split text into chunks and create sound files
	block_list = text.split("\n\n") 
	for idx, block in enumerate(block_list):
		if len(block) > 5:
			os.system('''pico2wave -l de-DE -w {}{}_{}.wav "{}"'''.format(sounds_path, ID, f'{idx:03d}', block))
			sounds.append(sounds_path+ID+'_'+f'{idx:03d}'+'.wav')
			print("["+f'{idx:03d}'+".wav] "+block)
			print('---')
	return sounds


import os, datetime						# import os library
import RPi.GPIO as GPIO				# import RPi.GPIO module  

# folders definition
pics_path = 'pics/'
sounds_path = 'sounds/'
texts_path = 'texts/'


### use relais to light up or not
DARKMODE = False
#DARKMODE = True


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
	#mixer.music.stop()
	print('right button pressed')

def on_middle_button_pressed():
	#if mixer.music.get_busy():
	#	mixer.music.pause()
	#else: 
	#	mixer.music.unpause()
	print('middle button pressed')

def on_left_button_pressed():
	mixer.music.rewind()
	print('left button pressed')


def readingbox():
	ID = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")

	take_picture(ID)

	text = ocr_scan(ID)
	write_textfile(ID, text)

	sound_files = tts_create(ID,text)
	print(sound_files)
	
	# play files
	mixer.init()
	INDEX = 0
	try:
		PAUSE = False
		while INDEX < len(sound_files):
		#for idx, soundfile in enumerate(sound_files):
			soundfile = sound_files[INDEX]
			try:
				mixer.music.load(soundfile)
			except error:
				sound_files.remove(soundfile)
				continue
			INDEX +=1
			mixer.music.play()
			while mixer.music.get_busy() or PAUSE:
				if GPIO.event_detected(RIGHT):
					mixer.music.stop()
				if GPIO.event_detected(LEFT):
					mixer.music.stop()
					INDEX = INDEX-2
					if INDEX < 0:
						INDEX = 0
				if GPIO.event_detected(MIDDLE):
					if not PAUSE:
						mixer.music.pause()
						PAUSE = True
					else:
						mixer.music.unpause()
						PAUSE = False
						INDEX -=1
						break
				time.delay(100)
				
	except KeyboardInterrupt:  
		mixer.music.stop()
	except IndexError:
		print("Listenproblem")




# play sound with pygame
from pygame import mixer, time, error

import RPi.GPIO as GPIO

if __name__ == '__main__':
	while True:
		if GPIO.event_detected(MIDDLE):
			readingbox()
		time.delay(100)
	GPIO.cleanup() 
	
