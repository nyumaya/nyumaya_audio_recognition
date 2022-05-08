import pyaudio
from threading import Thread
from ringbuffer import RingBuffer

# Efficienly capture audio into a ringbuffer using arecord
# This will work on all systems where portaudio is working

# To minimize CPU usage large chunks are read from alsa
# The audio capture is running in its own thread
# Reading from the buffer is blocking


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







