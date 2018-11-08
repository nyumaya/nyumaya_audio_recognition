# Detect simple voice commands and audio events on small embedded sytems like the PiZero.
Classify audio with neural nets on embedded systems like the Raspberry Pi using Tensorflow. This should run on any Linux system fine, on other systems at least the recording implementation has to be changed.

To run the demo you have to download at least one of the models and provide the path to the label and graph file. Currently you can change the sensitivity in streaming_example.py. All models contain a result file wich describes the false positive/accuracy tradeoff. 

If you need a special combination of audio classes or model architecture trained create an issue and I will try to prioritize or train it.


To run an example

```
git clone --depth 1 https://github.com/nyumaya/nyumaya_audio_recognition.git
cd nyumaya_audio_recognition/python 
```
For Raspberry Pi 2/3
```
python streaming_example.py --libpath ../lib/rpi/armv7/libnyumaya.so
```
For Raspberry Pi Zero
```
python streaming_example.py --libpath ../lib/rpi/armv6/libnyumaya.so
```

For Linux
```
python streaming_example.py --libpath ../lib/linux/libnyumaya.so
```

For Mac
```
python streaming_example.py --libpath ../lib/mac/libnyumaya.dylib
```



The demo captures audio from the default microphone. The new version only takes .tflite models.
For each application, different model architectures are available which are a tradeoff between accuracy and cpu/mem usage.

## Model Architectures
- Small model  (CPU Pi0: 20% CPU Pi3 one core: 12%)
- Big model    (CPU Pi0: 95% CPU Pi3 one core: 20%)


## Applications:
- Command Subset (yes,no,up,down,left,right,on,off,stop,follow,play)
- Command Numbers (one,two,three,four,five,six,seven,eight,nine,zero)
- Command Objects (music,radio,television,door,water,computer,temperature,light,house)
- German_commands(an,aus,computer,ein,fernseher,garage,jalousie,licht,musik,oeffnen,radio,rollo,schließen,start,stopp)
- Marvin Hotword (marvin)
- Sheila Hotword (sheila)
- Marvin Sheila Hotword (marvin,sheila)
- Voice-gender (female,male,nospeech)
- Baby-monitor (cry, babble, door-open, music, glass-break, footsteps, fire-alarm)
- Impulse-response (Play tone and interpret echo: Bedroom, Kitchen, Bathroom, Outdoor, Hall, Living Room, Basement)
- Alarm-system (door-open, glass-break, footsteps, fire-alarm, voice)
- Door-monitor (door bell, door knocking, voice)
- Weather (thunder, rain, storm, hail)
- Language detection
- Swear word detection (imagine some unappropriate words)
- Crowd monitoring(screaming, shouting, gunshot, siren, explosion)
- Animal monitoring (dog, cat, chicken, rooster..)

## Pretrained models:
- Marvin Hotword
- Sheila Hotword
- Marvin-Sheila Hotword
- Command Subset
- Command Numbers
- Command Objects (quality is not good yet)

## Audio Config

If your microphone has a DC-Offset (SPH0645) you can enable the option to remove it in software:
```
detector.RemoveDC(True)
```

You can run the audio_check script to get some info about your volume level and possible DC-Offset. Speak as loud as the maximum expected volume will be.
```
python check_audio.py
```

## Chaining Commands

The multi_streaming_example.py should give you a starting point when chaining commands <marvin><start>.

## Compiling the library for your own target:

The source code for building the library can be found [https://github.com/nyumaya/nyumaya_audio_recognition_lib](here).
You will most likely have to modify the CMakeLists.txt 

In order to run the example code on a system wihout arecord you have to create your own recorder. A cross-platform library like python-sounddevice might help. 

You might have to modify the python bindings.

## Roadmap:
- [x] Basic working models
- [X] Average output predictions
- [X] Benchmark accuracy and false recognition rate
- [X] Noisy Benchmark, use more diverse test set (maby musan dataset)
- [ ] Improve Far Field Recognition
- [ ] Benchmark latency
- [ ] Voice activity detection
- [ ] Provide TensorflowLite and TensorflowJS models
- [ ] Web demo
- [ ] Improve Architectures (including RNN and Attention)
- [ ] More Applications 


## Credits:
- [https://github.com/castorini/honk](honk) For inspiration and model ideas
- Peter Warden for releasing the Speech Command Dataset
-  The library uses [https://github.com/mborgerding/kissfft](kissfft)
