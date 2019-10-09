
from ctypes import *

import sys

def _load_labels(filename):
	with open(filename,'r') as f:
		return [line.strip() for line in f]


class AudioRecognition(object):

	lib = None
	obj = None

	def __init__(self,libpath,modelpath,label_path=None):

		if (not AudioRecognition.lib):
			AudioRecognition.lib = cdll.LoadLibrary(libpath)

			AudioRecognition.lib.createAudioRecognition.argtypes = None
			AudioRecognition.lib.createAudioRecognition.restype = c_void_p

			AudioRecognition.lib.getVersionString.argtypes = [c_void_p]
			AudioRecognition.lib.getVersionString.restype = c_char_p

			AudioRecognition.lib.getInputDataSize.argtypes = [c_void_p]
			AudioRecognition.lib.getInputDataSize.restype = c_size_t

			AudioRecognition.lib.setSensitivity.argtypes = [c_void_p,c_float]
			AudioRecognition.lib.setSensitivity.restype = None

			AudioRecognition.lib.runDetection.argtypes = [c_void_p, POINTER(c_uint8),c_int]
			AudioRecognition.lib.runDetection.restype = c_int

			AudioRecognition.lib.runRawDetection.argtypes = [c_void_p, POINTER(c_uint8),c_int]
			AudioRecognition.lib.runRawDetection.restype =  POINTER(c_uint8)

			AudioRecognition.lib.openModel.argtypes = [c_void_p, c_char_p]
			AudioRecognition.lib.openModel.restype = c_int

			AudioRecognition.lib.loadModelFromBuffer.argtypes = [c_void_p, POINTER(c_char_p),c_int]
			AudioRecognition.lib.loadModelFromBuffer.restype =  c_int

			AudioRecognition.lib.deleteAudioRecognition.argtypes = [c_void_p]
			AudioRecognition.lib.deleteAudioRecognition.restype =  None


		self.obj=AudioRecognition.lib.createAudioRecognition()

		self.CheckVersion()

		self.OpenModel(modelpath.encode('ascii'))

		if(label_path):
			self.labels_list = _load_labels(label_path)

	def __del__(self):
		AudioRecognition.lib.deleteAudioRecognition(self.obj)

	def CheckVersion(self):

		major = None
		minor = None
		rev = None

		if sys.version_info[0] < 3:
			major,minor,rev= self.GetVersionString().split('.')
		else:
			version_string =  self.GetVersionString()[2:]
			version_string = version_string[:-1]
			major,minor,rev= version_string.split('.')

		if major != "0" and minor != "3" :
				print("Your library version is not compatible with this API")

	def OpenModel(self,path):
		AudioRecognition.lib.openModel(self.obj,path)

	def RunDetection(self,data):
		datalen = int(len(data))
		pcm = c_uint8 * datalen
		pcmdata = pcm.from_buffer_copy(data)
		prediction = AudioRecognition.lib.runDetection(self.obj,pcmdata,datalen)
		return prediction


	def RunRawDetection(self,data):
		datalen = int(len(data))
		pcm = c_uint8 * datalen
		pcmdata = pcm.from_buffer_copy(data)
		prediction = AudioRecognition.lib.runRawDetection(self.obj,pcmdata,datalen)
		re = [prediction[i] for i in range(2)]
		return re


	def GetPredictionLabel(self,index):
		if(self.labels_list):
			return self.labels_list[index]

	def SetGain(self,gain):
		pass

	def SetSensitivity(self,sens):
		AudioRecognition.lib.setSensitivity(self.obj,sens)

	def GetVersionString(self):
		return str(AudioRecognition.lib.getVersionString(self.obj))

	def GetInputDataSize(self):
		return AudioRecognition.lib.getInputDataSize(self.obj)




class FeatureExtractor(object):

	lib = None
	obj = None

	def __init__(self,libpath,nfft=512,melcount=40,sample_rate=16000,lowerf=20,upperf=8000,window_len=0.03,shift=0.01):

		self.melcount = melcount
		self.shift =  sample_rate*shift
		self.gain = 1

		if (not FeatureExtractor.lib):
			FeatureExtractor.lib = cdll.LoadLibrary(libpath)

			FeatureExtractor.lib.createFeatureExtractor.argtypes = [c_int,c_int,c_int,c_int,c_int,c_float,c_float]
			FeatureExtractor.lib.createFeatureExtractor.restype = c_void_p

			FeatureExtractor.lib.getMelcount.argtypes = [c_void_p]
			FeatureExtractor.lib.getMelcount.restype =  c_int

			FeatureExtractor.lib.signalToMel.argtypes = [c_void_p, POINTER(c_int16),c_int,POINTER(c_uint8),c_float]
			FeatureExtractor.lib.signalToMel.restype = c_int

			FeatureExtractor.lib.deleteFeatureExtractor.argtypes = [c_void_p]
			FeatureExtractor.lib.deleteFeatureExtractor.restype =  None


		self.obj=FeatureExtractor.lib.createFeatureExtractor(nfft,melcount,sample_rate,lowerf,upperf,window_len,shift)

	def __del__(self):
		FeatureExtractor.lib.deleteFeatureExtractor(self.obj)

	#Takes audio data in the form of bytes which are converted to int16
	def signal_to_mel(self,data,gain=1):

		datalen = int(len(data)/2)
		pcm = c_int16 * datalen
		pcmdata = pcm.from_buffer_copy(data)

		number_of_frames = int(datalen / self.shift);
		melsize = self.melcount*number_of_frames
		
		result = (c_uint8 * melsize)()

		reslen = FeatureExtractor.lib.signalToMel(self.obj,pcmdata,datalen,result,gain)

		if(reslen != melsize):
			print("Bad: melsize mismatch")
			print("Expected: " + str(melsize))
			print("Got: " + str(reslen))

		return bytearray(result)

	def SetGain(self,gain):
		self.gain = gain

	def get_melcount(self):
		return FeatureExtractor.lib.getMelcount(self.obj)







