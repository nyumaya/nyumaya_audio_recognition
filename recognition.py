#Nyumaya Audio Classifier

import numpy as np

print("Loading Tensorflow")
from tensorflow import import_graph_def as tf_import_graph_def
from tensorflow import Session as tf_Session
from tensorflow import GraphDef as tf_GraphDef
from tensorflow import logging as tf_logging
print("Tensorflow loaded")
from feature_extraction import FeatureExtraction
import logging

class Detector():


	def __init__(self,graph_path,label_path):
		self.graph_path = graph_path
		self.label_path = label_path

		self.sample_rate= 16000  # Samle Rate: 16000
		self.window_len = 0.03   # Window Size: 30ms = 480 Samples 960 Bytes
		self.frame_shift_ms= 0.01   # Frame Shift: 10ms = 160 Samples 320 Bytes
		self.melcount = 40 
		self.frame_shift = int(self.frame_shift_ms*self.sample_rate)
		self.bitsize = 2
		self.blocksize = 20
		self.recognition_threshold = 0.9
		self.lower_frequency = 20 
		self.higher_frequency = 8000
		self.prediction_every = 20 #Number of mel steps between predictions
		self.gain = 1.0
		self.detection_cooldown = 5
		self.cooldown = 0
		self.sensitivity = 0.5
		self.mel_spectrogram = np.zeros((1,self.melcount*98), dtype=np.float32) 
		self.mel = FeatureExtraction(nfilt=self.melcount,lowerf=self.lower_frequency,upperf=self.higher_frequency,
			samprate=self.sample_rate,wlen=self.window_len,nfft=512,datalen=512)

		self.input_name = "fingerprint_input:0"
		self.output_name = "labels_softmax:0"

		self.sess = tf_Session()

		self.labels_list = self._load_labels(label_path)
		self._load_graph(graph_path)

		self.last_frames = {}

		self.softmax_tensor = self.sess.graph.get_tensor_by_name(self.output_name) 
		self._warmup()


	def set_sensitivity(self,sensitivity):
		self.sensitivity = 1- sensitivity


	#Returns the number of bytes to pass to the recognizer
	def input_data_size(self):
		return self.blocksize*self.frame_shift*self.bitsize

	#Run a prediction on given frame encoded as 16kHz 16bit mono integer pcm samples
	def recognize(self,frame):
	
		if(not frame):
			return None

		if(self.cooldown > 0):
			self.cooldown -= 1

		volume = (1.0/32768.0)*self.gain # Int to Float conversion including volume

		data = np.frombuffer(frame, dtype=np.int16) 
		mel_data = self.mel.signal_to_mel(data*volume)
		mel_len = len(mel_data)

		mel_end   = (self.melcount*98)
		mel_start = (self.melcount*98)-(mel_len)
		self.mel_spectrogram[0,mel_start:mel_end] = mel_data[0:mel_len]

		predictions, = self.sess.run(self.softmax_tensor, {self.input_name: self.mel_spectrogram})
		result = self._smooth_detection(predictions)
		#result = self._hotword_detection(predictions)

		self.mel_spectrogram = np.roll(self.mel_spectrogram, -mel_len,1)
		return result


	#Just simple threshold and maximum of one prediction every n frames
	def _hotword_detection(self,predictions):
		prediction = predictions.argsort()[-1:][::-1][0]
		label = self.labels_list[prediction]
		score = predictions[prediction]


		if label == '_unknown_':
			return None

		if(score > 0.98 and self.cooldown == 0):
			self.cooldown = self.detection_cooldown
			return label
		else: 
			return None


	# Accumulate scores over longer timeframes. This can be useful for better detecting longer events like footsteps,
	# crying babies, acoustic scenes
	def _ongoing_detection(self,predictions):
		pass

	# Accumulate scores. Scores are decayed over time. A event is usally 1 second maximum 
	# so after one second of no activity score should be close to zero. 
	# Maximum one prediction every n frames.
	def _smooth_detection(self,predictions):
		
		for key in self.last_frames:
			if len(self.last_frames[key]) >= 5:
				#print(self.last_frames[key])
				self.last_frames[key].pop(0)

		how_many_labels = len(self.labels_list)
		top_k = predictions.argsort()[-how_many_labels:][::-1]

		for node_id in top_k:
			label_string = self.labels_list[node_id]
			score = predictions[node_id]

			# Init Dict
			if(not label_string in self.last_frames):
				self.last_frames[label_string] = []

			if(label_string != "_unknown_"):
				if(score > 0.85 + 0.149999*self.sensitivity):
					self.last_frames[label_string].append(score)
				else: 
					self.last_frames[label_string].append(0)


		#Check if the biggest score in last frames is over the threshold
		biggest_score = 0
		biggest_score_key = None
		for key in self.last_frames:
			score = sum(self.last_frames[key])
			
			if(score > biggest_score):
				biggest_score  = score
				biggest_score_key = key
		
		if(biggest_score >  (0.9 + 2.0*self.sensitivity) and self.cooldown == 0):
			self.cooldown = self.detection_cooldown
			return biggest_score_key
		return None


	def _warmup(self):
		predictions, = self.sess.run(self.softmax_tensor, {self.input_name: self.mel_spectrogram})

	def _load_graph(self,filename):
		with open(filename, 'rb') as f:
			graph_def = tf_GraphDef()
			graph_def.ParseFromString(f.read())
			tf_import_graph_def(graph_def, name='')


	def _load_labels(self,filename):
		with open(filename,'r') as f:  
			return [line.strip() for line in f]


