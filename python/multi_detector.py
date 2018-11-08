import time
import os
import argparse
import sys
import datetime

from libnyumaya import AudioRecognition
from ringbuffer import RingBuffer

#TODO: Optimize: When running multiple detectors feature extraction has to be done only once

#TODO: Optimize: When changing detectors rerun the last 500ms in the new detector to better
#                recorgnize commands without a pause

#TODO: Optimize: More error handling

#TODO: Optimize: Creating detector and word list can be reduced


class MultiDetector():


	def __init__(self,libpath,timeout = 20):
		self.current_index = 0
		self.number_detectors = 0
		self.countdown = 0
		self.timeout = timeout
		self.detectors = []
		self.commands  = []
		self.libpath = libpath
		self.history=[]
		
	def get_possible_words(self,history):
		
		words = []
		for cmd in self.commands:
			index = self.command_starts_with_history(cmd['command'],history)
			if(index >=0):
	
				cmd = cmd['command'][index]
				if(not cmd in words):
					words.append(cmd)
		return words

	def get_detectors_for_words(self,words):
		detectors = []
		for detector in self.detectors:
			for word in words:
				if(word in detector.labels_list):
					if(not detector in detectors):
						detectors.append(detector)
		return detectors


	def command_starts_with_history(self,cmd,history):
		index = 0

		while index < len(history) and index < len(cmd):
			if(history[index] != cmd[index]):
				return -1
			index += 1
			
		return index

	def add_command(self,command,callback_function):
		
		if(len(command.split(",")) == 0):
			print("No valid command")
			return 

		self.commands.append({'command':command.split(","), 'function': callback_function })

	def add_detector(self,graph,labels,sensitivity):
		detector = AudioRecognition(self.libpath,graph,labels)
		detector.SetSensitivity(sensitivity)
		self.detectors.append(detector)

	def GetInputDataSize(self):
		return self.detectors[0].GetInputDataSize()

	def maby_execute(self):
		for cmd in self.commands:
			if(cmd['command'] == self.history):
				cmd['function']()
				self.history = []
				self.countdown = 0
				
	def check_timeout(self):

		if(self.countdown > 0):
			self.countdown -= 1
			if(self.countdown == 0):
				self.history = []
				print("Reset History")

	def run_frame(self,frame):
		possible_words = self.get_possible_words(self.history)
		current_detectors = self.get_detectors_for_words(possible_words)
		
		self.check_timeout()
		
		for detector in current_detectors:
			prediction = detector.RunDetection(frame)
			if(prediction):
				label = detector.GetPredictionLabel(prediction)
				if(label in possible_words):
					print("Got prediction: " + label)
					self.countdown = self.timeout
					self.history.append(label)
					self.maby_execute()

	def print_commands(self):
		for cmd in self.commands:
			print(cmd)











