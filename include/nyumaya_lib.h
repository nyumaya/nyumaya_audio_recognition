#ifndef NYUMAYA_AUDIO_RECOGNITION_H
#define NYUMAYA_AUDIO_RECOGNITION_H

#include <string>

class AudioRecognitionImpl;
class SpeakerVerificationImpl;
class FeatureExtractor;

extern "C"
{


	const char* GetVersionString(){return "0.0.3";}

	//Audio Recognition
	AudioRecognitionImpl* create_audio_recognition(const char* modelPath);
	
	//@param array_length    Number of int16_t samples
	//@param data            Signed int16 pcm data
	int RunDetection(AudioRecognitionImpl*impl,const uint8_t* const data,const int mel_length); 
	
	void SetSensitivity(AudioRecognitionImpl*impl,float sens);
 	
	size_t GetInputDataSize(AudioRecognitionImpl*impl);
	

	//Speaker Verification
	SpeakerVerificationImpl* create_speaker_verification(const char*modelPath);

	float* VerifySpeaker(SpeakerVerificationImpl*impl,const int16_t* const data,const int array_length);
	
	
	
	//Feature Extractor
	FeatureExtractor* create_feature_extractor(size_t nfft=512,size_t melcount = 40,size_t sample_rate=16000,
	    size_t lowerf=20, size_t upperf=8000,float window_len=0.03,float shift=0.01);

	int signal_to_mel(FeatureExtractor*impl,const int16_t * const pcm, size_t len,uint8_t*result,float gain);
	
	size_t get_melcount(FeatureExtractor*impl);
		
	void remove_dc_offset(FeatureExtractor*impl,bool value);
	

}





#endif
