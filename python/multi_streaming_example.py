import time
import os
import argparse
import sys
import datetime
import numpy as np

from libnyumaya import AudioRecognition
from record import AudiostreamSource
from record import RingBuffer

libpath = "../lib/linux/libnyumaya.so"
hotword_graph="../../nyumaya_audio_recognition_models/Hotword/marvin_small.tflite"
hotword_labels="../../nyumaya_audio_recognition_models/Hotword/marvin_labels.txt"

numbers_graph="../../nyumaya_audio_recognition_models/Command/numbers_big.tfile"
numbers_labels="../../nyumaya_audio_recognition_models/Command/numbers_labels.txt"

action_graph="../../nyumaya_audio_recognition_models/Command/subset_big.tflite"
action_labels="../../nyumaya_audio_recognition_models/Command/subset_labels.txt"



def label_stream():

	hotword_detected = False
	countdown = 0

	audio_stream = AudiostreamSource()

	action_detector = AudioRecognition(libpath,action_graph)
	hotword_detector = AudioRecognition(libpath,hotword_graph)
	#
	#action_detector = hotword_detector

	hotword_detector.SetSensitivity(0.5)
	action_detector.SetSensitivity(0.95)
	bufsize = hotword_detector.GetInputDataSize()
	audio_stream.start()

	print("Audio Recognition Version: " + hotword_detector.GetVersionString())
	try:
		while(True):
			frame = audio_stream.read(bufsize,bufsize)
 
			if(not frame):
				time.sleep(0.01)
				continue

			data = np.frombuffer(frame, dtype=np.int16)

			if(countdown > 0):
				countdown -= 1
				if(countdown == 0):
					hotword_detected = False
					print("Stopped Listening")

			if(not hotword_detected):
				prediction = hotword_detector.RunDetection(data,bufsize)
				if(prediction):
					hotword_detected = True
					countdown = 20
					now = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
					print("Listening")
			else:
				prediction = action_detector.RunDetection(data,bufsize)
				if(prediction):
					print("Got Action: " + str(prediction))
					countdown = 0
					hotword_detected = False



	except KeyboardInterrupt:
		print("Terminating")
		audio_stream.stop()
		sys.exit(0)

if __name__ == '__main__':
	label_stream()

