# Detect simple voice commands and audio events on small embedded sytems like the PiZero.
Classify audio with neural nets on embedded systems like the Raspberry Pi using Tensorflow. Libraries are avialable for **Linux**,**OSX**, **Android** and **RaspberryPi**. For other platforms you will have to compile the library yourself.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0402219fb22244feb10c04d4befcf3dc)](https://app.codacy.com/app/yodakohl/nyumaya_audio_recognition?utm_source=github.com&utm_medium=referral&utm_content=nyumaya/nyumaya_audio_recognition&utm_campaign=Badge_Grade_Dashboard)
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/nyumaya_audio_recognition)
[![GitHub Release](https://github-basic-badges.herokuapp.com/release/nyumaya/nyumaya_audio_recognition.svg)]()
[![Build Status](https://travis-ci.org/nyumaya/nyumaya_audio_recognition.svg?branch=master)](https://travis-ci.org/nyumaya/nyumaya_audio_recognition)

To run an example

```
git clone --depth 1 https://github.com/nyumaya/nyumaya_audio_recognition.git
cd nyumaya_audio_recognition/python 
python streaming_example.py
```

The demo captures audio from the default microphone.
For each application, different model architectures are available which are a tradeoff between accuracy and cpu/memory usage.

## WebDemo

An experimental web demo is available [here](https://nyumaya.com/demo/). 
This has been tested with recent versions of Chrome and Firefox.

## Model Architectures
- Small model  (CPU Pi0: 20% CPU Pi3 one core: 6%)
- Big model    (CPU Pi0: 62% CPU Pi3 one core: 13%)



## Pretrained free models:
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

Supporting a new platform is very easy. After compiling the library and moving it to lib/<myboard> you have to modify the file src/auto_platform.py . You can run the script with python auto_platform.py and it will output your system and machine information. All you have to do is setting the default library path and wether to use arecord or pydub as audio source.

You might have to modify the python bindings.

## Feature Requests:
[![Feature Requests](http://feathub.com/nyumaya/nyumaya_audio_recognition?format=svg)](http://feathub.com/nyumaya/nyumaya_audio_recognition)




