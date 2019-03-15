# EXECUTE AS: 
import os, time
import datetime
import picamera
from PIL import Image, ImageEnhance, ImageFilter
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--scan", default=False,
        help = "specify wether or not apply perspective transform")
ap.add_argument("-p", "--preprocess", default=False,
        help = "Apply a transformation to improve performance")       
ap.add_argument("-n", "--name", default=None,
	help = "Specify pathfile and name to be saved, helps debug\n z.B scanned_images/")
args = vars(ap.parse_args())


def take_picture(speed=150000, name = None, contrast=60, brightness=40):
    """Takes a picture and saves it in the specified path"""       
    if name == None:
        now = datetime.datetime.now()
        name = "/home/pi/hackdemyk/scanned_images/{}-{}-{}um{}:{}:{}.png".format(now.year, now.month, now.day,
                 	                                              now.hour, now.minute, now.second)
    else:
        name = "/home/pi/hackdemyk/scanned_images/{}".format(args['name']+'.png')
    with picamera.PiCamera() as camera:
        print("Take picture")
        camera.resolution = (2592, 1944)
        #camera.resolution = (1280, 960)
        #camera.quality=100
        #camera.iso=0
        # monochrome
        # camera.color_effects = (128,128)
        #camera.contrast=contrast
        #camera.brightness = brightness
        #camera.shutter_speed=speed
        camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2015 by Kai Gaertner'
        # start LED lights
        #self.light_up()
        # take picturee
        camera.capture(name)
        # turn of the lights
        #self.light_off()
        print("[take_picture] Taking picture lasts "+str(time.time() - start_time)+" seconds")
        # rotate picture for processing
        im = Image.open(name)
        im.filter(ImageFilter.SHARPEN)
        im.rotate(270).save(name)
        im.close()
        #NOTE: Applying Perspective Transform
        if bool(args['scan']) == True:
            os.system("python3 scan.py -i {} -o {}".format(name,'scanned.png'))
        #NOTE: Applying some preprocess to improve performance
        # [When the case if ready, and the conditions are fixed. Only then this makes sense]
        if args['preprocess'] == True:
            pass




start_time = time.time()
var = args['name']
take_picture(name = var)
# should return 2 images one normal the other scanned





