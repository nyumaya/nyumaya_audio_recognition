package com.nyumaya.audiorecognition

import android.media.AudioFormat
import android.media.MediaRecorder
import kotlin.concurrent.thread
import android.media.AudioRecord
import java.util.concurrent.locks.ReentrantLock


class AudioRecorder {

    private var doRecord = false
    private var mediaRecorder: AudioRecord? = null

    private var bufferSize = AudioRecord.getMinBufferSize(16000, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT)

    private var RingBufferSize = bufferSize*128
    private var RingBuffer = ByteArray(RingBufferSize)
    private val RingBufferLock = ReentrantLock()
    private var RingBufferReadPos : Int = 0
    private var RingBufferWritePos : Int = 0

    init {
        mediaRecorder = AudioRecord(
            MediaRecorder.AudioSource.MIC,
            16000,
            AudioFormat.CHANNEL_IN_MONO,
            AudioFormat.ENCODING_PCM_16BIT,
            bufferSize
        )
    }


    fun startRecording()
    {
        doRecord = true
        record()
    }

    fun stopRecording(){
        doRecord = false
        mediaRecorder?.stop()
    }

    private fun canReadRingBufferBytes(numBytes: Int):Boolean {
        if (RingBufferReadPos <= RingBufferWritePos) {
            return numBytes <= (RingBufferWritePos - RingBufferReadPos)
        } else {
            val avail = (RingBufferSize - RingBufferReadPos) + RingBufferWritePos
            return numBytes <= avail
        }
    }


    //Non-Blocking read on Ring Buffer

    fun readRingBuffer(numBytes:Int):ByteArray?{

        RingBufferLock.lock();

        //Not enough data for reading
        if(! canReadRingBufferBytes(numBytes)){
            RingBufferLock.unlock();
            return null
        }
        //Can read in one block
        if((RingBufferReadPos + numBytes) <= RingBufferSize){
            val slice = RingBuffer.copyOfRange(RingBufferReadPos,RingBufferReadPos+numBytes)
            RingBufferReadPos += numBytes
            RingBufferLock.unlock();
            return slice
        }

        //Need to concatenate
        val first_part = RingBuffer.copyOfRange(RingBufferReadPos,RingBufferSize) //-1?
        val first_len = (RingBufferSize - RingBufferReadPos)
        val second_len = numBytes - first_len
        val second_part = RingBuffer.copyOfRange(0,second_len) //-1?

        RingBufferReadPos += numBytes
        if(RingBufferReadPos > RingBufferSize) {
            RingBufferReadPos %= RingBufferSize
        }
        val slice = first_part + second_part

        RingBufferLock.unlock();
        return slice
    }


    private fun writeRingBuffer(data:ByteArray,numBytes: Int){
        RingBufferLock.lock();

        //Case A: Read pos was smaller than write pos
        //Case B: Read pos was bigger than write pos

        //Data fitting into remaining buffer
        if((RingBufferWritePos + numBytes) <= RingBufferSize) {
            System.arraycopy(data, 0, RingBuffer, RingBufferWritePos, numBytes)
            RingBufferWritePos += numBytes

        } else{
            //Write first part into buffer
            val first_len = RingBufferSize - RingBufferWritePos
            System.arraycopy(data, 0, RingBuffer, RingBufferWritePos, first_len)

            //Write second part wrapped around
            val second_len = numBytes - first_len
            System.arraycopy(data, first_len, RingBuffer, 0, second_len)

            RingBufferWritePos = second_len
        }

        RingBufferLock.unlock();
    }

    private fun record(){

        mediaRecorder?.startRecording()

        thread(start = true) {
            while(doRecord) {

                //Blocking Read of bufferSize Bytes
                //Buffer Read result returns number of read bytes
                val buffer = ByteArray(bufferSize)
                val bufferReadResult = mediaRecorder?.read(buffer, 0, bufferSize);
                val readBytes = (bufferReadResult ?:0)

                writeRingBuffer(buffer,readBytes)
                //println("Read " + readBytes + " Bytes")
            }
        }
    }
}