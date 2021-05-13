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
import datetime
import wave

sys.path.append('../../python/src')

from libnyumaya import AudioRecognition, FeatureExtractor
from auto_platform import AudiostreamSource, play_command,default_libpath

bytesPerSample = 2
framesPerSecond = 16000

def save_wav(data,path):
	print("saving wav to " + path)
	wav = wave.open(path,'w')
	wav.setnchannels(1)
	wav.setsampwidth(bytesPerSample)
	wav.setframerate(framesPerSecond)
	wav.writeframes(data)
	wav.close()

def recordActivations(libpath):

	audio_stream = AudiostreamSource()
	extractor = FeatureExtractor(libpath)
	detector = AudioRecognition(libpath)

	extactor_gain = 1.0

	recordBefore = 1.5 # Seconds before the activation
	recordAfter = 0.5 # Seconds after the activation

	activationCount = 0
	saveDirectory = "./"
	rbFrontSize = int(recordBefore*bytesPerSample*framesPerSecond)
	rbBackSize = int(recordAfter*bytesPerSample*framesPerSecond)

	framebufferFront = bytearray()
	framebufferBack = bytearray()

	#Add one or more keyword models
	keywordId = detector.addModel('../../models/Hotword/marvin_v2.0.23.premium',0.95)

	bufsize = detector.getInputDataSize()

	print("Audio Recognition Version: " + detector.getVersionString())

	audio_stream.start()
	try:
		while(True):
			frame = audio_stream.read(bufsize*2,bufsize*2)

			if(not frame):
				time.sleep(0.01)
				continue
			#Fill audio before the activation
			framebufferFront = framebufferFront + frame
			if(len(framebufferFront) > rbFrontSize):
				framebufferFront = framebufferFront[-rbFrontSize:]

			features = extractor.signalToMel(frame,extactor_gain)
			prediction = detector.runDetection(features)
			if(prediction != 0):
				#Fill audio after the activation
				while(len(framebufferBack) < rbBackSize):
					frame = audio_stream.read(bufsize*2,bufsize*2)
					if(not frame):
						time.sleep(0.01)
						continue

					framebufferBack = framebufferBack + frame

				savePath = saveDirectory + "activation_{}.wav".format(activationCount)
				save_wav(framebufferFront+framebufferBack,savePath)
				print("Saving Activation to {}".format(savePath))
				activationCount += 1
				os.system(play_command + " ../resources/ding.wav")

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
