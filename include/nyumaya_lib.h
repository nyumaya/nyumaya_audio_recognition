#ifndef NYUMAYA_AUDIO_RECOGNITION_H
#define NYUMAYA_AUDIO_RECOGNITION_H

#include <string>

class AudioRecognitionImpl;
class AudioRecognition {

	public:

		AudioRecognition(const std::string& modelPath);

		~AudioRecognition();

		int RunDetection(int16_t*data,const int array_length);

		//Set the detection sensitivity between 0-1
		//0 low sensitivity
		//1 high sensitivity
		void SetSensitivity(float sens);

		//Set the volume gain to be applied to the input signal
		void SetGain(float val);
		
		size_t GetInputDataSize();
		std::string GetVersionString();
	private:
		AudioRecognitionImpl* mImpl;
};




extern "C"
{
	AudioRecognitionImpl* create_audio_recognition(const char* modelPath);
	int RunDetection(AudioRecognitionImpl*impl,int16_t*data,const int array_length); 
	void SetSensitivity(AudioRecognitionImpl*impl,float sens);
 	void SetGain(AudioRecognitionImpl*impl,float val);
	size_t GetInputDataSize(AudioRecognitionImpl*impl);
	char* GetVersionString(AudioRecognitionImpl*impl);
}





#endif
