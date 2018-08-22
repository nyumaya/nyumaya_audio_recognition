# nyumaya_audio_recognition
Classify audio with neural nets on embedded systems like the Raspberry Pi


Audio classification using Tensorflow. To run the demo:
python streaming_example.py --labels models/speech_command/labels.txt --graph models/speech_command/conv-res-mini_frozen.pb

On the Pi Zero Tensorflow takes a few seconds to load. The demo captures audio from the default microphone. 

Accuracy is not perfect yet, especially on false positives.

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
- conv_res-mini-narrow (CPU_PI0 34%)
- conv_res-mini        (CPU_PI0 55%)
- conv_res-full        (CPU_PI0 90%)
- conv_res-huge        (CPU_PI0 nan)


## Applications:
- speech_commands_subset (yes,no,up,down,left,right,on,off,stop,go)
- speech_commands_numbers (one,two,three,four,five,six,seven,eight,nine,zero)
- marvin_hotword (marvin)

## Roadmap:
- [x] Basic working models
- [X] Average output predictions
- [ ] Benchmark accuracy and false recognition rate
- [ ] Provide TensorflowLite and TensorflowJS models
- [ ] Web demo
- [ ] Improve Architectures (including RNN and Attention)
- [ ] More Applications 
