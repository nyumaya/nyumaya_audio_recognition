# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import time
import os
import argparse
import sys
import signal
import numpy as np
import logging


print("Loading Tensorflow")
from tensorflow import import_graph_def as tf_import_graph_def
from tensorflow import Session as tf_Session
from tensorflow import GraphDef as tf_GraphDef
from tensorflow import logging as tf_logging
print("Tensorflow loaded")

from record import AudiostreamSource
from record import RingBuffer
from feature_extraction import FeatureExtraction


#Try mute tensorflow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
logging.getLogger("tensorflow").setLevel(logging.ERROR)
tf_logging.set_verbosity(tf_logging.ERROR)

Running = True

sample_rate= 16000  # Samle Rate: 16000
window_len = 0.03   # Window Size: 30ms = 480 Samples 960 Bytes
frame_shift= 0.01   # Frame Shift: 10ms = 160 Samples 320 Bytes
warmup_steps = 40
melcount = 40 
recognition_threshold = 0.9
lower_frequency = 20 
higher_frequency = 8000
prediction_every = 20 #Number of mel steps between predictions
volume = (1.0/32768.0)*256.0 # Int to Float conversion included
# MFCC Window length = 1 second = 1000 Shifts


s = AudiostreamSource()

def signal_handler(sig, frame):
	print('Terminating')
	Running = False
	s.stop()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



def load_graph(filename):
	with open(filename, 'rb') as f:
		graph_def = tf_GraphDef()
		graph_def.ParseFromString(f.read())
		tf_import_graph_def(graph_def, name='')


def load_labels(filename):
	with open(filename,'r') as f:  
		return [line for line in f]



def label_stream(labels, graph, input_name, output_name, how_many_labels):

	labels_list = load_labels(labels)
	load_graph(graph)
   
	mel = FeatureExtraction(nfilt=melcount,ncep=40,lowerf=lower_frequency,
		upperf=higher_frequency,samprate=16000,wlen=window_len,nfft=512,datalen=480)

	with tf_Session() as sess:
		softmax_tensor = sess.graph.get_tensor_by_name(output_name) 
		np.set_printoptions(precision=2)

		mel_spectrogram = np.zeros((1,3920), dtype=np.float32) 

		#Run one time with dummy data to warm up
		predictions, = sess.run(softmax_tensor, {input_name: mel_spectrogram})

		s.start()
		i = 0
    
		print("Detection Started")
		position = 0
		while(Running):

			data = s.read(960,320)
			if(data):
				data = np.frombuffer(data, dtype=np.int16) # Volume
				mel_data = mel.frame_to_mel(data*volume)

				#TODO: Remove magic numbers
				#TODO: Predict only once
				#TODO: Average predictions

				#Copy new mel data
				mel_end   = 3920-(melcount*position)
				mel_start = 3920-(melcount*(position+1))
				mel_spectrogram[0,mel_start:mel_end] = mel_data[0:melcount]

				i = i+1
				position += 1
				#Eval every 200 ms, warmup for the first second
				if(i%prediction_every == 0 and i > warmup_steps):
					
					#start = time.time()
					predictions, = sess.run(softmax_tensor, {input_name: mel_spectrogram})

					# Sort to show labels in order of confidence
					top_k = predictions.argsort()[-how_many_labels:][::-1]
 
					for node_id in top_k:
						human_string = labels_list[node_id]
						score = predictions[node_id]
						if(score > recognition_threshold and node_id != 0 and node_id != 1):
							print('%s (score = %.5f)' % (human_string, score))


					mel_spectrogram = np.roll(mel_spectrogram, -melcount*prediction_every,1)
					position = 0

					#end = time.time()
					#print("Classification done in : " + str(end - start))
			else:
				time.sleep(0.1)



if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--graph', type=str,
		default='./models/marvin_hotword/conv-res-mini_frozen.pb', 
		help='Model to use for identification.')

	parser.add_argument(
		'--labels', type=str,
		default='./models/marvin_hotword/labels.txt',
		help='Path to file containing labels.')

	parser.add_argument('--input_name',
		type=str,
		default='fingerprint_input:0',
		help='Name of WAVE data input node in model.')

	parser.add_argument(
		'--output_name',
		type=str,
		default='labels_softmax:0',
		help='Name of node outputting a prediction in the model.')

	parser.add_argument(
		'--how_many_labels',
		type=int,
		default=1,
		help='Number of results to show.')

	FLAGS, unparsed = parser.parse_known_args()

	label_stream(FLAGS.labels, FLAGS.graph, FLAGS.input_name,FLAGS.output_name, FLAGS.how_many_labels)



