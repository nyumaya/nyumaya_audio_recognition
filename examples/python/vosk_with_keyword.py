import os
import argparse
import sys
import datetime
import time
from vosk import Model, KaldiRecognizer


sys.path.append('../../python/src')

from libnyumaya import AudioRecognition, FeatureExtractor
from auto_platform import AudiostreamSource, play_command, default_libpath

def detectKeywords(libpath):

	audio_stream = AudiostreamSource()
	extractor = FeatureExtractor(libpath)
	detector = AudioRecognition(libpath)

	framerate = 16000
	model = Model("model")

	#Let's define a custom dictionary
	rec = KaldiRecognizer(model, framerate, '["oh one two three four five six seven eight nine zero", "[unk]"]')

	extactor_gain = 1.0

	#Add one or more keyword models
	keywordIdAlexa = detector.addModel('../../models/Hotword/alexa_v3.1.286.premium',0.85)

	bufsize = detector.getInputDataSize()

	print("Audio Recognition Version: " + detector.getVersionString())

	command_started = False

	audio_stream.start()
	try:
		while(True):
			# Wakeword loop
			if(not command_started):
				frame = audio_stream.read(bufsize*2,bufsize*2)
				if(not frame):
					time.sleep(0.01)
					continue

				features = extractor.signalToMel(frame,extactor_gain)
				prediction = detector.runDetection(features)
				if(prediction != 0):
					now = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
					if(prediction == keywordIdAlexa):
						print("Alexa detected:" + now)

					os.system(play_command + " ../resources/ding.wav")
					command_started = True
			# vosk loop
			else:
				frame = audio_stream.read(4000,4000)
				if(not frame):
					time.sleep(0.01)
					continue

				if rec.AcceptWaveform(bytes(frame)):
					print(rec.Result())
					command_started = False
					print(rec.FinalResult())

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
