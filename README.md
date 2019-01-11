# Detect simple voice commands and audio events on small embedded sytems like the PiZero.
Classify audio with neural nets on embedded systems like the Raspberry Pi using Tensorflow. Libraries are avialable for **Linux**,**OSX** and **RaspberryPi**. For other platforms you will have to compile the library yourself.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0402219fb22244feb10c04d4befcf3dc)](https://app.codacy.com/app/yodakohl/nyumaya_audio_recognition?utm_source=github.com&utm_medium=referral&utm_content=nyumaya/nyumaya_audio_recognition&utm_campaign=Badge_Grade_Dashboard)
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/nyumaya_audio_recognition)
[![GitHub Release](https://github-basic-badges.herokuapp.com/release/nyumaya/nyumaya_audio_recognition.svg)]()
[![Build Status](https://travis-ci.org/nyumaya/nyumaya_audio_recognition.svg?branch=master)](https://travis-ci.org/nyumaya/nyumaya_audio_recognition)

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
- Small model  (CPU Pi0: 20% CPU Pi3 one core: 6%)
- Big model    (CPU Pi0: 62% CPU Pi3 one core: 13%)

## Applications 

I compiled a list of project ideas [here](https://nyumaya.com/project-ideas-for-audio-machine-learning/)

## Planned Models:

- Command Objects (music,radio,television,door,water,computer,temperature,light,house)
- German_commands(an,aus,computer,ein,fernseher,garage,jalousie,licht,musik,oeffnen,radio,rollo,schließen,start,stopp)
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
- Speaker Verification

If you need a special combination of audio classes or model architecture trained create an issue and I will try to prioritize or train it.

## Pretrained models:
- Marvin Hotword (marvin)
- Sheila Hotword (sheila)
- Marvin Sheila Hotword (marvin,sheila)
- Command Subset (yes,no,up,down,left,right,on,off,stop,follow,play)
- Command Numbers (one,two,three,four,five,six,seven,eight,nine,zero)


## Sensitivity

The sensitivity parameter is a tradeoff between accuracy and false positives. Setting the sensitivity to a high value means it's easier to trigger the hotword. If you experience a lot of false detections, set the sensitivity to a lower value. 
All models have a corresponding result.txt file where the test results for different sensitivities are captured. A False predictions per hour value of 0 doesn't mean that no false prediction will ever occur. It just means that during the test (~5 hours of audio, mostly speech) no false prediction occured.

## Audio Config

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


## Credits:
- [honk](https://github.com/castorini/honk) For inspiration and model ideas
- Peter Warden for releasing the Speech Command Dataset
-  The library uses [kissfft](https://github.com/mborgerding/kissfft)
