#!/usr/bin/python

import os
import subprocess
from threading import Thread, Lock
import time
import unittest
import sys

import pyaudio

# Efficienly capture audio into a ringbuffer using arecord
# This will only work for linux based systems

# To minimize CPU usage large chunks are read from alsa
# The audio capture is running in its own thread
# Reading from the buffer is blocking



class RingBuffer():

	def __init__(self, buffer_size = 32768):
		self.read_pos=0
		self.write_pos=0
		self.buffer_size = buffer_size
		self.buffer = bytearray(self.buffer_size)
		self.lock = Lock()

	def write(self,data):

		if not data:
			return

		datalen = len(data)

		if(datalen > self.buffer_size):
			print("Trying to write huge buffer !!!!!!!")
			return
			
		self.lock.acquire()

		# TODO: Check for buffer overrun
		# Case A: Read pos was smaller than write pos
		# Case B: Read pos was bigger than write pos
		self.write_pos_old = self.write_pos
		# Data fitting into remaining buffer
		if((self.write_pos + datalen) <= self.buffer_size):
			self.buffer[self.write_pos:self.write_pos+datalen] = data[:]
			self.write_pos += datalen
			
		else:

			#Write first part into buffer
			first_len = self.buffer_size - self.write_pos	
			self.buffer[self.write_pos:self.write_pos+first_len] = data[0:first_len]

			#Write second part wrapped around
			second_len = datalen - first_len
			self.buffer[0:second_len] = data[first_len:first_len+datalen]
			self.write_pos = second_len

		self.lock.release()

	def get_buffer_size(self):
		return self.buffer_size

	def can_read_n_bytes(self,n):
		if(self.read_pos <= self.write_pos):
			return n <= (self.write_pos - self.read_pos)
		else:
			avail = (self.buffer_size - self.read_pos) + self.write_pos
			return n <= avail


	def read(self,blocksize,advance):


		self.lock.acquire()

		# Not enough data for reading
		if not self.can_read_n_bytes(blocksize):
			self.lock.release()
			return None

		# Can read in one block
		if((self.read_pos + blocksize) <= self.buffer_size):
			data = self.buffer[self.read_pos:self.read_pos+blocksize]
			self.read_pos += advance
			if(self.read_pos > self.buffer_size):
				self.read_pos %= self.buffer_size

			self.lock.release()
			return data

		# Need to concatenate	
		else:

			first_part = self.buffer[self.read_pos:self.buffer_size]
			first_len = (self.buffer_size - self.read_pos)
			second_len = blocksize - first_len
			second_part = self.buffer[0:second_len]
			self.read_pos += advance 
			if(self.read_pos > self.buffer_size):
				self.read_pos %= self.buffer_size

			data = first_part + second_part

			self.lock.release()
			return data

		

class AudiostreamSource(Thread):


	def __init__(self,sample_rate=16000,channels=1,audio_length=80):
		Thread.__init__(self)
		
		self.p = pyaudio.PyAudio()

		self.running = False
		self.input_device = 'default'
		self.bytes_per_sample=2
		self.sample_rate = sample_rate
		self.channels = channels
		self.audio_length = audio_length
		self.blocksize = int(((self.sample_rate) * (self.audio_length) / 1000) * self.channels * self.bytes_per_sample)


		self.audio_buffer = RingBuffer()

	def print_info(self):
		print("Blocksize: "   + str(self.blocksize))
		print("Sample Rate: " + str(self.sample_rate))
		print("Channels: "    + str(self.channels))

	# Get len number of samples
	# Blocks until samples is available
	def read(self,chunk_size,advance):
		return self.audio_buffer.read(chunk_size,advance)

	def stop(self):
		self.running = False

	def run(self):
		self.mic_stream = self.p.open(format=pyaudio.paInt16,
			channels=self.channels,
			rate=self.sample_rate,
			input=True,
			frames_per_buffer=self.blocksize)
			
		self.running = True
		while self.mic_stream and self.running:
			input_data = self.mic_stream.read(self.blocksize)
			if input_data:
				self.audio_buffer.write(input_data)

		#Shutdown record command
		if(self.mic_stream):
			self.mic_stream.close()
			self.mic_stream = None



class TestRingBuffer(unittest.TestCase):

	def test_can_read(self):
		r = RingBuffer()
		self.assertEqual(r.can_read_n_bytes(1),False)
		self.assertEqual(r.can_read_n_bytes(0),True)

	def test_read_write(self):
		r = RingBuffer()
		x = b"Bytes objects are immutable sequences of single bytes"
		r.write(x)
		self.assertEqual(r.can_read_n_bytes(len(x)),True)
		self.assertEqual(r.can_read_n_bytes(len(x)+1),False)

		xread =r.read(len(x),0)
		self.assertEqual(x,xread)

	def test_advance(self):
		r = RingBuffer(1024)
		x = b"ABCDEFGHIJKlMNOPQRSTUVWXYZ"
		y = b"BCDEFGHIJKlMNOPQRSTUVWXYZ"
		r.write(x)
		x1 = r.read(26,0)
		self.assertEqual(x,x1)

		x2 = r.read(26,1)
		self.assertEqual(x,x2)

		y1 = r.read(25,1)
		self.assertEqual(y,y1)

	def test_full_read_write(self):
		r = RingBuffer()
		s = r.get_buffer_size()
		data = bytearray(s)
		r.write(data)
		data_r = r.read(s,0)
		self.assertEqual(data,data_r)

	def test_overlap_read_write(self):
		r = RingBuffer(10)
		self.assertEqual(r.get_buffer_size(),10)
		x = b"ABCDEFGH"
		y = b"IJKlMNOP"
		r.write(x)
		datax = r.read(8,8)
		self.assertEqual(datax,x)

		r.write(y)
		datay = r.read(8,8)
		self.assertEqual(datay,y)



if __name__ == "__main__":
	unittest.main()
	source = AudiostreamSource()
	source.print_info()
	source.start()
	while True:
		time.sleep(1)




