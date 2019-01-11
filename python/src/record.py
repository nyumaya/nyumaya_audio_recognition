
import subprocess

from threading import Thread
from ringbuffer import RingBuffer

# Efficienly capture audio into a ringbuffer using arecord
# This will only work for linux based systems

# To minimize CPU usage large chunks are read from alsa
# The audio capture is running in its own thread
# Reading from the buffer is blocking


class AudiostreamSource(Thread):


	def __init__(self,sample_rate=16000,channels=1,audio_length=80):
		Thread.__init__(self)

		self.running = False
		self.input_device = 'default'
		self.bytes_per_sample=2
		self.sample_rate = sample_rate
		self.channels = channels
		self.audio_length = audio_length
		self.blocksize = int(((self.sample_rate) * (self.audio_length) / 1000) * self.channels * self.bytes_per_sample)

		self._cmd = [
			'arecord',
			'-q',
			'-t', 'raw',
			'-D', self.input_device,
			'-c', str(self.channels),
			'-f', 's16',
			'-r', str(self.sample_rate),
		]

		self._arecord = None
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
		self._arecord = subprocess.Popen(self._cmd, stdout=subprocess.PIPE)
		self.running = True
		while self._arecord and self.running:
			input_data = self._arecord.stdout.read(self.blocksize)
			if input_data:
				self.audio_buffer.write(input_data)

		#Shutdown record command
		if(self._arecord):
			self._arecord.kill()
			self._arecord = None




