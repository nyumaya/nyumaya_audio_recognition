from __future__ import unicode_literals
from __future__ import division

import argparse
import sys
import time
import os
import csv
import re
import hashlib

from os import walk
from os.path import splitext
from os.path import join

from pydub import AudioSegment
from libnyumaya import AudioRecognition
from random import randint

samplerate=16000


def load_audio_file(filename,resize=False):
	sound = None
	try:
		if filename.endswith('.mp3'):
			sound = AudioSegment.from_mp3(filename)
		elif filename.endswith('.wav'):
			sound = AudioSegment.from_wav(filename)

		sound = sound.set_frame_rate(samplerate)
		sound = sound.set_channels(1)
		sound = sound.set_sample_width(2)
		duration = sound.duration_seconds
	except:
		print("Couldn't load file")
		return None,None
		
	return sound,duration


def get_cv_list(labels_list,cvcorpus_path):
	csvfile = open(cvcorpus_path+"cv-valid-test.csv",'r')
	csvFileArray = []
	first = True
	i = 0
	for row in csv.reader(csvfile, delimiter = ','):
		if(first):
			first = False
			continue

		filepath = row[0]
		
		base = os.path.splitext(filepath)[0]
		filepath = base + ".wav"
		text = row[1].lower()    
		use = True
		for wanted_word in labels_list:
			if((wanted_word.lower() + " ") in text):  
				use = False

		if(use == True):
			i = i + 1
			csvFileArray.append(os.path.join(cvcorpus_path,filepath))
	return csvFileArray


def run_good_predictions(detector,good_folder,noise_folders,add_noise,sensitivity):

	detector.SetSensitivity(sensitivity)
	bufsize = detector.GetInputDataSize()
	
	good_predictions = 0
	wrong_predictions = 0
	missed_predictions = 0
	sample_number = 0

	testing_set = include_good_folder(good_folder,detector.labels_list)


	noise_list = []
	noise_folder_list = noise_folders.split(',')
	for noise_folder in noise_folder_list:
		noise_list += include_random_folder(noise_folder)
	
	for datapoint in testing_set:

		current_label = datapoint['label']

		wavdata,duration = load_audio_file(datapoint['file'])

		if(not wavdata):
			continue

		if(add_noise):
			bg_noise_file = get_random_file(noise_list)
			noise,noise_duration = load_audio_file(bg_noise_file)

			if(not noise):
				print("Couldn't load: " + bg_noise_file)
			else:
				wavdata = wavdata.overlay(noise, gain_during_overlay=0)

		one_second_silence = AudioSegment.silent(duration=1000)
		wavdata += one_second_silence
		splitdata = split_sequence(wavdata.raw_data,bufsize)

		sample_number += 1
	
		has_detected_something = False
		
		for frame in splitdata:
	
			prediction = detector.RunDetection(frame)

			if(prediction == 0):
				continue

			prediction = detector.GetPredictionLabel(prediction)

			if(prediction == current_label) :
				good_predictions += 1
				has_detected_something = True
			else:
				wrong_predictions += 1
				has_detected_something = True

		if(not has_detected_something):
			missed_predictions += 1

	return wrong_predictions, good_predictions, missed_predictions, sample_number


MAX_NUM_WAVS_PER_CLASS = 2**27 - 1  # ~134M
RANDOM_SEED = 59185
def which_set(filename, validation_percentage=2, testing_percentage=10):

	base_name = os.path.basename(filename)

	hash_name = re.sub(r'_nohash_.*$', '', base_name)

	#hash_name_hashed = hashlib.sha1(compat.as_bytes(hash_name)).hexdigest()
	hash_name_hashed = hashlib.sha1(hash_name.encode('utf-8')).hexdigest()
	percentage_hash = ((int(hash_name_hashed, 16) %
		(MAX_NUM_WAVS_PER_CLASS + 1)) *
		(100.0 / MAX_NUM_WAVS_PER_CLASS))
		
	if percentage_hash < validation_percentage:
		result = 'validation'
	elif percentage_hash < (testing_percentage + validation_percentage):
		result = 'testing'
	else:
		result = 'training'
	return result

#use include_only_test_files = False if you want to test against
#your own data
def include_good_folder(path,labels,include_only_test_files=True):
	file_list = []
	for root, dirs, files in walk(path):
		for f in files:
			if splitext(f)[1].lower() == ".wav":
				dirname = os.path.basename(os.path.dirname(join(root, f)))
				if(include_only_test_files):
					if(dirname in labels and which_set(f) == 'testing'):
						file_list.append({'label': dirname, 'file': join(root, f)}) 
				else:
					if(dirname in labels):
						file_list.append({'label': dirname, 'file': join(root, f)}) 
				
	return file_list

def include_random_folder(path):
	file_list=[]
	for root, dirs, files in walk(path):
		for f in files:
			if splitext(f)[1].lower() == ".wav":
				file_list.append(join(root, f)) 
	return file_list


def split_sequence(a,seg_length):
	return [a[x:x+seg_length] for x in range(0,len(a),seg_length)]


def get_random_file(file_list):
	filelen = len(file_list)
	index  = randint(0,filelen-1)
	return file_list[index]

def run_bad_predictions(detector,cv_folder,bad_folders,sensitivity):

	detector.SetSensitivity(sensitivity)
	bufsize = detector.GetInputDataSize()

	seconds = 0
	false_predictions = 0
	bad_predictions = 0
	file_count = 0
	filelist=get_cv_list(detector.labels_list,cv_folder)
	bad_folders = bad_folders.split(',')
	for folder in bad_folders:
		filelist = filelist + include_random_folder(folder)

	for file in filelist:
		file_count += 1
		
		#Having more files really takes long
		if(file_count > 10000):
			break

		wavdata,duration = load_audio_file(file)

		if(not wavdata):
			print("Couldn't load file: " + file)
			continue

		seconds += duration
		splitdata = split_sequence(wavdata.raw_data,bufsize)
		for frame in splitdata:
	
			if(len(frame) == bufsize):
				prediction = detector.RunDetection(frame)

				if(prediction):
					false_predictions+= 1

	hours = seconds/3600.0
	print("Ran hours: " + str(hours))
	false_per_hour = false_predictions / hours
	return false_per_hour



if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--graph', type=str, default='./conv-conv.tflite', help='Model to use for identification.')
	parser.add_argument(
		'--labels', type=str, default='./labels.txt', help='Path to file containing labels.')
	parser.add_argument(
		'--cv_folder', type=str, default='./cv_corpus_v1/', help='Path to cv_corpus.')
	parser.add_argument(
		'--good_folder', type=str, default='./good_files/', help='Path to good files.')
	parser.add_argument(
		'--noise_folders', type=str, default='./demand/', help='Path to noise files.')
	parser.add_argument(
		'--bad_folders', type=str, default='', help='Path to additional bad folders seperated by comma.')
	parser.add_argument(
		'--libpath', type=str, default='../lib/linux/libnyumaya.so', help='Path to nyumaya_library')


	FLAGS, unparsed = parser.parse_known_args()


	sensitivities = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99]

	detector = AudioRecognition(FLAGS.libpath,FLAGS.graph,FLAGS.labels)
	addnoise = [False,True]
	results_clean = []
	results_noisy = []
	results_false = []
	print(FLAGS.graph + "\n")
	for noise in addnoise:

		for sensitivity in sensitivities:
			wrong_predictions, good_predictions,missed_predictions,samples = run_good_predictions(detector,FLAGS.good_folder,FLAGS.noise_folders,noise,sensitivity)

			result = {}
			result["sensitivity"] = sensitivity
			result["accuracy"] = 1-(missed_predictions+wrong_predictions)/samples
			if(noise):
				results_noisy.append(result)
			else:
				results_clean.append(result)
			print("Sens: " + str(result["sensitivity"]) + " " + "Accuracy: " + str( result["accuracy"] ) )
			
	for sensitivity in sensitivities:
		false_predictions = run_bad_predictions(detector,FLAGS.cv_folder,FLAGS.bad_folders,sensitivity)
		result = {}
		result["sensitivity"] = sensitivity
		result["false_predictions"] = false_predictions
		results_false.append(result)
		print("Sens: " + str(result["sensitivity"]) +  " False per hour " +  str(result["false_predictions"]))
	
	
	with open(os.path.dirname(FLAGS.graph) + "/result.txt", "a") as result_file:
		result_file.write(FLAGS.graph + "\n")

		result_file.write("Accuracy clean \n")
		for result in results_clean:
			result_file.write("Sens: " + str(result["sensitivity"]) + " " + "Accuracy: " + str( result["accuracy"] ) + "\n")

		result_file.write("\n\n")

		result_file.write("Accuracy noisy \n")
		for result in results_noisy:
			result_file.write("Sens: " + str(result["sensitivity"]) + " " + "Accuracy: " + str( result["accuracy"] ) + "\n")
		result_file.write("\n\n")


		result_file.write("False predictions per hour\n")
		for result in results_false:
			result_file.write("Sens: " + str(result["sensitivity"]) + " " + "False Per Hour: " + str( result["false_predictions"] ) + "\n")





