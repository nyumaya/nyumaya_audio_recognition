import time
import os
import argparse
import sys
import datetime

from recognition import Detector
from record import AudiostreamSource
from record import RingBuffer

hotword_graph="/home/anon/Desktop/nyumaya_audio_recognition_models/Hotword/sheila/conv-conv-big/conv-conv-big_frozen.pb"
hotword_labels="/home/anon/Desktop/nyumaya_audio_recognition_models/Hotword/sheila/labels.txt"

numbers_graph="/home/anon/Desktop/nyumaya_audio_recognition_models/Command/Numbers/conv-conv-big/conv-conv-big_frozen.pb"
numbers_labels="/home/anon/Desktop/nyumaya_audio_recognition_models/Command/Numbers/labels.txt"

action_graph="/home/anon/Desktop/nyumaya_audio_recognition_models/Command/Action/conv-conv-big/conv-conv-big_frozen.pb"
action_labels="/home/anon/Desktop/nyumaya_audio_recognition_models/Command/Action/labels.txt"



def label_stream():

	hotword_detected = False
	countdown = 0

	audio_stream = AudiostreamSource()

	hotword_detector = Detector(hotword_graph,hotword_labels)
	action_detector = Detector(action_graph,action_labels)

	hotword_detector.set_sensitivity(0.5)
	action_detector.set_sensitivity(0.99)
	bufsize = hotword_detector.input_data_size()
	audio_stream.start()
	try:
		while(True):
			frame = audio_stream.read(bufsize,bufsize)
			if(not frame):
				time.sleep(0.01)
				continue

			if(countdown > 0):
				countdown -= 1
				if(countdown == 0):
					hotword_detected = False
					print("Stopped Listening")

			if(not hotword_detected):
				prediction = hotword_detector.recognize(frame)
				if(prediction):
					hotword_detected = True
					countdown = 20
					now = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
					print("Listening")
			else:
				prediction = action_detector.recognize(frame)
				if(prediction):
					print("Got Action: " + prediction)
					countdown = 0
					hotword_detected = False



	except KeyboardInterrupt:
		print("Terminating")
		audio_stream.stop()
		sys.exit(0)

if __name__ == '__main__':
	label_stream()

