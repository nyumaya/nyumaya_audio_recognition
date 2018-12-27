# Detect simple voice commands and audio events on small embedded sytems like the PiZero.
Classify audio with neural nets on embedded systems like the Raspberry Pi using Tensorflow. This should run on any Linux system fine, on other platforms you might have to compile the library yourself.

[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/nyumaya_audio_recognition)

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


The demo captures audio from the default microphone.
For each application, different model architectures are available which are a tradeoff between accuracy and cpu/mem usage.



## Model Architectures
- Small model  (CPU Pi0: 20% CPU Pi3 one core: 12%)
- Big model    (CPU Pi0: 62% CPU Pi3 one core: 20%)

## Applications 

I compiled a list of project ideas [here](https://nyumaya.com/project-ideas-for-audio-machine-learning/)

## Models:
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

If you need a special combination of audio classes or model architecture trained create an issue and I will try to prioritize or train it. All models contain a result file wich describes the false positive/accuracy tradeoff. 

## Sensitivity

The sensitivity parameter is a tradeoff between accuracy and false positives. Setting the sensitivity to a high value means it's easier to trigger the hotword. If you experience a lot of false detections, set the sensitivity to a lower value. 

All models have a corresponding result.txt file where the test results are captured. A False predictions per hour value of 0 doesn't mean that no false prediction will ever occur. It just means that during the test (~5 hours of audio, mostly speech) no false prediction occured.

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

The multi_streaming_example.py is a demo of how to chain commands.
You can add commands with a list of words and function to call when the command is detected.
```
mDetector.add_command("marvin,on",light_on)
mDetector.add_command("marvin,stop",stop)
```
Be aware that CPU usage increases when multiple models have to run concurrently. I this case the software has to run
the marvin_model (marvin) and the subset_model (stop) at the same time.
```
mDetector.add_command("marvin,on",light_on)
mDetector.add_command("stop",stop)
```

## Compiling the library for your own target:

The source code for building the library can be found [here](https://github.com/nyumaya/nyumaya_audio_recognition_lib).
You will most likely have to modify the CMakeLists.txt 

In order to run the example code on a non linux system you can use change the example code to include cross_record instead of record.

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
- [honk](https://github.com/castorini/honk) For inspiration and model ideas
- Peter Warden for releasing the Speech Command Dataset
-  The library uses [kissfft](https://github.com/mborgerding/kissfft)
