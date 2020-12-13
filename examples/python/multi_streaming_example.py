import time
import argparse
import sys


sys.path.append('../../python/src')

from libnyumaya import FeatureExtractor
from multi_detector import MultiDetector

from auto_platform import AudiostreamSource,default_libpath

def light_on():
	print("Turning light on")

def light_off():
	print("Turning light off")

def stop():
	print("Stopping")

def feedback():
	print("Ding")

def history_reset():
	print("History Reset")

def label_stream(libpath):

	extractor = FeatureExtractor(libpath)
	extractor_gain=1.0

	mDetector = MultiDetector(libpath,timeout=20)

	mDetector.add_word("../../models/Hotword/firefox_hotword.premium","firefox",0.5)
	mDetector.add_word("../../models/Command/light_command.premium","light",0.8)
	mDetector.add_word("../../models/Command/off_command.premium","off",0.8)
	mDetector.add_word("../../models/Command/stop_command.premium","stop",0.8)

	mDetector.add_command("firefox,light",light_on)
	mDetector.add_command("firefox,off",light_off)
	mDetector.add_command("stop",stop)

	mDetector.add_detected_callback(feedback)
	mDetector.add_reset_history_callback(history_reset)

	bufsize = mDetector.GetInputDataSize()

	audio_stream = AudiostreamSource()

	audio_stream.start()

	try:
		while(True):
			frame = audio_stream.read(bufsize*2,bufsize*2)

			if(not frame):
				time.sleep(0.01)
				continue

			features = extractor.signalToMel(frame,extractor_gain)
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

