import time
import os
import argparse
import sys
import datetime

from libnyumaya import AudioRecognition
from record import AudiostreamSource
from record import RingBuffer

def label_stream(labels,libpath ,graph,sensitivity):

	audio_stream = AudiostreamSource()
	detector = AudioRecognition(libpath,graph)

	detector.SetSensitivity(sensitivity)
	bufsize = detector.GetInputDataSize()

	print("Audio Recognition Version: " + detector.GetVersionString())

	audio_stream.start()
	try:
		while(True):
			frame = audio_stream.read(bufsize,bufsize)
			if(not frame):
				time.sleep(0.01)
				continue

			prediction = detector.RunDetection(frame)

			if(prediction):
				now = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
				print(str(prediction) + " " + now)
				os.system("aplay ./ding.wav")

	except KeyboardInterrupt:
		print("Terminating")
		audio_stream.stop()
		sys.exit(0)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--graph', type=str,
		default='../models/Hotword/sheila_small.tflite',
		help='Model to use for identification.')

	parser.add_argument(
		'--libpath', type=str,
		default='../lib/linux/libnyumaya.so',
		help='Path to Platform specific nyumaya_lib.')

	parser.add_argument(
		'--labels', type=str,
		default='../models/Hotword/sheila_labels.txt',
		help='Path to file containing labels.')

	parser.add_argument(
		'--sens', type=float,
                default='0.05',
		help='Sensitivity for detection')

	FLAGS, unparsed = parser.parse_known_args()

	label_stream(FLAGS.labels,FLAGS.libpath, FLAGS.graph, FLAGS.sens)

