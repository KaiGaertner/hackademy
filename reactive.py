#!/usr/bin/python3
import sys
import RPi.GPIO as GPIO
import time
import os
import wave
import pyaudio
# import cv2
import datetime
import picamera
import pytesseract
# import subprocess
from PIL import Image, ImageFilter

first_run = False
if len(sys.argv) > 1:
    first_run = sys.argv[1] == 'init'

RIGHT = 11
LEFT = 15
MIDDLE = 13

HOME_DIR = '/home/pi/hackademy/'
PICS_DIR = 'pictures/'

if not os.path.exists(HOME_DIR + PICS_DIR):
    os.mkdir(HOME_DIR + PICS_DIR)

GPIO.setmode(GPIO.BOARD)


GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MIDDLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def create_play(text, speed=0.93, language='de-DE'):
    '''transforms given text into a temporary wav file and plays it.
       text: words to be spoken
       speed: changes rate of sound [0-1]
       language: choose language see aplay -h'''

    os.system('''pico2wave -l {} -w {}temp.wav "{}"'''.format(language, HOME_DIR, text))
    sound = wave.open('''{}temp.wav'''.format(HOME_DIR))
    p = pyaudio.PyAudio()
    chunk_size = 1024
    stream = p.open(format=p.get_format_from_width(sound.getsampwidth()),
                channels=sound.getnchannels(),
                rate=int(sound.getframerate() * speed),
                output=True)
    data = sound.readframes(chunk_size)
    while data != b'':
        if data != '':
            stream.write(data)
            data = sound.readframes(chunk_size)


def take_picture(speed=150000, name=None, contrast=60, brightness=40):
    # A picture is being shot and saved. Path is returned
    path = HOME_DIR + PICS_DIR
    if name is None:
        now = datetime.datetime.now()
        path += "{}-{}-{}um{}:{}:{}.png".format(now.year, now.month, now.day,now.hour, now.minute, now.second)
    else:
        path += name + '.png'
    with picamera.PiCamera() as camera:
        print("Take picture")
        camera.resolution = (2592, 1944)
        now = datetime.datetime.now()
        camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) {} by Kai Gaertner'.format(now.year)
        camera.capture(path)
        # rotate picture for processing
        im = Image.open(path)
        rotated_image = im.rotate(angle=90, expand=True)
        monochrome_image = rotated_image.convert('L')
        # sharpened_image = black_and_white_image.filter(ImageFilter.SHARPEN)

        monochrome_image.save(path)
        im.close()
        return path


pictures = []


def on_left_button_pressed(pics):
    create_play(text='Bild wird aufgenommen')
    pics.append(take_picture())
    create_play(text='Für ein weiteres Bild den linken Knopf noch ein mal drücken.')


def on_middle_button_pressed(pics):
    if len(pics) < 1:
        create_play('Es liegen keine gespeicherten Dokumente vor.')
        return
    if len(pics) == 1:
        create_play('Bitte warten. Die Seite wird verarbeitet.')
    else:
        create_play(text='Bitte warten. Die Seiten werden verarbeitet. Das kann einige Minuten dauern.')
    print('Initiating Text extraction')
    complete_text = ''
    global pictures
    for picture_path in pics:
        start_time = time.time()
        text = pytesseract.image_to_string(Image.open(picture_path), lang='deu')
        time_span = time.time() - start_time
        complete_text += text
        print(text)
        print(time_span)
    pictures = []
    create_play(text=complete_text)
    # print("pressed middle button")



GPIO.add_event_detect(LEFT, GPIO.FALLING, callback=lambda x: on_left_button_pressed(pictures), bouncetime=300)
GPIO.add_event_detect(MIDDLE, GPIO.FALLING, callback=lambda x: on_middle_button_pressed(pictures), bouncetime=300)
try:
    print("Bereit")
    if first_run:
        create_play(text="Gerät ist bereit.")
    GPIO.wait_for_edge(RIGHT, GPIO.FALLING)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()

print("vielen dank")
