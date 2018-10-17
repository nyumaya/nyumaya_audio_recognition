# nyumaya_audio_recognition Lite

Experimental implementation of nyumaya audio recognition without any dependencies.
Currently prebuilt libraries for Ubuntu 64bit Raspberry Pi3 and Raspberry Pi0 are available.
This implementation is still slightly slower than the tensorflow python implementation, but loading time is much much faster. 

To compile the example programs for your architecture you need to modify the line LINK_DIRECTORIES(../lib/linux) in the CmakeLists.txt to point
to your architecture.

In order to compile this you need Cmake
 ```
 sudo apt-get install cmake
 cmake ./
 make
 ```


