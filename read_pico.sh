#!/bin/bash
pico2wave -l=de-DE -w=sounds/test.wav "$(cat $1)"
#aplay test.wav
