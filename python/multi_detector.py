import time
import os
import argparse
import sys
import datetime

from libnyumaya import AudioRecognition
from ringbuffer import RingBuffer

#TODO: Optimize: When running multiple detectors feature extraction has to be done only once

#TODO: Optimize: More error handling


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
		self.last_frames = []
		self.max_last_frames = 5
		
	def get_possible_words(self,history):
		
		words = []
		for cmd in self.commands:
			index = self.command_starts_with_history(cmd['command'],history)
			
			if(index >= len(cmd['command'])):
				print ("Error index out of range:")
				print ("Command: " + str(cmd))
				print ("Index: " + str(index))
				print ("History: " + str(history))
				return []
				
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

	def SetGain(self,value):
		for detector in self.detectors:
			detector.SetGain(value)


	def RemoveDC(self,value):
		for detector in self.detectors:
			detector.RemoveDC(value)

	def UpdateLastFrames(self,frame):
		self.last_frames.append(frame)
		if len(self.last_frames) > self.max_last_frames:
			self.last_frames.pop(0)

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
		self.update_word_and_detector()

	def add_detector(self,graph,labels,sensitivity):
		detector = AudioRecognition(self.libpath,graph,labels)
		detector.SetSensitivity(sensitivity)
		self.detectors.append(detector)

	def GetInputDataSize(self):
		return self.detectors[0].GetInputDataSize()

	def maby_execute(self):
		executed_cmd = False
		for cmd in self.commands:
			if(cmd['command'] == self.history):
				cmd['function']()
				self.history = []
				self.countdown = 0
				self.last_frames = []
				executed_cmd =  True
			
		return executed_cmd
			
	def check_timeout(self):

		if(self.countdown > 0):
			self.countdown -= 1
			if(self.countdown == 0):
				self.history = []
				self.update_word_and_detector()
				print("Reset History")

	def update_word_and_detector(self):
		self.possible_words = self.get_possible_words(self.history)
		self.current_detectors = self.get_detectors_for_words(self.possible_words)

	def run_frame(self,frame,update_frames=True):

		if(update_frames):
			self.UpdateLastFrames(frame)
			
		self.check_timeout()
		
		for detector in self.current_detectors:
			prediction = detector.RunDetection(frame)
			if(prediction):
				label = detector.GetPredictionLabel(prediction)
				if(label in self.possible_words):
					print("Got prediction: " + label)
					self.countdown = self.timeout
					self.history.append(label)
					result = self.maby_execute()
					self.update_word_and_detector()
					
					#Command hasn't finished so run last frames in next detectors
					if(not result):
						self.run_last_frames()
	
	def run_last_frames(self):
		for frame in self.last_frames:
			self.run_frame(frame,update_frames=False)

	def print_commands(self):
		for cmd in self.commands:
			print(cmd)











