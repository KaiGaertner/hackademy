#!/bin/bash
set -e

sudo apt update
sudo apt install --assume-yes python3 python3-pip python3-dev libopenjp2-7 libtiff5 tesseract-ocr tesseract-ocr-deu portaudio19-dev libjpeg-dev zlib1g-dev

pip3 install pillow picamera RPi.GPIO pyaudio pytesseract pyttsx3 py-picotts

# pico2wave install
sudo apt-get install --assume-yes libttspico-utils

# install raspiaudio head
sudo wget -O mic mic.raspiaudio.com
sudo bash mic -y
