import time
import argparse
import sys


sys.path.append('./src')

from libnyumaya import FeatureExtractor
from multi_detector import MultiDetector

from auto_platform import AudiostreamSource,default_libpath


hotword_graph="../models/Hotword/marvin_small_0.3.tflite"
hotword_labels="../models/Hotword/marvin_labels.txt"

#Note: subset_small_0.3 and subset_big_0.3 currently have a very low accuracy. 
#A newer model for on/off gives much better results. Take a look at 
#sonoff_switch.py for usage details.

action_graph="../models/Command/subset_small_0.3.tflite"
action_labels="../models/Command/subset_labels.txt"



def light_on():
	print("Turning light on")

def light_off():
	print("Turning light off")

def stop():
	print("Stopping")


def label_stream(libpath):

	extractor = FeatureExtractor(libpath)
	extractor_gain=1.0

	mDetector = MultiDetector(libpath,timeout=20)

	mDetector.add_detector(action_graph,action_labels,0.8)
	mDetector.add_detector(hotword_graph,hotword_labels,0.5)

	mDetector.add_command("marvin,on",light_on)
	mDetector.add_command("marvin,off",light_off)
	mDetector.add_command("stop",stop)

	bufsize = mDetector.GetInputDataSize()

	audio_stream = AudiostreamSource()

	audio_stream.start()

	try:
		while(True):
			frame = audio_stream.read(bufsize*2,bufsize*2)

			if(not frame):
				time.sleep(0.01)
				continue

			features = extractor.signal_to_mel(frame,extractor_gain)
			mDetector.run_frame(features)

	except KeyboardInterrupt:
		print("Terminating")
		audio_stream.stop()
		sys.exit(0)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()


	parser.add_argument(
		'--libpath', type=str,
		default=default_libpath,
		help='Path to Platform specific nyumaya_lib.')



	FLAGS, unparsed = parser.parse_known_args()

	label_stream(FLAGS.libpath)

