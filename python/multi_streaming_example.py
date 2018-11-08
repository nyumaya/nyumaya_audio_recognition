import time
import os
import argparse
import sys
import datetime

from multi_detector import MultiDetector
from record import AudiostreamSource

hotword_graph="../models/Hotword/marvin_small.tflite"
hotword_labels="../models/Hotword/marvin_labels.txt"


action_graph="../models/Command/subset_small.tflite"
action_labels="../models/Command/subset_labels.txt"



def light_on():
	print("Turning light on")

def light_off():
	print("Turning light off")

def stop():
	print("Stopping")


def label_stream(libpath):
	
	mDetector = MultiDetector(libpath,timeout=20)
	
	mDetector.add_detector(action_graph,action_labels,0.8)
	mDetector.add_detector(hotword_graph,hotword_labels,0.5)
	
	mDetector.SetGain(1)
	mDetector.RemoveDC(False)
	
	mDetector.add_command("marvin,on",light_on)
	mDetector.add_command("marvin,off",light_off)
	mDetector.add_command("stop",stop)

	bufsize = mDetector.GetInputDataSize()
	
	audio_stream = AudiostreamSource()

	audio_stream.start()

	try:
		while(True):
			frame = audio_stream.read(bufsize,bufsize)
 
			if(not frame):
				time.sleep(0.01)
				continue

			mDetector.run_frame(frame)

	except KeyboardInterrupt:
		print("Terminating")
		audio_stream.stop()
		sys.exit(0)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()


	parser.add_argument(
		'--libpath', type=str,
		default='../lib/linux/libnyumaya.so',
		help='Path to Platform specific nyumaya_lib.')



	FLAGS, unparsed = parser.parse_known_args()

	label_stream(FLAGS.libpath)

