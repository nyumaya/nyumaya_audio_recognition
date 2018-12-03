import time
import os
import argparse
import sys
import datetime
import platform

from libnyumaya import AudioRecognition
from libnyumaya import SpeakerVerification

if platform.system() == "Darwin":
	from cross_record import AudiostreamSource
else:
	from record import AudiostreamSource

fingerprints=[]
enrolling = 5

def get_averaged_fingerprint():

	if len(fingerprints) == 0:
		return None

	C=[]
	for i in range(len(fingerprints[0])):
		val = 0
		for f in range(len(fingerprints)):
			val += fingerprints[f][i]
		val /= len(fingerprints)
		C.append(val)
	return C

import math
def cosine_similarity(v1,v2):

	sumxx, sumxy, sumyy = 0, 0, 0
	for i in range(len(v1)):
		x = v1[i]; y = v2[i]
		sumxx += x*x
		sumyy += y*y
		sumxy += x*y
	return sumxy/math.sqrt(sumxx*sumyy)
	
	
#Enrolling:

#Capture 5 samples of word
#Do some kind of averaging
#Store Name and Vector in file

def label_stream(labels,libpath,verification_path ,graph,sensitivity):
	last_frames=[]
	
	#Keyword spotting has 200ms frames, Verifiyer takes 2 seconds of audio
	max_last_frames = 10

	audio_stream = AudiostreamSource()
	detector = AudioRecognition(libpath,graph,labels)
	
	verifiyer = SpeakerVerification(libpath,verification_path)
	detector.SetSensitivity(sensitivity)
	detector.SetGain(1)
	detector.RemoveDC(False)

	bufsize = detector.GetInputDataSize()
	
	print("Bufsize: " + str(bufsize))

	play_command = "play -q" if platform.system() == "Darwin" else "aplay"

	print("Audio Recognition Version: " + detector.GetVersionString())


	print("WARNING EXPERIMENTAL: The voice verification module can be use to verify if")
	print("A command is issued by a certian speaker. It processes speech signals with a")
	print("two second length. This experimental version isn't very good yet.")

	print("\n\n During enrolling a fingerprint of your voice is caputred. By default 5 samples")
	print("Will be captured and averaged. The progam will output a similarity score between 0 and 1")
	print("A value of 1 means totally similar, 0 means different.")
	
	print("Currently a threshold of 0.95 seems good")
	
	print("This module should not be run on a Pi Zero, as it uses excessive CPU")
	print("Verification can also be helpful to reduce false positives of non speech signals")

	audio_stream.start()
	try:
		while(True):
			frame = audio_stream.read(bufsize,bufsize)
			if(not frame):
				time.sleep(0.01)
				continue


			last_frames.append(frame)
			if len(last_frames) > max_last_frames:
				last_frames.pop(0)

			prediction = detector.RunDetection(frame)
		
			if(prediction):
				now = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
				print(detector.GetPredictionLabel(prediction) + " " + now)
				os.system(play_command + " ./ding.wav")
				
				detect_frame = bytearray()
				for element in last_frames:
					detect_frame.extend(element)
					
				print("Running Verification")
					
				features = verifiyer.VerifySpeaker(detect_frame)
				
				if(len(fingerprints) < enrolling):
					print("Enrolling")
					fingerprints.append(features)
				else:
					print("Completed")
				
				print(features)
				
				avg_fingerprint = get_averaged_fingerprint()
				
				if(avg_fingerprint):
					similarity_score = cosine_similarity(features,avg_fingerprint)
					print("Similarity: " + str(similarity_score))


				print("Verification Done")

	except KeyboardInterrupt:
		print("Terminating")
		audio_stream.stop()
		sys.exit(0)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--graph', type=str,
		default='../models/Hotword/marvin_small.tflite',
		help='Model to use for identification.')

	parser.add_argument(
		'--verification_path', type=str,
		default='../models/Experimental/Verification/s-recog.tflite',
		help='Model to use for verification.')

	parser.add_argument(
		'--libpath', type=str,
		default='../lib/linux/libnyumaya.so',
		help='Path to Platform specific nyumaya_lib.')

	parser.add_argument(
		'--labels', type=str,
		default='../models/Hotword/marvin_labels.txt',
		help='Path to file containing labels.')

	parser.add_argument(
		'--sens', type=float,
                default='0.5',
		help='Sensitivity for detection')

	FLAGS, unparsed = parser.parse_known_args()

	label_stream(FLAGS.labels,FLAGS.libpath,FLAGS.verification_path, FLAGS.graph, FLAGS.sens)
