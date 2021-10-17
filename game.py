import os, datetime						# import os library
import RPi.GPIO as GPIO				# import RPi.GPIO module
import pygame

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

def tts_create(ID,text=''):
	sounds = []
	# split text into chunks and create sound files
	block_list = text.split("\n\n")
	for idx, block in enumerate(block_list):
		current_block = block.trim()
		if len(current_block) > 5: # current_block contains words
			os.system('''pico2wave -l de-DE -w {}{}_{}.wav "{}"'''.format(sounds_path, ID, f'{idx:03d}', current_block))
            soundfile = sounds_path+ID+'_'+f'{idx:03d}'+'.wav'
            try: # check soundfile and add if not error prone
				pygame.mixer.music.load(soundfile)
                sounds.append(soundfile)
                pygame.mixer.music.unload()
                print("["+f'{idx:03d}'+".wav] " + current_block) # for debugging purposes
                print('---') # for debugging purposes
			except pygame.error:
				continue
	return sounds


clock = pygame.time.Clock()
pygame.display.set_mode((1,1), pygame.NOFRAME)

def on_right_button_pressed():
    if(mixer.music.get_busy()):
        pygame.event.post(pygame.event.Event(NEXT_TRACK))

def on_middle_button_pressed():
    if(mixer.music.get_busy()):
        pygame.event.post(pygame.event.Event(PAUSE_TRACK))
    else:
        pygame.event.post(pygame.event.Event(START_READING))

def on_left_button_pressed():
	if(pygame.mixer.music.get_busy()):
        pygame.event.post(pygame.event.Event(PREVIOUS_TRACK))

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

def start_reading():
    ID = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")

	take_picture(ID)

	text = ocr_scan(ID)
	write_textfile(ID, text) # for debugging purposes

	sound_files = tts_create(ID,text)
	print(sound_files) # for debugging purposes

    pygame.event.post(pygame.event.Event(OCR_DONE, list=sound_files))


FPS = 20
pygame.mixer.init()
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == START_READING:
            start_reading()
            break
        if event.type == OCR_DONE:
            global sound_files = event.list
            global current_sound_file_index = 0
            pygame.event.post(pygame.event.Event(START_PLAYING))
            break
        if event.type == START_PLAYING:
            if(current_sound_file_index >= len(sound_files)):
                pygame.event.post(pygame.event.Event(END_OF_QUEUE_REACHED)))
                break
            pygame.mixer.music.load(sound_files[current_sound_file_index])
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(NEXT_TRACK)
            break
        if event.type == NEXT_TRACK:
            current_sound_file_index += 1
            pygame.event.post(pygame.event.Event(START_PLAYING))
            print('Skip current track')
            break
        if event.type == PREVIOUS_TRACK:
            current_sound_file_index -= 1
            pygame.event.post(pygame.event.Event(START_PLAYING))
            print('Last track please')
            break
        if event.type == RESUME_TRACK:
            pygame.event.set_allowed(None) # Means all events are allowed...
            if(pygame.mixer.music.get_busy() == False):
                pygame.mixer.music.unpause()
            print('Resume playing')
            break
        if event.type == PAUSE_TRACK:
            pygame.event.set_allowed(RESUME_TRACK)
            if(pygame.mixer.music.get_busy()):
                pygame.mixer.music.pause()
            print('Pause reading')
            break
        if event.type == END_OF_QUEUE_REACHED:

            break
        if event.type == pygame.QUIT: # no idea how to trigger this, yet!
            pygame.quit()
            sys.exit()
    pygame.event.clear()
