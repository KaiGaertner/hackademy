import argparse
import time, os, subprocess
import RPi.GPIO as GPIO

# Controls how to configure raspberry pins: Add more modes?
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--scan", default=True,
        help = "Execute image reader")
ap.add_argument("-r", "--reader", default=False,
        help = "Execute image reader")
args = vars(ap.parse_args())

# _ _ _ _ _ _ _  _ _ _ _ _ _ _  _ _ _  _
# Button pin 40
if bool(args['scan']) == True:
    # RPi.GPIO Layout verwenden (wie Pin-Nummern)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # When Button pressed, voltage received, taking a photo
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    read = True
    #blinzler.play_audio('sounds/hello.wav')
    print('Press Button@Pin12 to take a picture')
    print("Press Button@Pin11 to take a picture")
    count = 0
    while True:
        if GPIO.input(12) == False:
            # Execute Code - s True
            os.system('python3 camera.py -n DEBUG{}'.format(count))
            count+=1
            time.sleep(2)
            print("Ready to take  another picture")
            print("Or Press Button@Pin11 to Extract Text")
        if GPIO.input(11) == False:
            print('Initiating Text Extraction')
            mode='offline'
            os.system("python3 images_to_text.py -f scanned_images -m {} -o results".format(mode))
            break
print('Completed')
