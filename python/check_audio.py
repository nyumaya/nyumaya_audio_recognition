import time
import os
import argparse
import sys
import datetime
import struct

from record import AudiostreamSource
from record import RingBuffer


audio_stream = AudiostreamSource()

mean      = 0
avg_level = 0
avg_sum   = 0
max_level = 0

bufsize = 256

frame_sum = 0
frame_len = 0

clipcount = 0

audio_stream.start()
print("Start speaking now!")
for i in range(2000):
		frame = audio_stream.read(bufsize,bufsize)
		if(not frame):
			time.sleep(0.01)
			continue
			
		#Convert to int array
		count = len(frame)/2
		frame = struct.unpack('h'*count, frame)
		
		frame_sum = sum(frame)
		frame_len += len(frame)
		for val in frame:
			avg_sum += abs(val)
			if abs(val) > max_level:
				max_level = abs(val)
			if abs(val) == 32768:
				clipcount += 1

mean = frame_sum / frame_len
avg_level = avg_sum / frame_len

possible_gain = 32768 / max_level

if(max_level == 0):
	"I'm getting no signal at all!"
	sys.exit(0)

print("Max Level: " + str(max_level))
print("Avg Level: " + str(avg_level))
print("Clippcount: " + str(clipcount) + " of " + str(frame_len) + " frames")
print("If Clippcount is more than a few frames you have to reduce your volume")

print("Mean Level: " + str(mean))

print("Possible Gain: " + str(possible_gain))


if(avg_level/(abs(mean)+1) > 10):
	print("Your Mic has no DC-offset")
else:
	print("Your Mic has a DC-offset: Don't worry it will be removed automagically")
	

audio_stream.stop()





