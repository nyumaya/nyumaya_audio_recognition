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

from libnyumaya import AudioRecognition,FeatureExtractor
from random import randint, seed


samplerate=16000


def load_audio_file(filename,resize=False):
	sound = None
	try:
		if filename.endswith('.mp3') or filename.endswith('.MP3'):
			sound = AudioSegment.from_mp3(filename)
		elif filename.endswith('.wav') or filename.endswith('.WAV'):
			sound = AudioSegment.from_wav(filename)
		elif filename.endswith('.ogg'):
			sound = AudioSegment.from_ogg(filename)
		elif filename.endswith('.flac'):
			sound = AudioSegment.from_file(filename, "flac")
		elif filename.endswith('.3gp'):
			sound = AudioSegment.from_file(filename, "3gp")
		elif filename.endswith('.3g'):
			sound = AudioSegment.from_file(filename, "3gp")

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


def run_good_predictions(detector,extractor,good_folders,noise_folders,add_noise,sensitivity,use_all_files):

	detector.SetSensitivity(sensitivity)
	
	bufsize = detector.GetInputDataSize() * 2

	seed(1234)
	
	good_predictions = 0
	wrong_predictions = 0
	missed_predictions = 0
	sample_number = 0
	
	testing_set = []

	good_folders = good_folders.split(',')
	for folder in good_folders:
		testing_set = testing_set + include_good_folder(folder,detector.labels_list,not use_all_files)

	if(len(testing_set) == 0):
		print("No testdata found")
		return None, None, None, None

	print("Number of positive Samples: " + str(len(testing_set))) 
	noise_list = []
	
	if(add_noise):
		noise_folder_list = noise_folders.split(',')
		for noise_folder in noise_folder_list:
			if(os.path.exists(noise_folder)):
				noise_list += include_random_folder(noise_folder)

	
		if(len(noise_list) == 0):
			print("No noise data available")
			return None, None, None, None
			
		
	for datapoint in testing_set:

		current_label = datapoint['label']

		wavdata,duration = load_audio_file(datapoint['file'])

		if(not wavdata):
			continue
			
		one_second_silence = AudioSegment.silent(duration=1000)
		wavdata += one_second_silence
		
		if(add_noise):
			bg_noise_file = get_random_file(noise_list)
			noise,noise_duration = load_audio_file(bg_noise_file)

			if(not noise):
				print("Couldn't load: " + bg_noise_file)
			else:
				wavdata = wavdata.overlay(noise, gain_during_overlay=0)

		wavdata = wavdata.get_array_of_samples().tostring()
		splitdata = split_sequence(wavdata,bufsize)

		sample_number += 1
	
		has_detected_something = False
		
		for frame in splitdata:
	
			features = extractor.signal_to_mel(frame)
			prediction = detector.RunDetection(features)

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


def file_as_bytes(file):
	with file:
		return file.read()


def md5sum_of_file(full_path):
	return hashlib.md5(file_as_bytes(open(full_path, 'rb'))).hexdigest()

def split_sequence(a,seg_length):
	return [a[x:x+seg_length] for x in range(0,len(a),seg_length)]


def get_random_file(file_list):
	filelen = len(file_list)
	index  = randint(0,filelen-1)
	return file_list[index]

def run_bad_predictions(detector,extractor,cv_folder,bad_folders,sensitivity):

	detector.SetSensitivity(sensitivity)

	bufsize = detector.GetInputDataSize() * 2

	seconds = 0
	false_predictions = 0
	bad_predictions = 0
	file_count = 0
	filelist=[]
	if(cv_folder):
		filelist = filelist + get_cv_list(detector.labels_list,cv_folder)
	
	bad_folders = bad_folders.split(',')
	for folder in bad_folders:
		filelist = filelist + include_random_folder(folder)

	if(len(filelist) == 0):
		return None

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
				
		wavdata = wavdata.get_array_of_samples().tostring()
		splitdata = split_sequence(wavdata,bufsize)

		for frame in splitdata:
	
			if(len(frame) == bufsize):
			
				features = extractor.signal_to_mel(frame)
				prediction = detector.RunDetection(features)

				if(prediction):
					false_predictions+= 1


	hours = seconds/3600.0
	print("Ran hours: " + str(hours))
	false_per_hour = false_predictions / hours
	return false_per_hour



if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--graph', type=str, default='./models/Hotword/marvin_small_3.0.tflite', help='Model to use for identification.')
	parser.add_argument(
		'--labels', type=str, default='./labels.txt', help='Path to file containing labels.')
	parser.add_argument(
		'--cv_folder', type=str, default=None, help='Path to cv_corpus.')
	parser.add_argument(
		'--good_folder', type=str, default='./good_files/', help='Path to good files.')
	parser.add_argument(
		'--noise_folders', type=str, default='./demand/', help='Path to noise files.')
	parser.add_argument(
		'--bad_folders', type=str, default='', help='Path to additional bad folders seperated by comma.')
	parser.add_argument(
		'--libpath', type=str, default='../lib/linux/libnyumaya.so', help='Path to nyumaya_library')

	parser.add_argument(
		'--use_all_files',  action='store_true', help='Wether to use all files or only files which have a hash matching test files')
		
	FLAGS, unparsed = parser.parse_known_args()

	print("include_only_test_files: " + str(FLAGS.use_all_files))

	sensitivities = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

	detector = AudioRecognition(FLAGS.libpath,FLAGS.graph,FLAGS.labels)
	extractor = FeatureExtractor(FLAGS.libpath)
		
	addnoise = [False,True]
	results_clean = []
	results_noisy = []
	results_false = []
	print(FLAGS.graph + "\n")
	for noise in addnoise:

		for sensitivity in sensitivities:
			wrong_predictions, good_predictions,missed_predictions,samples = run_good_predictions(detector,extractor,FLAGS.good_folder,FLAGS.noise_folders,noise,sensitivity,FLAGS.use_all_files)

			if(wrong_predictions is not None):
				result = {}
				result["sensitivity"] = sensitivity
				result["accuracy"] = 1-(missed_predictions+wrong_predictions)/samples
				if(noise):
					results_noisy.append(result)
				else:
					results_clean.append(result)
				print("Sens: " + str(result["sensitivity"]) + " " + "Accuracy: " + str( result["accuracy"] ) )
			
	for sensitivity in sensitivities:
		false_predictions = run_bad_predictions(detector,extractor,FLAGS.cv_folder,FLAGS.bad_folders,sensitivity)
		if(false_predictions is not None):
			result = {}
			result["sensitivity"] = sensitivity
			result["false_predictions"] = false_predictions
			results_false.append(result)
			print("Sens: " + str(result["sensitivity"]) +  " False per hour " +  str(result["false_predictions"]))
		
		
	result_name = os.path.splitext(os.path.basename(FLAGS.graph))[0]  + "_" + "result.txt"
	with open(os.path.dirname(FLAGS.graph) + "/" + result_name, "a") as result_file:
		result_file.write(FLAGS.graph + "\n")
		result_file.write(md5sum_of_file(FLAGS.graph) + "\n\n")
		result_file.write("Accuracy clean \n")
		
		area_clean = 0
		i=0
		for result in results_clean:
			result_file.write("Sens: " + str(result["sensitivity"]) + " " + "Accuracy: " + str( result["accuracy"] ) + "\n")
			#area_clean += (1-result["accuracy"]) * results_false[i]["false_predictions"]
			i+=1 
		print("Area clean:" + str(area_clean))
			
		result_file.write("\n\n")

		result_file.write("Accuracy noisy \n")
		for result in results_noisy:
			result_file.write("Sens: " + str(result["sensitivity"]) + " " + "Accuracy: " + str( result["accuracy"] ) + "\n")
		result_file.write("\n\n")


		result_file.write("False predictions per hour\n")
		for result in results_false:
			result_file.write("Sens: " + str(result["sensitivity"]) + " " + "False Per Hour: " + str( result["false_predictions"] ) + "\n")





