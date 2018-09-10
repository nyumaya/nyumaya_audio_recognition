# nyumaya_audio_recognition
Classify audio with neural nets on embedded systems like the Raspberry Pi using Tensorflow. This should run on any Linux system fine, on other systems at least the recording implementation has to be changed.

To run the demo you have to download at least one of the models and provide the path to the label and graph file. Currently you can change the sensitivity in streaming_example.py. All models contain a result file wich describes the false positive/accuracy tradeoff. 

If you need a special combination of audio classes or model architecture trained create an issue and I will try to prioritize or train it.

## Dependencies:
numpy,tensorflow 

**Inference for Conv-Res-Mini-Narrow and Conv-Res-Mini currently seems broken/incompatible on tensorflow versions 1.8.0 and 1.9.0
To install Tensorflow 1.10.0 on the Raspberry Pi 2/3:**
```
sudo pip install --no-cache-dir https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.10.0/tensorflow-1.10.0-cp27-none-linux_armv7l.whl
```
 **For the Pi Zero:**
 ```
 sudo pip install --no-cache-dir https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.10.0/tensorflow-1.10.0-cp27-none-linux_armv6l.whl
 ```
 **This compiles numpy so it takes about 20 minutes.**
 
```
sudo apt-get install python-numpy
```
To get all models

```
wget https://www.dropbox.com/s/lu3tgxrc49tyhea/models.zip?dl=0
unzip models.zip?dl=0
```
To run an example
```
python streaming_example.py --graph models/Marvin/Conv-Res-Huge/conv-res-huge_frozen.pb  --labels models/Marvin/Conv-Res-Huge/labels.txt  --sens 0.5
```
On the Pi Zero Tensorflow takes a few seconds to load. The demo captures audio from the default microphone. 

Because models constantly improve and I don't want this repository to get bloated the pretrained models are hosted seperately.
To download all models use this [zip file](https://www.dropbox.com/s/lu3tgxrc49tyhea/models.zip?dl=0) This file may not always be up to date.
For each application, different model architectures are available which are a tradeoff between accuracy and cpu/mem usage.

## Model Architectures
- conv_res-mini-narrow (CPU_PI0 34%, CPU_PI3 24% one core)
- conv_res-mini        (CPU_PI0 55%)
- conv_res-full        (CPU_PI0 90%)
- conv_res-huge        (CPU_PI0 nan)


## Applications:
- Speech_commands_subset (yes,no,up,down,left,right,on,off,stop,go)
- Speech_commands_numbers (one,two,three,four,five,six,seven,eight,nine,zero)
- German_commands(an,aus,computer,ein,fernseher,garage,jalousie,licht,musik,oeffnen,radio,rollo,schließen,start,stopp)
- Marvin_hotword (marvin)
- Sheila_hotword (sheila)
- Voice-gender (female,male,nospeech)
- Baby-monitor (cry, babble, door-open, music, glass-break, footsteps, fire-alarm)
- Impulse-response (Play tone and interpret echo: Bedroom, Kitchen, Bathroom, Outdoor, Hall, Living Room, Basement)
- Alarm-system (door-open, glass-break, footsteps, fire-alarm, voice)
- Door-monitor (door bell, door knocking, voice)
- Weather (thunder, rain, storm, hail)
- Language detection
- Swear word detection (imagine some unappropriate words)
- Crowd monitoring(screaming, shouting, gunshot, siren, explosion)

## Pretrained models:
**Accuracy results are taken by feeding the test-set for accuracy and the clean cv-corpus test set for false positives. Some results seem a bit fishy and shouldn't be taken a scientific benchmark. The testing should be improved by using a more diverse test set for false positives and adding background noise / music.**

- [Marvin-conv_res-mini-narrow](https://drive.google.com/open?id=1offSK9sRVc3R5rJiEPTtlxLPgy07CSZz) 
```
Sens: 0.1 Accuracy: 0.940530058177117 False per hour 0.0
Sens: 0.2 Accuracy: 0.9566903684550744 False per hour 0.0
Sens: 0.3 Accuracy: 0.962508080155139 False per hour 0.532086595319765
Sens: 0.4 Accuracy: 0.9657401422107305 False per hour 0.532086595319765
Sens: 0.5 Accuracy: 0.989010989010989 False per hour 2.12834638127906
Sens: 0.6 Accuracy: 0.9909502262443439 False per hour 2.12834638127906
Sens: 0.7 Accuracy: 0.9915966386554622 False per hour 2.12834638127906
Sens: 0.8 Accuracy: 0.9922430510665805 False per hour 3.724606167238355
Sens: 0.9 Accuracy: 0.9922430510665805 False per hour 4.25669276255812
```
- [Marvin-conv_res-mini](https://drive.google.com/open?id=15pwmofH_XeB4HeRuYqiceKA4lYg2Oifx) 
```
Sens: 0.1 Accuracy: 0.9541047188106012 False per hour 0.0
Sens: 0.2 Accuracy: 0.9689722042663219 False per hour 0.0
Sens: 0.3 Accuracy: 0.9722042663219134 False per hour 0.24218132110465665
Sens: 0.4 Accuracy: 0.9747899159663865 False per hour 0.24218132110465665
Sens: 0.5 Accuracy: 0.9922430510665805 False per hour 0.9687252844186266
Sens: 0.6 Accuracy: 0.9948287007110537 False per hour 0.9687252844186266
Sens: 0.7 Accuracy: 0.9948287007110537 False per hour 0.9687252844186266
Sens: 0.8 Accuracy: 0.9961215255332903 False per hour 0.9687252844186266
Sens: 0.9 Accuracy: 0.9961215255332903 False per hour 0.9687252844186266
```
- [Marvin-conv_res-huge](https://drive.google.com/open?id=1npTbW0iNZoEgtE2SolvmLWIFDDkyKfPX)
```
Sens: 0.1 Accuracy: 0.9961215255332903 False per hour 0.9687252844186266
Sens: 0.2 Accuracy: 0.9974143503555268 False per hour 1.9374505688372532
Sens: 0.3 Accuracy: 0.9980607627666451 False per hour 2.4218132110465667
Sens: 0.4 Accuracy: 0.9987071751777634 False per hour 2.6639945321512233
Sens: 0.5 Accuracy: 0.9993535875888817 False per hour 4.35926377988382
Sens: 0.6 Accuracy: 0.9993535875888817 False per hour 5.327989064302447
Sens: 0.7 Accuracy: 0.9993535875888817 False per hour 6.054533027616416
Sens: 0.8 Accuracy: 0.9993535875888817 False per hour 6.296714348721073
Sens: 0.9 Accuracy: 1.0 False per hour 6.296714348721073
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

- [Sheila-conv_mini](https://drive.google.com/open?id=1Bdjem1D3eLjIepN_f54h_olWafBjEyIr)
```
Sens: 0.1 Accuracy: 0.9533678756476685 False per hour 0.24218132110465665
Sens: 0.2 Accuracy: 0.9533678756476685 False per hour 0.24218132110465665
Sens: 0.3 Accuracy: 0.9637305699481865 False per hour 0.24218132110465665
Sens: 0.4 Accuracy: 0.9689119170984456 False per hour 0.24218132110465665
Sens: 0.5 Accuracy: 0.9948186528497409 False per hour 0.4843626422093133
Sens: 0.6 Accuracy: 0.9948186528497409 False per hour 0.4843626422093133
Sens: 0.7 Accuracy: 1.0 False per hour 0.4843626422093133
Sens: 0.8 Accuracy: 1.0 False per hour 0.4843626422093133
Sens: 0.9 Accuracy: 1.0 False per hour 0.4843626422093133
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
Sens: 0.1 Accuracy: 0.7921847246891651 False per hour 3.1532598756852566
Sens: 0.2 Accuracy: 0.8340522709972088 False per hour 5.336285943467358
Sens: 0.3 Accuracy: 0.855874143618371 False per hour 6.063961299394724
Sens: 0.4 Accuracy: 0.8713524486171023 False per hour 6.791636655322091
Sens: 0.5 Accuracy: 0.9286982999238772 False per hour 21.102585321893642
Sens: 0.6 Accuracy: 0.9363105810707942 False per hour 24.983520553506263
Sens: 0.7 Accuracy: 0.9408779497589445 False per hour 27.409105073264154
Sens: 0.8 Accuracy: 0.9456990611519919 False per hour 29.349572689070467
Sens: 0.9 Accuracy: 0.9497589444303476 False per hour 31.29004030487678
```

- [BabyCry-conv_res-mini](https://drive.google.com/open?id=1I1STGHmrBLzwXEOZcv9qRVUP5F80L57U)
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
- [BabyCry-conv_res-huge](https://drive.google.com/open?id=1OgpkGeXQmLQ7tYhsOQXvzOxbE2U-ZRmi)
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

- [Speech-Command-Subset-conv_res-huge](https://drive.google.com/open?id=1SZrFPYf_pBBV6ymyWi7zf4NjpLRG5CSC)
```
Sens: 0.1 Accuracy: 0.9265113699389905 False per hour 2.7370065177248493
Sens: 0.2 Accuracy: 0.9431503050471437 False per hour 2.7370065177248493
Sens: 0.3 Accuracy: 0.9506378258458126 False per hour 3.831809124814789
Sens: 0.4 Accuracy: 0.9556295063782585 False per hour 3.831809124814789
Sens: 0.5 Accuracy: 0.9786466999445369 False per hour 19.706446927618913
Sens: 0.6 Accuracy: 0.9828064337215752 False per hour 21.896052141798794
Sens: 0.7 Accuracy: 0.9847476428175264 False per hour 27.91746648079346
Sens: 0.8 Accuracy: 0.9861342207432058 False per hour 29.0122690878834
Sens: 0.9 Accuracy: 0.9869661674986134 False per hour 31.20187430206328
```

- [Speech-Command-Subset-conv_res-mini](https://drive.google.com/open?id=1SjwEd888qF9nmdkpdkUh9YEbrgLVnIQL)
```
Sens: 0.1 Accuracy: 0.8333333333333334 False per hour 3.831809124814789
Sens: 0.2 Accuracy: 0.8721575152523572 False per hour 6.568815642539638
Sens: 0.3 Accuracy: 0.8926788685524126 False per hour 8.211019553174548
Sens: 0.4 Accuracy: 0.9059900166389351 False per hour 9.853223463809456
Sens: 0.5 Accuracy: 0.9486966167498614 False per hour 45.981709497777466
Sens: 0.6 Accuracy: 0.9572933998890738 False per hour 53.09792644386207
Sens: 0.7 Accuracy: 0.9606211869107044 False per hour 61.30894599703662
Sens: 0.8 Accuracy: 0.9625623960066556 False per hour 64.59335381830644
Sens: 0.9 Accuracy: 0.9656128674431503 False per hour 70.06736685375614
```



## Roadmap:
- [x] Basic working models
- [X] Average output predictions
- [X] Benchmark accuracy and false recognition rate
- [ ] Noisy Benchmark, use more diverse test set (maby musan dataset)
- [ ] Benchmark latency
- [ ] Voice activity detection
- [ ] Provide TensorflowLite and TensorflowJS models
- [ ] Web demo
- [ ] Improve Architectures (including RNN and Attention)
- [ ] More Applications 
