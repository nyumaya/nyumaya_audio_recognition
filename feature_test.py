from feature_extraction import  FeatureExtraction

import cProfile
import numpy as np


   
mel = FeatureExtraction(nfilt=40,ncep=40,lowerf=20,upperf=8000,samprate=16000,wlen=0.03,nfft=512,datalen=480)
data = np.zeros(480)
pr = cProfile.Profile()
pr.enable()
for i in range (10000):
	mel_data = mel.signal_to_mel(data) 
 
pr.disable()
 
pr.print_stats(sort='time')
