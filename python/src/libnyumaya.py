from ctypes import c_void_p, c_size_t, c_float, c_int, c_uint8, c_int32
from ctypes import cdll, POINTER, c_int16, c_char_p, c_bool, byref, pointer

import sys
import os
class AudioRecognition(object):

	lib = None
	obj = None

	def __init__(self,libpath):

		if (not AudioRecognition.lib):
			print("Loading Library")
			AudioRecognition.lib = cdll.LoadLibrary(libpath)

			print("Initialize Functions")
			AudioRecognition.lib.createAudioRecognition.argtypes = None
			AudioRecognition.lib.createAudioRecognition.restype = c_void_p

			AudioRecognition.lib.getVersionString.argtypes = [c_void_p]
			AudioRecognition.lib.getVersionString.restype = c_char_p

			AudioRecognition.lib.getInputDataSize.argtypes = [c_void_p]
			AudioRecognition.lib.getInputDataSize.restype = c_size_t

			AudioRecognition.lib.setSensitivity.argtypes = [c_void_p, c_float, c_int]
			AudioRecognition.lib.setSensitivity.restype = None

			AudioRecognition.lib.setActive.argtypes = [c_void_p, c_bool, c_int]
			AudioRecognition.lib.setActive.restype = c_int

			AudioRecognition.lib.runDetection.argtypes = [c_void_p, POINTER(c_uint8), c_int]
			AudioRecognition.lib.runDetection.restype = c_int

			AudioRecognition.lib.addModel.argtypes = [c_void_p, c_char_p,c_float, POINTER(c_int32)]
			AudioRecognition.lib.addModel.restype = c_int

			AudioRecognition.lib.addContinousModel.argtypes = [c_void_p, c_char_p, POINTER(c_int32)]
			AudioRecognition.lib.addContinousModel.restype = c_int

			AudioRecognition.lib.getContinousResult.argtypes = [c_void_p, c_int, POINTER(c_float)]
			AudioRecognition.lib.getContinousResult.restype = c_int

			AudioRecognition.lib.addModelFromBuffer.argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_int32)]
			AudioRecognition.lib.addModelFromBuffer.restype = c_int

			AudioRecognition.lib.deleteAudioRecognition.argtypes = [c_void_p]
			AudioRecognition.lib.deleteAudioRecognition.restype = None

		self.obj=AudioRecognition.lib.createAudioRecognition()
		self.checkVersion()

	def __del__(self):
		AudioRecognition.lib.deleteAudioRecognition(self.obj)

	def checkVersion(self):

		major = None
		minor = None
		rev = None

		if sys.version_info[0] < 3:
			major, minor, rev= self.getVersionString().split('.')
		else:
			version_string = self.getVersionString()[2:]
			version_string = version_string[:-1]
			major, minor, rev= version_string.split('.')

		if major != "3":
				print("Your library version is not compatible with this API")

	def addModel(self, path, sensitivity=0.5):
		if( not os.path.exists(path)):
			print("Libnyumaya: Model path {} does not exist".format(path))
			return -1
		modelNumber = c_int32()
		success = AudioRecognition.lib.addModel(self.obj, path.encode('ascii'), sensitivity, pointer(modelNumber))
		if(success != 0):
			print("Libnyumaya: Failed to open model")
			return -1

		#FIXME: Throw error on failure
		return modelNumber.value

	def addContinousModel(self, path):
		modelNumber = c_int32()
		success = AudioRecognition.lib.addContinousModel(self.obj, path.encode('ascii'), pointer(modelNumber))
		if(success != 0):
			print("Libnyumaya: Failed to open model")
			return -1

		#FIXME: Throw error on failure
		return modelNumber.value

	def setActive(self, modelNumber, active):
		success = AudioRecognition.lib.setActive(self.obj, active, modelNumber)
		if(success != 0):
			print("Libnyumaya: Failed to set model active")

		return success

	def removeModel(self, modelNumber):
		success = AudioRecognition.lib.removeModel(self.obj, modelNumber)
		if(success != 0):
			print("Libnyumaya: Failed to remove model")

		return success

	def getContinousResult(self, modelNumber):
		result = (c_float*16)()
		success = AudioRecognition.lib.getContinousResult(self.obj, modelNumber, result)
		if(success != 0):
			print("Failed to get continous result")
		re = [result[i] for i in range(2)]
		return re

	def runDetection(self, data):
		datalen = int(len(data))
		pcm = c_uint8 * datalen
		pcmdata = pcm.from_buffer_copy(data)
		prediction = AudioRecognition.lib.runDetection(self.obj, pcmdata, datalen)
		return prediction

	def setSensitivity(self, sens, modelNumber):
		AudioRecognition.lib.setSensitivity(self.obj, sens, modelNumber)

	def getVersionString(self):
		return str(AudioRecognition.lib.getVersionString(self.obj))

	def getInputDataSize(self):
		return AudioRecognition.lib.getInputDataSize(self.obj)




class FeatureExtractor(object):

	lib = None
	obj = None

	def __init__(self, libpath, nfft=1024, melcount=80, sample_rate=16000, lowerf=50, upperf=4000, window_len=0.03, shift=0.01):

		self.melcount = melcount
		self.shift =  sample_rate*shift
		self.gain = 1

		if (not FeatureExtractor.lib):
			FeatureExtractor.lib = cdll.LoadLibrary(libpath)

			FeatureExtractor.lib.createFeatureExtractor.argtypes = [c_int, c_int, c_int, c_int, c_int, c_float, c_float]
			FeatureExtractor.lib.createFeatureExtractor.restype = c_void_p

			FeatureExtractor.lib.getMelcount.argtypes = [c_void_p]
			FeatureExtractor.lib.getMelcount.restype =  c_int

			FeatureExtractor.lib.signalToMel.argtypes = [c_void_p, POINTER(c_int16), c_int, POINTER(c_uint8), c_float]
			FeatureExtractor.lib.signalToMel.restype = c_int

			FeatureExtractor.lib.deleteFeatureExtractor.argtypes = [c_void_p]
			FeatureExtractor.lib.deleteFeatureExtractor.restype =  None


		self.obj=FeatureExtractor.lib.createFeatureExtractor(nfft, melcount, sample_rate, lowerf, upperf, window_len, shift)

	def __del__(self):
		FeatureExtractor.lib.deleteFeatureExtractor(self.obj)

	#Takes audio data in the form of bytes which are converted to int16
	def signalToMel(self,data,gain=1):

		datalen = int(len(data)/2)
		pcm = c_int16 * datalen
		pcmdata = pcm.from_buffer_copy(data)

		number_of_frames = int(datalen / self.shift);
		melsize = self.melcount*number_of_frames
		
		result = (c_uint8 * melsize)()

		reslen = FeatureExtractor.lib.signalToMel(self.obj, pcmdata, datalen, result, gain)

		if(reslen != melsize):
			print("Bad: melsize mismatch")
			print("Expected: " + str(melsize))
			print("Got: " + str(reslen))

		return bytearray(result)

	def setGain(self,gain):
		self.gain = gain

	def getMelcount(self):
		return FeatureExtractor.lib.getMelcount(self.obj)







