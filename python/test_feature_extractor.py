from __future__ import unicode_literals
from __future__ import division



from libnyumaya import FeatureExtractor
from feature_extraction import FeatureExtraction

from random import randint

import math
import numpy as np

def test_feature_extractor():

	signal = np.zeros(3600,dtype=np.int16)
 
	for i in range(3600):
		signal[i] = int(math.sin(i/100.0)*2000.0)


	lib_extractor = FeatureExtractor("../lib/linux/libnyumaya.so",nfft=512,melcount=40,sample_rate=16000,lowerf=20,upperf=8000,window_len=0.03,shift=0.01)
	python_extractor = FeatureExtraction(nfilt=40,lowerf=20,upperf=8000,samprate=16000,wlen=0.03,nfft=512,datalen=512)

	mel_lib    = lib_extractor.signal_to_mel(signal)
	mel_python = python_extractor.signal_to_mel(signal/32768.0)
	
	diff = mel_lib-mel_python
	
	print("Difference: " + str(sum(abs(diff))))

test_feature_extractor()
