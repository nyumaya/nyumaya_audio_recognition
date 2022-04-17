# Detect simple voice commands and audio events on small embedded sytems
Nyumaya offline audio classification. Libraries are avialable for **Linux**, **WASM** and **RaspberryPi**.

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fa3ffbfff7fa4554acad93e044b24fdd)](https://www.codacy.com/gh/nyumaya/nyumaya_audio_recognition/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=nyumaya/nyumaya_audio_recognition&amp;utm_campaign=Badge_Grade)

To run an example

```
git clone --depth 1 https://github.com/nyumaya/nyumaya_audio_recognition.git
cd nyumaya_audio_recognition/examples/python
python3 simple_hotword.py
```

The python demo captures audio from the default alsa microphone.


## Web Demo

A web demo is available [here](https://nyumaya.com/demo/). 
This has been tested with recent versions of Chrome and Firefox.

## Performance V3.0

- Pi Zero: CPU 55%
- Pi 3: CPU one core: 12%
- Pi 4: CPU one core: 4%


## Free models:

- Marvin Hotword
- Sheila Hotword
- Firefox Hotword
- Alexa Hotword
- View Glass Hotword

## Versioning

Models and the Library are Versioned with \<major\>.\<minor\>.\<revision\>
Models must match the \<major\>.\<minor\> version of the library to be compatible.

## Sensitivity

The sensitivity parameter is a tradeoff between accuracy and false positives. Setting the sensitivity to a high value means it's easier to trigger the hotword. If you experience a lot of false detections, set the sensitivity to a lower value.


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
Be aware that CPU usage increases a little bit when multiple models have to run concurrently. I this case the software has to run
the marvin_model (marvin) and the subset_model (stop) at the same time.
```
mDetector.add_command("marvin,on",light_on)
mDetector.add_command("stop",stop)
```

## Custom Keywords:

Custom Keywords can be requested for evalutaion and commercial use [here](https://nyumaya.com/requesting-custom-keywords/)

## Custom Targets:

Libraries for other targets can be requested for commercial customers.



