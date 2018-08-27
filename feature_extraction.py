import numpy, numpy.fft
import unittest
import math


def mel(f):
	return 2595. * numpy.log10(1. + f / 700.)

def melinv(m):
	return 700. * (numpy.power(10., m / 2595.) - 1.)

class FeatureExtraction(object):
	def __init__(self, nfilt=17,lowerf=20, upperf=4000,
		samprate=16000, wlen=0.03,nfft=512,datalen=512,shift=0.01):

		# Store parameters
		self.lowerf = lowerf
		self.upperf = upperf
		self.nfft = nfft
		self.nfilt = nfilt
		self.datalen = datalen
		self.shift = samprate*shift
		self.window = numpy.hanning(datalen)
		# Build mel filter matrix

		self.filters = numpy.zeros((int(nfft/2+1),nfilt), 'd')
		dfreq = float(samprate) / nfft
		if upperf > samprate/2:
			raise(Exception,"Upper frequency %f exceeds Nyquist %f" % (upperf, samprate/2))

		melmax = mel(upperf)
		melmin = mel(lowerf)
		dmelbw = (melmax - melmin) / (nfilt + 1)
		# Filter edges, in Hz
		filt_edge = melinv(melmin + dmelbw * numpy.arange(nfilt + 2, dtype='d'))

		for whichfilt in range(0, nfilt):
			# Filter triangles, in DFT points
			leftfr = round(filt_edge[whichfilt] / dfreq)
			centerfr = round(filt_edge[whichfilt + 1] / dfreq)
			rightfr = round(filt_edge[whichfilt + 2] / dfreq)
			# For some reason this is calculated in Hz, though I think
			# it doesn't really matter
			fwidth = (rightfr - leftfr) * dfreq
			height = 2. / fwidth

			if centerfr != leftfr:
				leftslope = height / (centerfr - leftfr)
			else:
				leftslope = 0
			freq = leftfr + 1
			while freq < centerfr:
				self.filters[int(freq),whichfilt] = (freq - leftfr) * leftslope
				freq = freq + 1
			if freq == centerfr: # This is always true
				self.filters[int(freq),whichfilt] = height
				freq = freq + 1
			if centerfr != rightfr:
				rightslope = height / (centerfr - rightfr)
			while freq < rightfr:
				self.filters[int(freq),whichfilt] = (freq - rightfr) * rightslope
				freq = freq + 1



	def signal_to_mel(self,signal):
 
		signal_len = len(signal)
		number_of_frames = int(signal_len / self.shift)

		mels = numpy.empty(int(number_of_frames*self.nfilt), dtype=numpy.float32) 
		frameindex = 0
		fftarray = []
		for _ in range(number_of_frames):
			start = int(round(frameindex * self.shift))
			end = int(min(signal_len, start + self.datalen))
			frame = signal[start:end]
  
			if len(frame) < self.datalen:
				frame = numpy.resize(frame,self.datalen)
				frame[self.datalen:] = 0
			fftarray.append(frame)

			frameindex +=1

		windowed = fftarray * self.window            
		spectrum = numpy.fft.rfft(windowed,n=self.nfft)                      #/ fft_size
		autopower = numpy.abs(spectrum * numpy.conj(spectrum))              # find the autopower spectrum

		result = numpy.empty((number_of_frames,int(self.nfft/2+1)), dtype=numpy.float32)        # space to hold the result
		result[:,:] = autopower[:,:self.nfft]  

		lin = numpy.dot(result,self.filters)

		mel = numpy.log(lin+1e-6)

		return mel.flatten()




    
