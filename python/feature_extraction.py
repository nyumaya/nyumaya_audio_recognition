import numpy, numpy.fft
import unittest
import math

numpy.set_printoptions(threshold=numpy.nan)
def mel(f):
	return 2595. * numpy.log10(1. + f / 700.)

def melinv(m):
	return 700. * (numpy.power(10., m / 2595.) - 1.)

class FeatureExtraction(object):
	def __init__(self, nfilt=40,lowerf=20, upperf=8000,
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
		dfreq = float(samprate) / float(nfft)
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

		fftarray = []
		for idx in range(number_of_frames):
			start = int(round(idx * self.shift))
			end = int(min(signal_len, start + self.datalen))
			frame = signal[start:end]
			framelen = len(frame)
			if framelen < self.datalen:
				frame = numpy.resize(frame,self.datalen)
				frame[framelen:] = 0
			fftarray.append(frame)

		windowed = fftarray * self.window
		spectrum = numpy.fft.rfft(windowed,n=self.nfft)
		autopower = numpy.abs(spectrum * numpy.conj(spectrum))

		lin = numpy.matmul(autopower,self.filters)
		mel = numpy.log(lin+1e-6)
		
		return mel.flatten()

