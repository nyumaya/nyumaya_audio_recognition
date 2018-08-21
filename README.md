# nyumaya_audio_recognition
Classify audio with neural nets on embedded systems like the Raspberry Pi


Audio classification using Tensorflow. To run the demo:
python streaming_example.py --labels models/speech_command/labels.txt --graph models/speech_command/conv-res-mini_frozen.pb

On the Pi Zero Tensorflow takes a few seconds to load. The demo captures audio from the default microphone. 
Accuracy is not good yet, especially on false positives. This will be improved in the next couple days.

## Dependencies:
numpy,tensorflow 
Both can be installed via pip

```
pip install numpy
pip install tensorflow
```
Because models constantly improve and I don't want this repository to get bloated the pretrained models are hosted [here](https://drive.google.com/open?id=1cv4R_zrfr88q7AcNxd5OsXVIxOyFwLOu).
For each application, different model architectures are available which are a tradeoff between accuracy and cpu/mem usage.

## Model Architectures
- conv_res-mini-narrow
- conv_res-mini
- conv_res-full
- conv_res-huge


## Applications:
- speech_commands_subset (yes,no,up,down,left,right,on,off,stop,go)
- speech_commands_numbers (one,two,three,four,five,six,seven,eight,nine,zero)
- marvin_hotword (marvin)

## Roadmap:
- [x] Basic working models
- [ ] Benchmark accuracy and false recognition rate
- [ ] Web demo
- [ ] Improve Architectures (including RNN and Attention)
- [ ] More Applications 
