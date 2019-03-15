import argparse
import time, os, subprocess
import RPi.GPIO as GPIO
import wave, sys, pyaudio 


# Controls how to configure raspberry pins: Add more modes?
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--scan", default=True,
        help = "Execute image reader")
ap.add_argument("-r", "--reader", default=False,
        help = "Execute image reader")
ap.add_argument('-a', '--ausgabe', help = 'How to convert text to speech')
args = vars(ap.parse_args())


# Audio
def create_play(text, speed=0.93, language='de-DE'):
    '''transforms given text into a temporary wav file and plays it. 
       text: words to be spoken
       speed: changes rate of sound [0-1]
       language: choose language see aplay -h'''

    os.system('''pico2wave -l {} -w /home/pi/hackdemyk/audio/temp.wav "{}"'''.format(language,text))
    sound = wave.open("/home/pi/hackdemyk/audio/temp.wav")
    p = pyaudio.PyAudio()
    chunk = 1024
    stream = p.open(format =
                p.get_format_from_width(sound.getsampwidth()),
                channels = sound.getnchannels(),
                rate = int(sound.getframerate()*speed),
                output = True)
    data = sound.readframes(chunk)
    while True:
        if data != '':
            stream.write(data)
            data = sound.readframes(chunk)
        if data == b'':
            break

#  Initializing raspberrypi 3b + pins.
#create_play(text='Das System is bereit. Drucken Sie auf den linken Knopf um Bilder aufzunehmen. Wenn sie fertig sind, drucken sie auf den rechten Knopf um die Textverarbeitung zu starten')
create_play(text='Das System is bereit')
if bool(args['scan']) == True:
    # RPi.GPIO Layout verwenden (wie Pin-Nummern)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) # When Button pressed, voltage received, taking a photo
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    read = True
    count = 0
    while True:
        if GPIO.input(13) == False:
            create_play(text='Bild wird aufgenommen')
            os.system('python3 camera.py -n DEBUG{}'.format(count))
            count+=1
            time.sleep(2)
            print("Press Button@13 to take a picture")
            create_play(speed=0.93, text='Drucken Sie erneut den gleichen Knopf um ein neues Bild aufzunehmen. Oder drucken Sie den rechten Knopf um Verarbeitung zu starten')
            print("Or Press Button@Pin11 to Extract Text")
        if GPIO.input(11) == False:
            print('Initiating Text Extraction')
            mode='online'
            create_play(text='Verarbeitung gestartet')
            os.system("python3 images_to_text.py -f scanned_images -m {} -o results".format(mode))
            break
print('Completed')


extracted_text = open("/home/pi/hackdemyk/text_results/results.txt","r") 
to_read=extracted_text.read()
extracted_text.close()

create_play(text = to_read, language='de-DE')
