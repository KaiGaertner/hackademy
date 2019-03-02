import os, time, subprocess, sys, signal
from datetime import datetime

import picamera
from PIL import Image, ImageEnhance, ImageFilter
DEBUG = True

brightness=37
contrast=55
speed=150000

name = "b"+str(brightness)+"-c"+str(contrast)+"-s"+str(speed)+".png"

def shoot(name):

#def take_picture(self,name=None):
	if DEBUG:
		start_time = time.time()
	if not name:
		name = "pics/"+str(datetime.now()).replace(' ','_')+'.png'
	last_picture = name
	with picamera.PiCamera() as camera:
		print "Take picture"
		camera.resolution = (2592, 1944)
		# monochrome
		camera.color_effects = (128,128)
		camera.contrast=contrast
		camera.brightness = brightness
		camera.shutter_speed=speed
		camera.quality=100
		camera.exif_tags['IFD0.Artist'] = 'Kai Gaertner'
		camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2015 by Kai Gaertner'
		# start LED lights
		#self.light_up()
		# take picture
		camera.capture(name)

		if DEBUG:
			print "[take_picture] Taking picture lasts "+str(time.time() - start_time)+" seconds"
		# rotate picture for processing
		print "Rotate picture!"
		im = Image.open(name)
		im.filter(ImageFilter.SHARPEN)
		im.rotate(-90).save(name)
		

def read(picture=None):
	if DEBUG:
		start_time = time.time()
	print "Start OCR!"
	if not picture:
		picture = last_picture
	textfile = picture.replace(".png",".txt").replace('pics/', 'texts/')
	last_textfile = textfile
	subprocess.call(['tesseract', picture, textfile.replace(".txt",""), '-l', 'deu'], shell=False)
	print "TESSERACT OCR finished!"
	if DEBUG:
		print "[read] OCR analysis takes "+str(time.time() - start_time)+" seconds"

shoot(name)
read(name)
