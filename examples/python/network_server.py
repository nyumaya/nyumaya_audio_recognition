#!/usr/bin/env python

import socket
import sys
import os
sys.path.append('../../python/src')

from libnyumaya import AudioRecognition
from auto_platform import default_libpath

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 9999))
serversocket.listen(5) # become a server socket, maximum 5 connections

detector = AudioRecognition(default_libpath)
keywordIdFirefox = detector.addModel('../../models/Hotword/alexa_v3.1.286.premium',0.8)

connection, address = serversocket.accept()

while True:
	buf = connection.recv(640)
	if len(buf) > 0:
		prediction = detector.runDetection(buf)
		if(prediction != 0):
			print("Keyword detected")
