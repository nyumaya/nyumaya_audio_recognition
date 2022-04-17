package com.nyumaya.audiorecognition


class NyumayaLibrary {

    init {
        System.loadLibrary("nyumaya_premium")
    }

    external fun getVersionString(): String

    external fun createFeatureExtractor(nfft:Int=1024,melcount:Int=80,sample_rate:Int=16000,
                                        lowerf:Int=50,upperf:Int=4000,window_len:Float=0.03F,shift:Float=0.01F): Long

    external fun deleteFeatureExtractor(impl:Long)

    external fun createAudioRecognition() :Long

    external fun deleteAudioRecognition(impl:Long)

    external fun signalToMel(impl:Long, pcm:ByteArray, gain:Float) :ByteArray

    external fun getMelcount(impl:Long) :Int

    external fun setSensitivity(impl:Long, sensitivity:Float, modelNumber:Int)

    external fun getInputDataSize(impl:Long) :Int

    external fun runDetection(impl:Long, data:ByteArray):Int

    external fun addModelFromBuffer(impl:Long, data:ByteArray):Int

    external fun addModel(impl:Long, path:String, sensitivity: Float):Int

    external fun setActive(impl:Long, active:Boolean, modelNumber:Int):Int

    external fun deleteModel(impl:Long, modelNumber:Int):Int

    fun printVersion() {
        println(getVersionString())
    }
}


class FeatureExtractor(n:NyumayaLibrary){

    private var nlib:NyumayaLibrary = n
    private var fpointer:Long = 0

    init {
        fpointer = nlib.createFeatureExtractor()
    }

    fun signalToMel(pcm:ByteArray,gain:Float):ByteArray{
        return nlib.signalToMel(fpointer,pcm,gain)
    }

    fun getMelcount():Int{
        return nlib.getMelcount(fpointer)
    }

    protected fun finalize() {
        nlib.deleteFeatureExtractor(fpointer)
    }

}

class AudioRecognition(n:NyumayaLibrary){

    private var nlib:NyumayaLibrary = n
    private var fpointer:Long = 0

    init
    {
        fpointer = nlib.createAudioRecognition()
    }

    fun addModel(mpath:String, sensitivity:Float): Int
    {
        return nlib.addModel(fpointer,mpath,sensitivity)
    }

    fun setActive(active:Boolean, modelNumber:Int):Int
    {
        return nlib.setActive(fpointer,active,modelNumber)
    }

    fun deleteModel(modelNumber:Int):Int
    {
        return nlib.deleteModel(fpointer,modelNumber)
    }

    fun addModelFromBuffer(data:ByteArray):Int {
        return nlib.addModelFromBuffer(fpointer,data)
    }

    //Number of 16 bit samples means 6400 bytes
    fun getInputDataSize(): Int {
        return 2600
        //return nlib.getInputDataSize(fpointer)
    }

    fun runDetection(data:ByteArray): Int {
        return nlib.runDetection(fpointer,data)
    }

    fun setSensitivity(sensitivity:Float, modelNumber:Int) {
        return nlib.setSensitivity(fpointer,sensitivity,modelNumber)
    }

    protected fun finalize() {
        nlib.deleteAudioRecognition(fpointer)
    }

}



