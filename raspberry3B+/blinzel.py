import os, time, subprocess, sys, signal
import pyaudio, wave
from datetime import datetime

import picamera
from PIL import Image, ImageEnhance, ImageFilter



class Blinzler:
	""" Main Class for the Blinzler Devise """
	picture_text = []
	last_textfile = ""
	last_picture = ""
	last_text = ""
	current_index = 0
	STOP = False
	END_OF_TEXT = False
	# process id for reading subprocess
	SPEAK_PROCESS = False
	#TTS_SYSTEM = "ESPEAK"
	TTS_SYSTEM = "PICOTTS"
	OCR_SYSTEM = "TESSERACT"
	#OCR_SYSTEM = "OCRAD"
	DEBUG = True

	def take_picture(self,speed=150000, name=None, contrast=60, brightness=40):
	#def take_picture(self,name=None):
		#subprocess.call(['aplay', 'sounds/start_reading.wav'])
		self.play_audio('sounds/start_reading.wav')
		if self.DEBUG:
			start_time = time.time()
		if not name:
			name = "pics/"+str(datetime.now()).replace(' ','_')+'.png'
		self.last_picture = name
		with picamera.PiCamera() as camera:
			print "Take picture"
			camera.resolution = (2592, 1944)
			#camera.resolution = (1280, 960)
			camera.quality=100
			#camera.iso=0
			# monochrome
			camera.color_effects = (128,128)
			#camera.contrast=contrast
			#camera.brightness = brightness
			#camera.shutter_speed=speed
			camera.exif_tags['IFD0.Artist'] = 'Kai Gaertner'
			camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2015 by Kai Gaertner'
			# start LED lights
			#self.light_up()
			# take picture
			camera.capture(name)
			# turn of the lights
			#self.light_off()
			if self.DEBUG:
				print "[take_picture] Taking picture lasts "+str(time.time() - start_time)+" seconds"
			# rotate picture for processing
			print "Rotate picture!"
			im = Image.open(name)
			im.filter(ImageFilter.SHARPEN)
			im.rotate(-90).save(name)

	def rotate_picture(self, picture=None):
		if not picture:
			picture = self.last_picture
		pass

	def make_ocr(self, picture=None):
		if self.DEBUG:
			start_time = time.time()
		print "Start OCR!"
		if not picture:
			picture = self.last_picture
		textfile = picture.replace(".png",".txt").replace('pics/', 'texts/')
		self.last_textfile = textfile
		self.picture_text.append([picture, textfile])
		if self.OCR_SYSTEM == "TESSERACT":
			subprocess.call(['tesseract', picture, textfile.replace(".txt",""), '-l', 'deu'], shell=False)
			print "TESSERACT OCR finished!"
		if self.OCR_SYSTEM == "OCRAD":
			#subprocess.call(['tesseract', picture, textfile.replace(".txt",""), '-l', 'deu'], shell=False)
			# pngtopnm test.png | ocrad -c iso-8859-15 > test_ocrad.txt && \
			# 	iconv -f ISO-8859-15 test_ocrad.txt -t UTF-8 -o test_ocrad.txt
			#PIPE = subprocess.PIPE
			#p1 = subprocess.Popen(["pngtopnm", picture], stdout=PIPE)
			#p2 = subprocess.Popen(["ocrad", "-c iso-8859-15", "> "+textfile], stdin=p1.stdout, stdout=PIPE)
			#p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
			#output = p2.communicate()[0]
			#subprocess.Popen(['iconv', '-f ISO-8859-15', textfile, '-t UTF-8', '-o '+textfile])
			os.system('pngtopnm '+picture+' | ocrad -c iso-8859-15 > '+textfile
						+' && iconv -f ISO-8859-15 '+textfile+' -t UTF-8 -o '+textfile)
			print "OCRAD OCR finished!"
		if self.DEBUG:
				print "[make_ocr] Process OCR lasts "+str(time.time() - start_time)+" seconds"
		return textfile
		
	
	def read_ocr(self, textfile=False):
		# read textfile to variable
		if not textfile:
			textfile = self.last_textfile
		f = open(textfile, 'r')
		self.last_text = f.read()
		#print self.last_text
	
	def split_ocr(self, textfile=False):
		self.read_ocr(textfile)
		# split in lines and remove blank lines
		#self.last_text_array = list(filter(lambda x: x!= '', self.last_text.rstrip().split()))
		self.last_text_array = list(filter(lambda x: x!= '', self.last_text.rstrip().split('\n')))

	def read_word(self):
		# reads text by words (formerly used for threaded solution
		index = self.current_index
		print self.last_text_array[index]
		subprocess.call(['espeak', '-vde', self.last_text_array[index]], shell=False)
		if index < len(self.last_text_array)-1:
			self.current_index = index+1
		else:
			self.current_index = 0
			self.END_OF_TEXT = True
	
	def speak_text(self, text=None):
		if not text:
			text = self.last_text
		# read text with espeak in subprocess and returns espeak pid
		# espeak-data folder /usr/lib/x86_64-linux-gnu/espeak-data
		if self.TTS_SYSTEM == "ESPEAK":
			# problem mit langen Texten, benutze Pipe auf aplay: '-f stdout |aplay'
			self.SPEAK_PROCESS = subprocess.Popen(['espeak', '-vde', self.last_text, '-f stdout |aplay'])
			# mbrola-voices mit -vmb-de* und '-s 100' fuer Geschwindigkeit
			#self.SPEAK_PROCESS = subprocess.Popen(['espeak', '-vmb-de4', '-s 150' ,self.last_text])
			print "eSPEAK-Process pid: "+ str(self.SPEAK_PROCESS.pid)
			sys.stdout.flush()
			return self.SPEAK_PROCESS.pid
		if self.TTS_SYSTEM == "PICOTTS":
			self.read_ocr()
			soundfile = self.last_textfile.replace('.txt','.wav').replace('texts/','sounds/') 
			print '[speak_text] '+ soundfile
			#subprocess.Popen(['pico2wave', '--lang=de-DE', '--wave=sounds/'+self.last_textfile.replace('.txt','.wav'),text], shell=False)
			#os.system('sh read_pico.sh "$(cat texts/'+self.last_textfile+')"')
			subprocess.call(['pico2wave', '-l=de-DE', '-w='+soundfile, self.last_text])
			#subprocess.call(['aplay', soundfile])
			#subprocess.call(['aplay', 'sounds/stopped_reading.wav'])
			self.play_audio(soundfile)
			self.play_audio('sounds/stopped_reading.wav')
			print "Finished Reading"
			
		
	def stop_reading(self):
		# stop process by signal SIGSTOP
		if self.SPEAK_PROCESS.pid:
			self.SPEAK_PROCESS.send_signal(signal.SIGSTOP)
		pass
			
	def continue_reading(self):
		# continue process by signal SIGCONT
		if self.SPEAK_PROCESS.pid:
			self.SPEAK_PROCESS.send_signal(signal.SIGCONT)
		pass
			
		
	def speak_runtest(self):
		# check speak process
		# True - processs running
		# otherwise - returncode
		try:
			if self.SPEAK_PROCESS.poll() == None:
				return True
			else: 
				return self.SPEAK_PROCESS.returncode
		except:
			print "Fehler!"

	def play_audio(self,file):
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


