#ifndef NYUMAYA_AUDIO_RECOGNITION_H
#define NYUMAYA_AUDIO_RECOGNITION_H

class AudioRecognitionImpl;
class FeatureExtractor;

#define DEFAULT_VIS __attribute__ ((visibility ("default") ))

extern "C"
{
	const char* getVersionString() DEFAULT_VIS;

	//Audio Recognition
	AudioRecognitionImpl* createAudioRecognition() DEFAULT_VIS;

	//Free Audio recognition instance
	void deleteAudioRecognition(AudioRecognitionImpl*impl) DEFAULT_VIS;

	//Open Audio Recognition Model by Filename
	//@param modelPath: Zero Terminate char array of model filename
	//@param sensitivity: Sensitivity of hotword in the range 0.0-1.0
	//@param modelNumber: Reference to integer where the resulting model
	//                    number will be written to
	//returns: 0 on success
	int addModel(AudioRecognitionImpl*impl, const char *modelPath, float sensitivity, int32_t *modelNumber) DEFAULT_VIS;

	//Activate or deactivate a model
	int setActive(AudioRecognitionImpl*impl, bool active, int modelNumber) DEFAULT_VIS;

	//Delete Model by ID
	//@param modelPath: Zero Terminate char array of model filename
	int deleteModel(AudioRecognitionImpl*impl, int modelNumber) DEFAULT_VIS;

	//Sometimes it's not possible to load files (eg. Android). 
	//This method allows to load a model from a binary buffer
	//@param binaryModel: char array of the binary read model file
	//@param len: Length of the binary model file
	int addModelFromBuffer(AudioRecognitionImpl*impl, const char *binaryModel, int len, int32_t *modelNumber) DEFAULT_VIS;

	//Input Mel Features and get the index of the detected label if recognized
	//@param array_length    Number of mel features
	//@param data            Signed uint8_t mel features
	int runDetection(AudioRecognitionImpl*impl, const uint8_t* const data, const int mel_length) DEFAULT_VIS;
	
	//Set Detection Sensitivity
	//@param sens [0-1] 0: Low detection rate 1: High detection rate
	int setSensitivity(AudioRecognitionImpl*impl, float sens, int modelNumber) DEFAULT_VIS;

	//Set Detection Cooldown
	//@param frames [0-1] 0: Low detection rate 1: High detection rate
	int setDetectionCooldown(AudioRecognitionImpl*impl, int frames, int modelNumber) DEFAULT_VIS;


 	//Retrieve the number of Mel Features the Detector Expects
	uint32_t getInputDataSize(AudioRecognitionImpl*impl) DEFAULT_VIS;


	//Feature Extractor
	FeatureExtractor* createFeatureExtractor(uint32_t nfft=1024, uint32_t melcount=80, uint32_t sample_rate=16000,
	    uint32_t lowerf=50, uint32_t upperf=4000, float window_len=0.03, float shift=0.01) DEFAULT_VIS;

	void deleteFeatureExtractor(FeatureExtractor*impl) DEFAULT_VIS;

	//Extract Mel-Spectrogram Features from PCM Audio Data
	//@param pcm: Single Channel 16kHZ PCM encoded audio data
	//@param len: Number of 
	//@param result:
	//@param gain
	int signalToMel(FeatureExtractor*impl,const int16_t * const pcm, uint32_t len, uint8_t*result, float gain) DEFAULT_VIS;

	//Returns the number of Chosen Mel Features per frame
	uint32_t getMelcount(FeatureExtractor*impl) DEFAULT_VIS;

	int addContinousModel(AudioRecognitionImpl*impl, const char*modelPath, int32_t *modelNumber) DEFAULT_VIS;

	int getContinousResult(AudioRecognitionImpl*impl, int modelNumber, float*result) DEFAULT_VIS;
}


#endif


