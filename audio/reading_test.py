#!/usr/bin/python3
import pyttsx3

import wave
import io
import pyaudio
# import PicoTTS
from picotts import PicoTTS



engine = pyttsx3.init()
engine.say('Good morning')
engine.runAndWait()


picotts = PicoTTS()
wavs = picotts.synth_wav('Good morning')

"""
print(wavs)
bytes = io.BytesIO(wavs)
print(bytes)
s = io.StringIO(wavs)"""
f = wave.open('./bam.wav')

chunk = 1024

p = pyaudio.PyAudio()
#open stream
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                channels = f.getnchannels(),
                rate = f.getframerate(),
                output = True)
#read data
data = f.readframes(chunk)

#play stream
while data:
    stream.write(data)
    data = f.readframes(chunk)

#stop stream
stream.stop_stream()
stream.close()

#close PyAudio
p.terminate()

print(f.getnchannels(), f.getframerate(), f.getnframes())
