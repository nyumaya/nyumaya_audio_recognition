# nyumaya_audio_recognition
Classify audio with neural nets on embedded systems like the Raspberry Pi


Audio classification using Tensorflow. To run the demo:
python streaming_example.py --labels models/speech_command/labels.txt --graph models/speech_command/conv-res-mini_frozen.pb

On the Pi Zero Tensorflow takes a few seconds to load. The demo captures audio from the default microphone. 
Accuracy is not good yet, especially on false positives. This will be improved in the next couple days.

Dependencies:  
numpy, tensorflow

Both can be installed via pip
