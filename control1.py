# control.py: initializes HackacademyReadingOutLoud
import argparse
import time, os, subprocess
import RPi.GPIO as GPIO
import wave, sys, pyaudio 
import sh

# Controls how to configure the script:
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--scan", default=True,
        help = "Execute image reader")
ap.add_argument("-r", "--reader", default=False,
        help = "Execute image reader")
ap.add_argument('-a', '--ausgabe', help = 'How to convert text to speech')
args = vars(ap.parse_args())

# state holds current state of the user
state = 'home'
# 3 different states: home, memory, reading

# offline: tesseract / or online
mode='online'

# Main Audio Function:
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
        # return prev or next to break the loop and be able to navigate during reading
        if GPIO.input(13) == False:
            return('prev')
        if data == b'' or GPIO.input(11) == False:
            return('next')

#  Initializing raspberrypi 3b + pins.
if bool(args['scan']) == True:
    # Defining input pins for three buttons: left, center and right.
    GPIO.setmode(GPIO.BOARD)                   # Phases:   HOME       |       MEMORY        |       READING
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Takes picture | navigates in memory | goes back a sentence (reading)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Extract text  | navitates in memory | skips a sentence
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Go to memory  | select text to read | stops(?)
    create_play(text='Das System ist bereit. Drucken Sie auf den linken Knopf um Bilder aufzunehmen oder auf den rechten Knopf um Textverarbeitung zu starten.')
    read = True
    count = 0
    while True:
        if GPIO.input(13) == False and GPIO.input(11) == False:
            sys.exit()
        if state == 'home':
        # where user takes the pictures with button 13. 
        # pressing button 11 initializes text extraction.
            if GPIO.input(13) == False:
                create_play(text='Bild wird aufgenommen')
                os.system('python3 camera.py -n DEBUG{}'.format(count))
                count+=1
                time.sleep(2)
                print("Press Button@13 to take a picture")
                create_play(speed=0.93, text='Drucken Sie erneut den gleichen Knopf um ein neues Bild aufzunehmen. Oder drucken Sie den rechten Knopf um Verarbeitung zu starten')
                print("Or Press Button@Pin11 to Extract Text")
            if GPIO.input(11) == False:
                time.sleep(0.2)
                create_play(text='Verarbeitung gestartet')
                print('Initiating Text extraction')
                os.system("python3 images_to_text.py -f scanned_images -m {} -o results".format(mode))
                state='init_memory'
            if GPIO.input(15) == False:
                create_play('Knopf in der Mitte gedrueckt. Zum Speicher')
                state='init_memory'
        elif state =='init_memory':
            # required to initialize memory
            sh.cd('/home/pi/hackdemyk/text_results')
            texts = sh.ls('-t').split()
            number_of_texts = len(texts)
            current_text = 0
            create_play(text='Text wurde extrahiert und als {} gespeichert'.format(texts[current_text]))
            create_play(speed=1, text='''Sie sind jetzt im Speicher. Mit der rechten und linken Knoepfe koennen durch ihre gespeicherten Dokumente navigieren. 
                Wahlen Sie dann einen Text mit dem Knopf in der Mitte um es abzuspielen''')
            state='memory'
        elif state =='memory':
            # Controls to navigate in the memory: where all extracted texts are located.
            # Press right button to skip a section. Press left to go back a session.
            if GPIO.input(11) == False and current_text == number_of_texts-1:
                create_play(texts[current_text])
            if GPIO.input(13) == False and current_text == 0:
                create_play(texts[current_text])
            if GPIO.input(11) == False and current_text < number_of_texts-1:
                current_text += 1
                time.sleep(0.3)
                create_play(texts[current_text])
            if GPIO.input(13) == False and current_text > 0:
                current_text -= 1
                time.sleep(0.3)
                create_play(texts[current_text])
            if GPIO.input(15) == False:
                chosen_text_file = texts[current_text]
                break

create_play(text=chosen_text_file + 'wird abgespielt.')
create_play('Drucken Sie auf den rechten Knopf um vorwarts zu scrollen oder auf den linken Knopf um ruckwaerts zu gehen.')

print(chosen_text_file)
# Reading results.txt into a string
extracted_text = open("/home/pi/hackdemyk/text_results/{}".format(chosen_text_file),"r")
to_read=extracted_text.read()
extracted_text.close()

#Removing linebreaks and removing empty strings in the list
pretext = to_read.split('\n')
pretext = list(filter(None, pretext))

index=0
while index < len(pretext):
    a = create_play(text = pretext[index])
    if a == 'prev' and index > 0:
        index = index -1
    else:
        index +=1

create_play('Program beendet')
