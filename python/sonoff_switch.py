import time
import os
import argparse
import sys
import platform

sys.path.append('./src')

from libnyumaya import FeatureExtractor
from multi_detector import MultiDetector

if platform.system() == "Darwin":
	from cross_record import AudiostreamSource
else:
	from record import AudiostreamSource
	
hotword_graph="../models/Hotword/marvin_small_0.3.tflite"
hotword_labels="../models/Hotword/marvin_labels.txt"


action_graph="../models/Command/on_off_big_0.3.tflite"
action_labels="../models/Command/on_off_labels.txt"

play_command = "play -q" if platform.system() == "Darwin" else "aplay"

sonoff_ip="10.0.0.54"

def light_on():
	print("Turning light on")
	os.system("curl http://" + sonoff_ip +"/cm?cmnd=Power%20On &")

def light_off():
	print("Turning light off")
	os.system("curl http://" + sonoff_ip +"/cm?cmnd=Power%20Off &")
	
def detected_something_callback():
	os.system(play_command + " ./resources/tone-beep.wav")
	print("Detected Something")
	
def reset_history_callback():
	print("Reset History")

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
	
	mDetector.add_reset_history_callback(reset_history_callback)
	mDetector.add_detected_callback(detected_something_callback)

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
		default='../lib/linux/libnyumaya.so',
		help='Path to Platform specific nyumaya_lib.')



	FLAGS, unparsed = parser.parse_known_args()

	label_stream(FLAGS.libpath)

