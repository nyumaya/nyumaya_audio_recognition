
from libnyumaya import AudioRecognition

#TODO: Optimize: More error handling

def command_starts_with_history(cmd,history):
	index = 0

	while index < len(history) and index < len(cmd):
		if(history[index] != cmd[index]):
			return -1
		index += 1
		
	return index

class MultiDetector():


	def __init__(self,libpath,timeout = 40):
		self.current_index = 0
		self.number_detectors = 0
		self.countdown = 0
		self.timeout = timeout
		self.detector = None
		self.commands  = []
		self.libpath = libpath
		self.history=[]
		self.last_frames = []
		self.max_last_frames = 5
		self.detector = AudioRecognition(self.libpath)
		self.keyword_map = {}

	#Given the current history which words are we checking for?
	def get_possible_words(self,history):
		words = []
		for cmd in self.commands:
			index = command_starts_with_history(cmd['command'],history)

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



	def UpdateLastFrames(self,frame):
		self.last_frames.append(frame)
		if len(self.last_frames) > self.max_last_frames:
			self.last_frames.pop(0)

	def add_command(self,command,callback_function):
		if(len(command.split(",")) == 0):
			print("No valid command")
			return

		self.commands.append({'command':command.split(","), 'function': callback_function })
		self.update_word_and_detector()

	def add_word(self,graph,name,sensitivity):
		keywordId = self.detector.addModel(graph,sensitivity)
		self.keyword_map[keywordId]=name

	def add_reset_history_callback(self,callback_function):
		self.history_callback = callback_function

	def add_detected_callback(self,callback_function):
		self.detected_callback = callback_function

	def GetInputDataSize(self):
		return self.detector.getInputDataSize()

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
				if(self.history_callback):
					self.history_callback()


	def update_word_and_detector(self):
		self.possible_words = self.get_possible_words(self.history)
		#Set possible words active
		#Set impossible words inactive
		print(self.possible_words)
		for id in self.keyword_map:
			key = self.keyword_map[id]
			if(key in self.possible_words):
				self.detector.setActive(id,True)
			else:
				self.detector.setActive(id,False)



	def run_frame(self,frame,update_frames=True):

		if(update_frames):
			self.UpdateLastFrames(frame)

		self.check_timeout()

		prediction = self.detector.runDetection(frame)
		if(prediction):
			label = self.keyword_map[prediction]
			if(label in self.possible_words):
				print("Got prediction: " + label)
				self.countdown = self.timeout
				self.history.append(label)
				result = self.maby_execute()
				self.update_word_and_detector()

				if(self.detected_callback):
					self.detected_callback()

				#Command hasn't finished so run last frames in next detectors
				if(not result):
					self.run_last_frames()

	def run_last_frames(self):
		for frame in self.last_frames:
			self.run_frame(frame,update_frames=False)

	def print_commands(self):
		for cmd in self.commands:
			print(cmd)











