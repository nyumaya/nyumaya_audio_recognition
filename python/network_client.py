import time
import os
import argparse
import sys
import datetime
import platform
import socket

sys.path.append('./src')

from libnyumaya import FeatureExtractor
from auto_platform import AudiostreamSource, play_command,default_libpath


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.0.0.52', 9999))


def send_features(features):
	s.send(features)

def label_stream(libpath):

	audio_stream = AudiostreamSource()

	extractor = FeatureExtractor(libpath)
	extactor_gain=16.0

	bufsize = 3200

	audio_stream.start()
	try:
		while(True):
			frame = audio_stream.read(bufsize*2,bufsize*2)
			if(not frame):
				time.sleep(0.01)
				continue

			features = extractor.signal_to_mel(frame,extactor_gain)
			send_features(features)

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
