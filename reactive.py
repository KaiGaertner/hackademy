#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import os
import wave
import pyaudio
import cv2
import datetime
import picamera
# import pytesseract
import subprocess
from PIL import Image, ImageFilter

RIGHT = 11
LEFT = 13
MIDDLE = 15

HOME_DIR = '/home/pi/reading_box/'
PICS_DIR = 'pictures/'

GPIO.setmode(GPIO.BOARD)


GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MIDDLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.add_event_detect(LEFT, GPIO.FALLING)
GPIO.add_event_detect(MIDDLE, GPIO.FALLING)
GPIO.add_event_detect(RIGHT, GPIO.FALLING)


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
        im.filter(ImageFilter.SHARPEN).rotate(270).save(path)
        im.close()
        return path


pictures = []
running = True
while running:
    if GPIO.event_detected(LEFT):
        time.sleep(0.2)
        create_play(text='Bild wird aufgenommen')
        pictures.append(take_picture())
        print(pictures)
        create_play(speed=0.93, text='Drücken Sie erneut den linken Knopf um ein weiteres Bild aufzunehmen. Oder drücken Sie den mittleren Knopf um die Verarbeitung zu starten')
    if GPIO.event_detected(MIDDLE):
        create_play(text='Bitte warten. Die Seiten werden verarbeitet')
        print('Initiating Text extraction')
        for picture_path in pictures:
            image = cv2.imread(picture_path)
            start_time = time.time()
            # text = pytesseract.image_to_string(image=image)
            # text = pytesseract.image_to_string(Image.open(picture_path), lang='deu')
            subprocess.call(['tesseract', picture_path, picture_path.replace(".png",""), '-l', 'deu'], shell=False)
            time_span = time.time() - start_time
            # print(text)
            print(time_span)
        print("pressed middle button")
    if GPIO.event_detected(RIGHT):
        print("pressed right button")
        running = False
    time.sleep(0.2)
