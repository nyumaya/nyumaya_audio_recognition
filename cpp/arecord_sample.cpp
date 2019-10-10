
#include <stdio.h>
#include <stdlib.h>
#include <alsa/asoundlib.h>
#include <iostream>

#include "nyumaya_lib.h"

unsigned int sample_rate = 16000;

snd_pcm_t * open_soundcard(char*name)
{
	snd_pcm_t *capture_handle;
	int err;
	snd_pcm_hw_params_t *hw_params;
	snd_pcm_format_t format = SND_PCM_FORMAT_S16_LE;


	if ((err = snd_pcm_open (&capture_handle, name, SND_PCM_STREAM_CAPTURE, 0)) < 0) {
		fprintf (stderr, "cannot open audio device %s (%s)\n", name,snd_strerror (err));
		exit (1);
	}
	   
	if ((err = snd_pcm_hw_params_malloc (&hw_params)) < 0) {
		fprintf (stderr, "cannot allocate hardware parameter structure (%s)\n",snd_strerror (err));
		exit (1);
	}

			 
	if ((err = snd_pcm_hw_params_any (capture_handle, hw_params)) < 0) {
		fprintf (stderr, "cannot initialize hardware parameter structure (%s)\n",snd_strerror (err));
		exit (1);
	}


	if ((err = snd_pcm_hw_params_set_access (capture_handle, hw_params, SND_PCM_ACCESS_RW_INTERLEAVED)) < 0) {
		fprintf (stderr, "cannot set access type (%s)\n",snd_strerror (err));
		exit (1);
	}

	
	if ((err = snd_pcm_hw_params_set_format (capture_handle, hw_params, format)) < 0) {
		fprintf (stderr, "cannot set sample format (%s)\n",snd_strerror (err));
		exit (1);
	}
	
	if ((err = snd_pcm_hw_params_set_rate_near (capture_handle, hw_params, &sample_rate, 0)) < 0) {
		fprintf (stderr, "cannot set sample rate (%s)\n",snd_strerror (err));
		exit (1);
	}
	
	if ((err = snd_pcm_hw_params_set_channels (capture_handle, hw_params, 1)) < 0) {
		fprintf (stderr, "cannot set channel count (%s)\n",snd_strerror (err));
		exit (1);
	}

	if ((err = snd_pcm_hw_params (capture_handle, hw_params)) < 0) {
		fprintf (stderr, "cannot set parameters (%s)\n",snd_strerror (err));
		exit (1);
	}

	snd_pcm_hw_params_free (hw_params);

	if ((err = snd_pcm_prepare (capture_handle)) < 0) {
		fprintf (stderr, "cannot prepare audio interface for use (%s)\n",snd_strerror (err));
		exit (1);
	}

	return capture_handle;

}



int main (int argc, char *argv[])
{

	//New Instance of Audio Recognizer
	AudioRecognitionImpl *audio_recognizer = createAudioRecognition();
	openModel(audio_recognizer,argv[2]);
	setSensitivity(audio_recognizer,0.5);
	int buffer_size = getInputDataSize(audio_recognizer);
	
	FeatureExtractor* feature_extractor = createFeatureExtractor();
	
	//Open the default Soundcard
	snd_pcm_t *capture_handle;
	capture_handle = open_soundcard(argv[1]);

	int err;
	char *buffer = (char*) malloc(buffer_size);


	while(true) 
	{
		if ((err = snd_pcm_readi (capture_handle, buffer, buffer_size/2)) !=  buffer_size/2) {
			fprintf (stderr, "read from audio interface failed (%s)\n",err, snd_strerror (err));
			exit (1);
		}
		
		uint8_t melfeatures[800];
		
		float gain = 1.0;
		int mel_len = signalToMel(feature_extractor,(int16_t*)buffer,buffer_size/2,melfeatures,gain);
		
		int res = runDetection(audio_recognizer,melfeatures,mel_len);

		if(res != 0){
			std::cout << "Keyword detected" << std::endl;
		}

	}

	free(buffer);
	snd_pcm_close (capture_handle);

	return 0;

}







