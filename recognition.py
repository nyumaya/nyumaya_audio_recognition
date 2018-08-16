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
r"""Runs a trained audio graph against a WAVE file and reports the results.

The model, labels and .wav file specified in the arguments will be loaded, and
then the predictions from running the model against the audio data will be
printed to the console. This is a useful script for sanity checking trained
models, and as an example of how to use an audio model from Python.

Here's an example of running it:

python tensorflow/examples/speech_commands/label_wav.py \
--graph=/tmp/my_frozen_graph.pb \
--labels=/tmp/speech_commands_train/conv_labels.txt \
--wav=/tmp/speech_dataset/left/a5d485dc_nohash_0.wav

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import numpy as np
import tensorflow as tf
from record import AudiostreamSource
from record import RingBuffer

import time
import os
from mfcc import MFCC
import wave


s = AudiostreamSource()

Running = True
FLAGS = None

# Window Size: 30ms = 480 Samples 960 Bytes
# Frame Shift: 10ms = 160 Samples 320 Bytes
# Samle Rate: 16000
# MFCC Window length = 1 second = 1000 Shifts

def shift_one(xs):
    e = np.empty_like(xs)
    e[1:] = xs[:-1]
    return e

def load_graph(filename):
  """Unpersists graph from file as default graph."""
  with tf.gfile.FastGFile(filename, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')


def load_labels(filename):
  """Read in labels, one label per line."""
  return [line for line in tf.gfile.GFile(filename)]



def label_stream(labels, graph, input_name, output_name, how_many_labels):
  """Loads the model and labels, and runs the inference to print predictions."""

  if not labels or not tf.gfile.Exists(labels):
    tf.logging.fatal('Labels file does not exist %s', labels)

  if not graph or not tf.gfile.Exists(graph):
    tf.logging.fatal('Graph file does not exist %s', graph)

  labels_list = load_labels(labels)
  load_graph(graph)
   
  mel = MFCC(nfilt=40,ncep=40,lowerf=20,upperf=8000,samprate=16000,wlen=0.03,nfft=512,datalen=480)


  with tf.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name(output_name) 
    np.set_printoptions(precision=2)

    #Run one time with dummy data
    mel_spectrogram = np.zeros((1,40*98), dtype=np.float32) 

    predictions, = sess.run(softmax_tensor, {input_name: mel_spectrogram})
    s.start()
    i = 0
    
    print("Detection Started")

    while(Running):

      if (i == 100000):
        break
 

      data = s.read(960,320)
      if(data):
        data = np.frombuffer(data, dtype=np.int16) # Volume
        mel_data = mel.frame_to_mel(data/1024.0)     
        mel_spectrogram = np.roll(mel_spectrogram, -40,1)
        mel_spectrogram[0,3880:3920] = mel_data[0:40]

        #TODO: We can roll 30 times less if we just roll on prediction
        #TODO: Predict only once
        #TODO: Average predictions


        i = i+1

	#Eval every 100 ms, warmup for the first second
        if(i%10 ==0 and i > 100):
          #start = time.time()
          predictions, = sess.run(softmax_tensor, {input_name: mel_spectrogram})

          # Sort to show labels in order of confidence
          top_k = predictions.argsort()[-how_many_labels:][::-1]
 
          for node_id in top_k:
            human_string = labels_list[node_id]
            score = predictions[node_id]
            if(score > 0.7 and node_id != 0 and node_id != 1):
                print('%s (score = %.5f)' % (human_string, score))
          #end = time.time()
          #print("Classification done in : " + str(end - start))
      else:
        time.sleep(0.1)





def main(_):

 label_stream(FLAGS.labels, FLAGS.graph, FLAGS.input_name,FLAGS.output_name, FLAGS.how_many_labels)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument(
      '--graph', type=str, default='./conv-res-mini-narrow_frozen.pb', help='Model to use for identification.')
  parser.add_argument(
      '--labels', type=str, default='./conv_labels.txt', help='Path to file containing labels.')
  parser.add_argument(
      '--input_name',
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
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
