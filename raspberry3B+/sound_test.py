"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys

def play_audio(file):
	CHUNK = 1024
	
	wf = wave.open(file, 'rb')
	
	p = pyaudio.PyAudio()
	
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
	                channels=wf.getnchannels(),
	                rate=wf.getframerate(),
	                output=True)
	
	data = wf.readframes(CHUNK)
	
	while data != '':
	    stream.write(data)
	    data = wf.readframes(CHUNK)
	
	stream.stop_stream()
	stream.close()
	
	p.terminate()

if len(sys.argv) < 2:
    	print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
	sys.exit(-1)
play_audio(sys.argv[1])