
from ctypes import *



class AudioRecognition(object):


	def __init__(self,libpath,modelpath):

		self.lib = cdll.LoadLibrary(libpath)
		
		self.lib.create_audio_recognition.argtypes = [c_char_p]
		self.lib.create_audio_recognition.restype = c_void_p

		self.lib.GetVersionString.argtypes = [c_void_p]
		self.lib.GetVersionString.restype = c_char_p

		self.lib.GetInputDataSize.argtypes = [c_void_p]
		self.lib.GetInputDataSize.restype = c_size_t


		self.lib.SetGain.argtypes = [c_void_p,c_float]
		self.lib.SetGain.restype = None

		self.lib.SetSensitivity.argtypes = [c_void_p,c_float]
		self.lib.SetSensitivity.restype = None

		self.lib.RunDetection.argtypes = [c_void_p, POINTER(c_int16),c_int]
		self.lib.RunDetection.restype = c_int

		self.obj=self.lib.create_audio_recognition(modelpath)

	def RunDetection(self,data,datalen):
		return self.lib.RunDetection(self.obj,(c_int16 * len(data))(*data),datalen/2)

	def SetSensitivity(self,sens):
		self.lib.SetSensitivity(self.obj,sens)

	def GetVersionString(self):
		return self.lib.GetVersionString(self.obj)

	def GetInputDataSize(self):
		return self.lib.GetInputDataSize(self.obj)









