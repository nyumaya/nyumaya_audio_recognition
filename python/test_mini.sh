if [[ "$OSTYPE" == "linux-gnu" ]]; then

    if [ "$(uname -m | grep x86_64 -c)" -eq 1 ]; then
        echo "Check for X86_64"
        LIBPATH="../lib/linux/libnyumaya.so"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
     echo "Check for OSX"
     LIBPATH="/usr/local/lib/libnyumaya.dylib"

elif [[ "$OSTYPE" == "linux-gnueabihf" ]]; then

    if [ "$(uname -m | grep armv6l -c)" -eq 1 ]; then
        echo "Check for PiZero"
        LIBPATH="../lib/rpi/armv6/libnyumaya.so"
    fi

    if [ "$(uname -m | grep armv7l -c)" -eq 1 ]; then
        echo "Check for Pi3"
        LIBPATH="../lib/rpi/armv7/libnyumaya.so"
    fi

else
    echo "Unknown OS: $OSTYPE"
    exit
fi



python test_accuracy.py --graph ../models/Hotword/marvin_small_0.3.tflite \
                        --labels ../models/Hotword/marvin_labels.txt \
                        --good_folder ../../nyumaya_audio_testdata/nyumaya_marvin_test_0.1/nyumaya_marvin_ff_test/marvin \
                        --noise_folders ../../nyumaya_audio_testdata/nyumaya_mic_noise \
                        --bad_folders "../../nyumaya_audio_testdata/cv_mini,../../nyumaya_audio_testdata/nyumaya_mic_noise" \
                        --libpath $LIBPATH
                        
python3 test_accuracy.py --graph ../models/Hotword/marvin_small_0.3.tflite \
                        --labels ../models/Hotword/marvin_labels.txt \
                        --good_folder ../../nyumaya_audio_testdata/nyumaya_marvin_test_0.1/nyumaya_marvin_ff_test/marvin \
                        --noise_folders ../../nyumaya_audio_testdata/nyumaya_mic_noise \
                        --bad_folders "../../nyumaya_audio_testdata/cv_mini,../../nyumaya_audio_testdata/nyumaya_mic_noise" \
                        --libpath $LIBPATH
