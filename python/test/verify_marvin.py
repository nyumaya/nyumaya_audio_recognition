import time
import os
import argparse
import sys
import datetime

sys.path.append('../../python/src')

from libnyumaya import AudioRecognition, FeatureExtractor
from auto_platform import default_libpath

from pydub import AudioSegment

def split_sequence(a,seg_length):
	return [a[x:x+seg_length] for x in range(0,len(a),seg_length)]


def load_audio_file(filename):
	sound = None
	sound = AudioSegment.from_wav(filename)
	sound = sound.set_frame_rate(16000)
	sound = sound.set_channels(1)
	sound = sound.set_sample_width(2)
	duration = sound.duration_seconds

	return sound,duration

def detectKeywords(libpath,wavpath):
	wav,dur = load_audio_file(wavpath)
	extractor = FeatureExtractor(libpath)
	detector = AudioRecognition(libpath)
	extactor_gain = 1.0

	keywordId = detector.addModel('../../models/Hotword/marvin_v3.1.286.premium',0.5)
	bufsize = detector.getInputDataSize()*2

	wav = wav.get_array_of_samples().tobytes()
	splitdata = split_sequence(wav,bufsize)

	for i,frame in enumerate(splitdata):
		if(bufsize == len(frame)):
			features = extractor.signalToMel(frame)
			prediction = detector.runDetection(features)
			if(prediction > 0):
				return 1 # Keyword detected

	return 0 # No keyword detected


if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--libpath', type=str,
		default=default_libpath,
		help='Path to Platform specific nyumaya_lib.')

	FLAGS, unparsed = parser.parse_known_args()
	res_pos = None
	res_neg = None
	try:
		res_pos = detectKeywords(FLAGS.libpath, "./nearfield_marvin.wav") # Positive Example
		res_neg = detectKeywords(FLAGS.libpath, "./nearfield_sheila.wav") # Negative Example
	except:
		print("Test crashed")
		sys.exit(1)

	if( res_pos == 1 and res_neg == 0):
		print("Test result OK")
		sys.exit(0)
	else:
		print("Test result FAILED")
		sys.exit(1)


