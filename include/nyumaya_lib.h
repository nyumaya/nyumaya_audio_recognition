#ifndef NYUMAYA_AUDIO_RECOGNITION_H
#define NYUMAYA_AUDIO_RECOGNITION_H

#include <string>

class AudioRecognitionImpl;
class AudioRecognition {

	public:

		AudioRecognition(const std::string& modelPath);
		~AudioRecognition();

		int RunDetection(int16_t*data,const int array_length);
		void SetSensitivity(float sens);
		void SetGain(float val);

		size_t GetInputDataSize();
		std::string GetVersionString();
	private:
		AudioRecognitionImpl* mImpl;
};

#endif
