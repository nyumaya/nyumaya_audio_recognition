#!/usr/bin/env python

import socket
import sys
import os
sys.path.append('./src')

from libnyumaya import FeatureExtractor
from multi_detector import MultiDetector

libpath = "../lib/linux/libnyumaya.so"

hotword_graph="../models/Hotword/marvin_big_0.3.tflite"
hotword_labels="../models/Hotword/marvin_labels.txt"

action_graph="../models/Command/on_off_big_0.3.tflite"
action_labels="../models/Command/on_off_labels.txt"

sonoff_ip="10.0.0.54"


def light_on():
	print("Turning light on")
	os.system("curl http://" + sonoff_ip +"/cm?cmnd=Power%20On &")

def light_off():
	print("Turning light off")
	os.system("curl http://" + sonoff_ip +"/cm?cmnd=Power%20Off &")
	
def detected_something_callback():
	#os.system(play_command + " ./resources/tone-beep.wav")
	print("Detected Something")
	
def reset_history_callback():
	print("Reset History")


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 9999))
serversocket.listen(5) # become a server socket, maximum 5 connections


mDetector = MultiDetector(libpath,timeout=20)

mDetector.add_detector(action_graph,action_labels,0.8)
mDetector.add_detector(hotword_graph,hotword_labels,0.5)

mDetector.add_command("marvin,on",light_on)
mDetector.add_command("marvin,off",light_off)

mDetector.add_reset_history_callback(reset_history_callback)
mDetector.add_detected_callback(detected_something_callback)

connection, address = serversocket.accept()

while True:
	buf = connection.recv(800)
	if len(buf) > 0:
		mDetector.run_frame(buf)

