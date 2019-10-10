#ifndef NYUMAYA_AUDIO_RECOGNITION_H
#define NYUMAYA_AUDIO_RECOGNITION_H

class AudioRecognitionImpl;
class FeatureExtractor;

#define DEFAULT_VIS  __attribute__ ((visibility ("default") ))

extern "C"
{

	const char* getVersionString() DEFAULT_VIS;

	//Audio Recognition
	AudioRecognitionImpl* createAudioRecognition() DEFAULT_VIS;

	void deleteAudioRecognition(AudioRecognitionImpl*impl) DEFAULT_VIS;
	
	//Open Audio Recognition Model by Filename
	//@param modelPath: Zero Terminate char array of model filename
	int openModel(AudioRecognitionImpl*impl,const char*modelPath) DEFAULT_VIS;

	//Sometimes it's not possible to load files (eg. Android). 
	//This method allows to load a model from a binary buffer
	//@param binaryModel: char array of the binary read model file
	//@param len: Length of the binary model file
	int loadModelFromBuffer(AudioRecognitionImpl*impl,const char*binaryModel,int len) DEFAULT_VIS;

	//Input Mel Features and get the raw probabilities of the labels
	uint8_t* runRawDetection(AudioRecognitionImpl*impl,const uint8_t* const data,const int mel_length) DEFAULT_VIS;

	
	//Input Mel Features and get the index of the detected label if recognized
	//@param array_length    Number of mel features
	//@param data            Signed uint8_t mel features
	int runDetection(AudioRecognitionImpl*impl,const uint8_t* const data,const int mel_length) DEFAULT_VIS;
	
	//Set Detection Sensitivity
	//@param sens [0-1] 0: Low detection rate 1: High detection rate
	void setSensitivity(AudioRecognitionImpl*impl,float sens) DEFAULT_VIS;

 	//Retrieve the number of Mel Features the Detector Expects
	size_t getInputDataSize(AudioRecognitionImpl*impl) DEFAULT_VIS;


	//Feature Extractor
	FeatureExtractor* createFeatureExtractor(size_t nfft=512,size_t melcount=40,size_t sample_rate=16000,
	    size_t lowerf=20, size_t upperf=8000,float window_len=0.03,float shift=0.01) DEFAULT_VIS;

	void deleteFeatureExtractor(FeatureExtractor*impl) DEFAULT_VIS;

	//Extract Mel-Spectrogram Features from PCM Audio Data
	//@param pcm: Single Channel 16kHZ PCM encoded audio data
	//@param len: Number of 
	//@param result:
	//@param gain
	int signalToMel(FeatureExtractor*impl,const int16_t * const pcm, size_t len,uint8_t*result,float gain) DEFAULT_VIS;
	

	//Returns the number of Chosen Mel Features per frame
	size_t getMelcount(FeatureExtractor*impl) DEFAULT_VIS;


}


#endif


