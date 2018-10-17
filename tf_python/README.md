# tf_python
This is the deprecated audio recognition software which depends on tensorflow.
Please use the new tensorflow lite based version if possible. 

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
git clone https://github.com/nyumaya/nyumaya_audio_recognition_models.git
```
To run an example
```
python tf_python/streaming_example.py --graph <model_path>/conv-conv/conv-conv_frozen.pb  --labels <model_path>/labels.txt  --sens 0.5
```
On the Pi Zero Tensorflow takes a few seconds to load. The demo captures audio from the default microphone. 

