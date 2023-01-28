import time
import argparse
import sys

sys.path.append('../../python/src')

from libnyumaya import AudioRecognition, FeatureExtractor
from auto_platform import AudiostreamSource, default_libpath
from datetime import datetime

def detectKeywords(libpath):

	audio_stream = AudiostreamSource()
	extractor = FeatureExtractor(libpath)
	detector = AudioRecognition(libpath)

	extactor_gain = 1.0
	vad_threshold = 0.5

	keywordVAD = detector.addContinousModel('../../models/Hotword/vad_v3.1.262.premium')
	bufsize = detector.getInputDataSize()

	print("Audio Recognition Version: " + detector.getVersionString())

	audio_stream.start()
	try:
		while(True):
			frame = audio_stream.read(bufsize*2, bufsize*2)
			if(not frame):
				time.sleep(0.01)
				continue
			features = extractor.signalToMel(frame, extactor_gain)
			_ = detector.runDetection(features)

			vadResult = detector.getContinousResult(keywordVAD)
			if(vadResult[1] > vad_threshold):
				print("Speech detected {}".format(datetime.now()))

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

	detectKeywords(FLAGS.libpath)
