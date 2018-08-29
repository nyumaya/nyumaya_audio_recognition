import time
import os
import argparse
import sys

from recognition import Detector
from record import AudiostreamSource
from record import RingBuffer




def label_stream(labels, graph):
	audio_stream = AudiostreamSource()
	detector = Detector(graph,labels)
	detector.set_sensitivity(0.5)
	bufsize = detector.input_data_size()
	audio_stream.start()
	try:
		while(True):
			frame = audio_stream.read(bufsize,bufsize)
			prediction = detector.recognize(frame)
			if(not prediction):
				time.sleep(0.01)
			else: 	
				print(prediction)
	except KeyboardInterrupt:
		print("Terminating")
		audio_stream.stop()
		sys.exit(0)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--graph', type=str,
		default='./models/marvin_hotword/conv-res-mini_frozen.pb', 
		help='Model to use for identification.')

	parser.add_argument(
		'--labels', type=str,
		default='./models/marvin_hotword/labels.txt',
		help='Path to file containing labels.')

	FLAGS, unparsed = parser.parse_known_args()

	label_stream(FLAGS.labels, FLAGS.graph)

