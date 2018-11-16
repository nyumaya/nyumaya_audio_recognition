import time
import os
import argparse
import sys
import datetime
import platform

from libnyumaya import AudioRecognition

if platform.system() == "Darwin":
	from cross_record import AudiostreamSource
else:
	from record import AudiostreamSource


def label_stream(labels,libpath ,graph,sensitivity):

	audio_stream = AudiostreamSource()
	detector = AudioRecognition(libpath,graph,labels)

	detector.SetSensitivity(sensitivity)
	detector.SetGain(1)
	detector.RemoveDC(False)
	
	bufsize = detector.GetInputDataSize()

	play_command = "play -q" if platform.system() == "Darwin" else "aplay"

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
				print(detector.GetPredictionLabel(prediction) + " " + now)
				os.system(play_command + " ./ding.wav")

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
                default='0.5',
		help='Sensitivity for detection. A lower value means more sensitivity, for example,'
		     '0.1 will lead to less false positives, but will also be harder to trigger.'
		     '0.9 will make it easier to trigger, but lead to more false positives')

	FLAGS, unparsed = parser.parse_known_args()

	label_stream(FLAGS.labels,FLAGS.libpath, FLAGS.graph, FLAGS.sens)
