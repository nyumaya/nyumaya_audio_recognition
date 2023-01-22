# This example waits for a keyword detection and
# then saves the audio around the detection into
# a file located at saveDirectory with the name
# activation_X where X is an increasing number
# The recordBefore and recordAfter specify the length
# of the audio before and after the activation
#
# This also shows how a postprocessing step for
# the keyword activation could work. For example
# extracting the audio slice and sending it to a
# server for a second opinion

import time
import os
import argparse
import sys
import wave

sys.path.append('../../python/src')

from libnyumaya import AudioRecognition, FeatureExtractor
from auto_platform import AudiostreamSource, default_libpath

bytesPerSample = 2
framesPerSecond = 16000
saveDirectory = "./activations"

def save_wav(data,path):
	print("saving wav to " + path)
	wav = wave.open(path,'w')
	wav.setnchannels(1)
	wav.setsampwidth(bytesPerSample)
	wav.setframerate(framesPerSecond)
	wav.writeframes(data)
	wav.close()

def ensure_dir(file_path):
	if not os.path.exists(file_path):
		os.makedirs(file_path)


#Add one or more keyword models
models = [
	('../../models/Hotword/alexa_v3.1.286.premium',0.95,'alexa_3_1_286'),
]

def recordActivations(libpath):

	audio_stream = AudiostreamSource()
	extractor = FeatureExtractor(libpath)

	detectors = {}
	framebuffersFront = {}
	framebuffersBack = {}

	extactor_gain = 1.0
	recordBefore = 2.5 # Seconds before the activation
	recordAfter = 0.5 # Seconds after the activation

	activationCount = 0
	ensure_dir(saveDirectory)

	rbFrontSize = int(recordBefore*bytesPerSample*framesPerSecond)
	rbBackSize = int(recordAfter*bytesPerSample*framesPerSecond)

	for mpath,msens,mname in models:
		detector = AudioRecognition(libpath)
		detector.addModel(mpath,msens)
		detectors[mname] = detector
		framebuffersFront[mname] = bytearray()
		framebuffersBack[mname] = bytearray()

	bufsize = detector.getInputDataSize()

	print("Audio Recognition Version: " + detector.getVersionString())

	audio_stream.start()
	try:
		while(True):
			frame = audio_stream.read(bufsize*2,bufsize*2)

			if(not frame):
				time.sleep(0.01)
				continue

			for mname in detectors:
				#Fill audio before the activation
				framebuffersFront[mname] = framebuffersFront[mname] + frame
				if(len(framebuffersFront[mname]) > rbFrontSize):
					framebuffersFront[mname] = framebuffersFront[mname][-rbFrontSize:]

			features = extractor.signalToMel(frame,extactor_gain)

			for mname in detectors:
				detector = detectors[mname]
				prediction = detector.runDetection(features)
				if(prediction != 0):
					#FIXME: Record after is currently ignored
					#Fill audio after the activation
					#while(len(framebuffersBack[mname]) < rbBackSize):
					#	frame = audio_stream.read(bufsize*2,bufsize*2)
					#	if(not frame):
					#		time.sleep(0.01)
					#		continue
					#	framebuffersBack[mname] = framebuffersBack[mname] + frame

					savePath = saveDirectory + "/activation_{}_{}_{}.wav".format(mname, activationCount, time.time_ns())
					save_wav(framebuffersFront[mname],savePath)
					#save_wav(framebufferFront+framebufferBack,savePath)
					print("Saving Activation to {}".format(savePath))
					activationCount += 1

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

	recordActivations(FLAGS.libpath)
