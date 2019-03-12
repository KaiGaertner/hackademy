import wave, sys, pyaudio, os, subprocess
import time


def create_play(text):
    os.system('''pico2wave -w /home/pi/hackdemyk/audio/bam.wav "Look Beast, I  see you're really upset about this."''')
    sound = wave.open("/home/pi/hackdemyk/audio/bam.wav")
    p = pyaudio.PyAudio()
    chunk = 1024
    stream = p.open(format =
                p.get_format_from_width(sound.getsampwidth()),
                channels = sound.getnchannels(),
                rate = sound.getframerate(),
                output = True)
    data = sound.readframes(chunk)
    while True:
        if data != '':
            stream.write(data)
            data = sound.readframes(chunk)
        if data == b'':
            break

create_play('hello')
