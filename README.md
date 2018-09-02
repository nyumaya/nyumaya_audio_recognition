# nyumaya_audio_recognition
Classify audio with neural nets on embedded systems like the Raspberry Pi. This should run on any Linux system fine, on other systems at least the recording implementation has to be changed.


Audio classification using Tensorflow. To run the demo you have to download at least one of the models and provide the path to the label and graph file. Currently you can change the sensitivity in streaming_example.py. All models contain a result file wich describes the false positive/accuracy tradeoff. 

python streaming_example.py --labels models/speech_command/labels.txt --graph models/speech_command/conv-res-mini_frozen.pb

On the Pi Zero Tensorflow takes a few seconds to load. The demo captures audio from the default microphone. 


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
- language detection

## Pretrained models:
**Accuracy results are taken by feeding the test-set for accuracy and the clean cv-corpus test set for false positives. Some results seem a bit fishy and shouldn't be taken a scientific benchmark. The testing should be improved by using a more diverse test set for false positives and adding background noise / music.**

- [Marvin-conv_res-mini-narrow](https://drive.google.com/open?id=1offSK9sRVc3R5rJiEPTtlxLPgy07CSZz) 
```
Sens: 0.1 Accuracy: 0.7078215901745313 False per hour 1.06417319063953
Sens: 0.2 Accuracy: 0.7627666451195863 False per hour 1.5962597859592949
Sens: 0.3 Accuracy: 0.7853910795087266 False per hour 1.5962597859592949
Sens: 0.4 Accuracy: 0.8047834518422754 False per hour 1.5962597859592949
Sens: 0.5 Accuracy: 0.92049127343245 False per hour 3.1925195719185897
Sens: 0.6 Accuracy: 0.9282482223658695 False per hour 3.1925195719185897
Sens: 0.7 Accuracy: 0.9340659340659341 False per hour 3.1925195719185897
Sens: 0.8 Accuracy: 0.9379444085326438 False per hour 3.724606167238355
Sens: 0.9 Accuracy: 0.940530058177117 False per hour 3.724606167238355
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
- [Sheila-conv_res-huge](https://drive.google.com/open?id=1gEwY6TGylaWiqn8RHvCE1D-7n71N3vvj)
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
- [Sheila-conv_res-mini-narrow](https://drive.google.com/open?id=1sa4ZOqwmVges7dsDX5LG5mXOOHMiyp8t)
```
Sens: 0.1 Accuracy: 0.9222797927461139 False per hour 0.0
Sens: 0.2 Accuracy: 0.9533678756476685 False per hour 0.532086595319765
Sens: 0.3 Accuracy: 0.9533678756476685 False per hour 0.532086595319765
Sens: 0.4 Accuracy: 0.9585492227979274 False per hour 1.06417319063953
Sens: 0.5 Accuracy: 0.9896373056994818 False per hour 7.44921233447671
Sens: 0.6 Accuracy: 0.9896373056994818 False per hour 9.045472120436004
Sens: 0.7 Accuracy: 0.9896373056994818 False per hour 9.045472120436004
Sens: 0.8 Accuracy: 0.9948186528497409 False per hour 9.045472120436004
Sens: 0.9 Accuracy: 0.9948186528497409 False per hour 9.57755871575577
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

- [Number-conv_res-mini](https://drive.google.com/open?id=1r3E_vcT57XcNvKddANRYLsY_kw5lpLda)
```
Sens: 0.1 Accuracy: 0.8299923877188531 False per hour 11.867344663650664
Sens: 0.2 Accuracy: 0.8627251966505963 False per hour 14.564468450843997
Sens: 0.3 Accuracy: 0.8787109870591221 False per hour 16.722167480598664
Sens: 0.4 Accuracy: 0.8896219233697031 False per hour 19.95871602523066
Sens: 0.5 Accuracy: 0.9449378330373002 False per hour 85.22911167530931
Sens: 0.6 Accuracy: 0.9492514590205532 False per hour 98.71473061127598
Sens: 0.7 Accuracy: 0.9515351433646283 False per hour 101.41185439846932
Sens: 0.8 Accuracy: 0.9558487693478812 False per hour 111.66092478980397
Sens: 0.9 Accuracy: 0.9578787109870591 False per hour 116.51574760675197
```

- [Number-conv_res-mini-narrow](https://drive.google.com/open?id=1QhpafpjpAdrgwi04NMH5yNUx8wi9Fiko)
```
Sens: 0.1 Accuracy: 0.7132707434661254 False per hour 28.05008738681066
Sens: 0.2 Accuracy: 0.7663029687896473 False per hour 50.16650244179599
Sens: 0.3 Accuracy: 0.796244607967521 False per hour 63.652121377762654
Sens: 0.4 Accuracy: 0.818066480588683 False per hour 71.74349273934266
Sens: 0.5 Accuracy: 0.9007866023851814 False per hour 248.13538842178662
Sens: 0.6 Accuracy: 0.9152499365643237 False per hour 292.90764328919596
Sens: 0.7 Accuracy: 0.9210860187769602 False per hour 328.5096772801479
Sens: 0.8 Accuracy: 0.9266683582846993 False per hour 353.3232161223266
Sens: 0.9 Accuracy: 0.931743212382644 False per hour 374.3607816624346
```

-[BabyCry-conv_res-mini](https://drive.google.com/open?id=1I1STGHmrBLzwXEOZcv9qRVUP5F80L57U)
```
Sens: 0.1 Accuracy: 0.9 False per hour 0.0
Sens: 0.2 Accuracy: 0.9 False per hour 0.0
Sens: 0.3 Accuracy: 0.9181818181818182 False per hour 0.0
Sens: 0.4 Accuracy: 0.9272727272727272 False per hour 0.0
Sens: 0.5 Accuracy: 0.9636363636363636 False per hour 0.0
Sens: 0.6 Accuracy: 0.9727272727272728 False per hour 0.0
Sens: 0.7 Accuracy: 0.9727272727272728 False per hour 0.0
Sens: 0.8 Accuracy: 0.9727272727272728 False per hour 0.0
Sens: 0.9 Accuracy: 0.9727272727272728 False per hour 0.0
```
-[BabyCry-conv_res-huge](https://drive.google.com/open?id=1OgpkGeXQmLQ7tYhsOQXvzOxbE2U-ZRmi)
```
Sens: 0.1 Accuracy: 0.9636363636363636 False per hour 0.0
Sens: 0.2 Accuracy: 0.9636363636363636 False per hour 0.0
Sens: 0.3 Accuracy: 0.9727272727272728 False per hour 0.0
Sens: 0.4 Accuracy: 0.9727272727272728 False per hour 0.0
Sens: 0.5 Accuracy: 0.990909090909091 False per hour 2.12834638127906
Sens: 0.6 Accuracy: 0.990909090909091 False per hour 2.6604329765988246
Sens: 0.7 Accuracy: 0.990909090909091 False per hour 2.6604329765988246
Sens: 0.8 Accuracy: 0.990909090909091 False per hour 3.1925195719185897
Sens: 0.9 Accuracy: 0.990909090909091 False per hour 3.724606167238355
```


## Roadmap:
- [x] Basic working models
- [X] Average output predictions
- [X] Benchmark accuracy and false recognition rate
- [ ] Noisy Benchmark, use more diverse test set
- [ ] Benchmark latency
- [ ] Voice activity detection
- [ ] Provide TensorflowLite and TensorflowJS models
- [ ] Web demo
- [ ] Improve Architectures (including RNN and Attention)
- [ ] More Applications 
