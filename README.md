# nyumaya_audio_recognition
Classify audio with neural nets on embedded systems like the Raspberry Pi. This should run on any Linux system fine, on other systems at least the recording implementation has to be changed.


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
Because models constantly improve and I don't want this repository to get bloated the pretrained models are hosted on a google drive.
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
- sheila_hotword (sheila)
- voice-gender (female,male,nospeech)
- baby-monitor (cry, babble, door-open, music, glass-break, footsteps, fire-alarm)
- impulse-response (Play tone and interpret echo: Bedroom, Kitchen, Bathroom, Outdoor, Hall, Living Room, Basement)
- alarm-system (door-open, glass-break, footsteps, fire-alarm, voice)
- door-monitor (door bell, door knocking, voice)
- weather (thunder, rain, storm, hail)

## Pretrained models:
**Accuracy Results are taken by feeding the test-set for accuracy and the clean cv-corpus test set for false positives. Some results seem a bit fishy and shouldn't be taken a scientific benchmark. The testing should be improved by using a more diverse test set for false positives and adding background noise / music.***

- [Marvin-conv_res-mini-narrow](https://drive.google.com/open?id=1sBml8VnnrjsleY8EQagoAzddwQCSayUP) 
```
Sens: 0.1 Accuracy: 0.40077569489334197 False per hour 3.1925195719185897
Sens: 0.2 Accuracy: 0.4886877828054299 False per hour 4.25669276255812
Sens: 0.3 Accuracy: 0.5307045895281189 False per hour 6.385039143837179
Sens: 0.4 Accuracy: 0.5656108597285068 False per hour 7.981298929796474
Sens: 0.5 Accuracy: 0.7795733678086619 False per hour 24.47598338470919
Sens: 0.6 Accuracy: 0.7963800904977376 False per hour 31.925195719185897
Sens: 0.7 Accuracy: 0.8093083387201034 False per hour 33.52145550514519
Sens: 0.8 Accuracy: 0.8170652876535229 False per hour 39.906494648982374
Sens: 0.9 Accuracy: 0.8241758241758241 False per hour 44.16318741154049
```
- [Marvin-conv_res-huge](https://drive.google.com/open?id=1npTbW0iNZoEgtE2SolvmLWIFDDkyKfPX)
```
Sens: 0.1 Accuracy: 0.9967679379444085 False per hour 6.683523999420757
Sens: 0.2 Accuracy: 0.9980607627666451 False per hour 6.683523999420757
Sens: 0.3 Accuracy: 0.9980607627666451 False per hour 6.683523999420757
Sens: 0.4 Accuracy: 0.9980607627666451 False per hour 6.683523999420757
Sens: 0.5 Accuracy: 0.9993535875888817 False per hour 15.037928998696703
Sens: 0.6 Accuracy: 0.9993535875888817 False per hour 16.708809998551892
Sens: 0.7 Accuracy: 0.9993535875888817 False per hour 18.37969099840708
Sens: 0.8 Accuracy: 0.9993535875888817 False per hour 20.05057199826227
Sens: 0.9 Accuracy: 0.9993535875888817 False per hour 21.72145299811746
```
- [Sheila-conv_res-huge](https://drive.google.com/open?id=1gnjww5741tDX5J1pqcz_w6aw3yAR747T)
```
Sens: 0.1 Accuracy: 1.0 False per hour 0.0
Sens: 0.2 Accuracy: 1.0 False per hour 0.0
Sens: 0.3 Accuracy: 1.0 False per hour 0.0
Sens: 0.4 Accuracy: 1.0 False per hour 0.0
Sens: 0.5 Accuracy: 1.0 False per hour 1.6708809998551892
Sens: 0.6 Accuracy: 1.0 False per hour 3.3417619997103785
Sens: 0.7 Accuracy: 1.0 False per hour 5.012642999565568
Sens: 0.8 Accuracy: 1.0 False per hour 5.012642999565568
Sens: 0.9 Accuracy: 1.0 False per hour 5.012642999565568
```
- [Number-conv_res-huge](https://drive.google.com/open?id=1bPx9c84pZ3GcjlK-c4-MvYz9lyaKPvhW)
```
Sens: 0.1 Accuracy: 0.9218472468916519 False per hour 15.200990879405474
Sens: 0.2 Accuracy: 0.9406242070540471 False per hour 18.578988852606688
Sens: 0.3 Accuracy: 0.9507739152499366 False per hour 20.267987839207297
Sens: 0.4 Accuracy: 0.9540725704136006 False per hour 23.645985812408515
Sens: 0.5 Accuracy: 0.9743719868053794 False per hour 81.07195135682919
Sens: 0.6 Accuracy: 0.9766556711494545 False per hour 89.51694628983223
Sens: 0.7 Accuracy: 0.9784318700837351 False per hour 99.65094020943589
Sens: 0.8 Accuracy: 0.9794468409033240 False per hour 109.78493412903953
Sens: 0.9 Accuracy: 0.9802080690180157 False per hour 121.60792703524379
```

## Roadmap:
- [x] Basic working models
- [X] Average output predictions
- [ ] Benchmark accuracy and false recognition rate
- [ ] Voice activity detection
- [ ] Provide TensorflowLite and TensorflowJS models
- [ ] Web demo
- [ ] Improve Architectures (including RNN and Attention)
- [ ] More Applications 
