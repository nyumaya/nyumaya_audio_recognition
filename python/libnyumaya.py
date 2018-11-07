
from ctypes import *


class AudioRecognition(object):

	lib = None

	def __init__(self,libpath,modelpath,label_path=None):

		if (not AudioRecognition.lib):
			AudioRecognition.lib = cdll.LoadLibrary(libpath)
		
			AudioRecognition.lib.create_audio_recognition.argtypes = [c_char_p]
			AudioRecognition.lib.create_audio_recognition.restype = c_void_p

			AudioRecognition.lib.GetVersionString.argtypes = [c_void_p]
			AudioRecognition.lib.GetVersionString.restype = c_char_p

			AudioRecognition.lib.GetInputDataSize.argtypes = [c_void_p]
			AudioRecognition.lib.GetInputDataSize.restype = c_size_t

			AudioRecognition.lib.SetGain.argtypes = [c_void_p,c_float]
			AudioRecognition.lib.SetGain.restype = None
			
			AudioRecognition.lib.RemoveDC.argtypes = [c_void_p,c_bool]
			AudioRecognition.lib.RemoveDC.restype = None

			AudioRecognition.lib.SetSensitivity.argtypes = [c_void_p,c_float]
			AudioRecognition.lib.SetSensitivity.restype = None

			AudioRecognition.lib.RunDetection.argtypes = [c_void_p, POINTER(c_int16),c_int]
			AudioRecognition.lib.RunDetection.restype = c_int

		self.obj=AudioRecognition.lib.create_audio_recognition(modelpath.encode('ascii'))

		if(label_path):
			self.labels_list = self._load_labels(label_path)

	def RunDetection(self,data):
		datalen = int(len(data)/2)
		pcm = c_int16 * datalen	
		pcmdata = pcm.from_buffer(data)
		prediction = AudioRecognition.lib.RunDetection(self.obj,pcmdata,datalen)
		return prediction

	def GetPredictionLabel(self,index):
		if(self.labels_list):
			return self.labels_list[index]
		
	def SetGain(self,gain):
		AudioRecognition.lib.SetGain(self.obj,gain)

	def SetSensitivity(self,sens):
		AudioRecognition.lib.SetSensitivity(self.obj,sens)

	def GetVersionString(self):
		return str(AudioRecognition.lib.GetVersionString(self.obj))

	def GetInputDataSize(self):
		return AudioRecognition.lib.GetInputDataSize(self.obj)
		
	def RemoveDC(self,val):
		AudioRecognition.lib.RemoveDC(self.obj,val)



	def _load_labels(self,filename):
		with open(filename,'r') as f:  
			return [line.strip() for line in f]






