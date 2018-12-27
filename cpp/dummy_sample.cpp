#include <ctime>
#include <iostream>
#include <cstdlib>  

#include "nyumaya_lib.h"


int main (int argc, char *argv[])
{
	AudioRecognitionImpl *audio_recognizer = create_audio_recognition(argv[1]);
	SetSensitivity(audio_recognizer,0.5);
	int buffer_size = GetInputDataSize(audio_recognizer);
	
	FeatureExtractor* feature_extractor = create_feature_extractor();

	char *buffer = (char*) malloc(buffer_size);

	clock_t begin = clock();

	for (int i = 0 ; i < 100 ; i++){
		// Run inference
		int16_t data_test[3200];
		for(int i = 0; i < 3200; ++i)
		{
			data_test[i] = (std::rand() - 16384)/1000.0 ;
		}
		
		
		uint8_t melfeatures[800];
		float gain = 1.0;
		int mel_len = signal_to_mel(feature_extractor,(int16_t*)buffer,buffer_size/2,melfeatures,gain);
		
		int res = RunDetection(audio_recognizer,melfeatures,mel_len);
		std::cout << "OK: " << res << std::endl;
	}


	clock_t end = clock();
	double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	std::cout << "Time taken: " << elapsed_secs << std::endl;
	

	return 0;
}
