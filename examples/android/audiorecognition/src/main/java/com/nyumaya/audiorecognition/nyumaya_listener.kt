package com.nyumaya.audiorecognition

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.os.Binder
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import kotlin.concurrent.thread


class nyumaya_listener : Service() {

    private val nyumayaBinder = nyumaya_listener_binder()
    private var audioRecorder = AudioRecorder()
    private var nyumayaLib = NyumayaLibrary()
    private var featureExtractor = FeatureExtractor(nyumayaLib)
    private var audioRecognizer = AudioRecognition(nyumayaLib)
    val CHANNEL_ID = "ForegroundServiceChannel"
    private var detectedCallback : ((Int) -> Unit)? = null

    override fun onBind(intent: Intent): IBinder? {
        println("Listener Service on Bind")
        return nyumayaBinder
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val serviceChannel = NotificationChannel(
                CHANNEL_ID,
                "Foreground Service Channel",
                NotificationManager.IMPORTANCE_DEFAULT
            )
            val manager = getSystemService(
                NotificationManager::class.java
            )
            manager.createNotificationChannel(serviceChannel)
        }
    }
    override fun onStartCommand(intent: Intent?, flags: Int,
                                startId: Int): Int {
        createNotificationChannel()
        val pendingIntent = PendingIntent.getActivity(this, 0, intent, 0)
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Nyumaya Service")
            .setContentText("Listening for Hotword")
            .setSmallIcon(R.drawable.ic_android_24dp)
            .setContentIntent(pendingIntent)
            .build()
        startForeground(1, notification)

        return START_STICKY
    }

    inner class nyumaya_listener_binder : Binder() {
        fun getService() : nyumaya_listener {
            return this@nyumaya_listener
        }
    }

    //FIXME: Add keword spotted callback
    fun setDetectedCallback(cb:(keywordId: Int) ->  Unit){
        detectedCallback = cb
    }

    fun listen(){
        //Detection Thread
        thread(start = true) {

            val modelData = application.assets.open("alexa_v3.0.35.premium").readBytes()

            println("Model Data Len =  " + modelData.size)

            val modelNumber = audioRecognizer.addModelFromBuffer(modelData)

            println("Added Model Number " + modelNumber)

            audioRecognizer.setSensitivity(0.5F,modelNumber)
            println("Set Model " + modelNumber + " Sensitivity to 0.5")
            audioRecognizer.setActive(false,modelNumber)
            println("Set Model " + modelNumber + " Active to false")
            audioRecognizer.setActive(true,modelNumber);
            println("Set Model " + modelNumber + " Active to true")

            //var melCount = featureExtractor.getMelcount()
            val recordSize = 6400 //audioRecognizer.getInputDataSize()*2
            nyumayaLib.printVersion()
            audioRecorder.startRecording()
            while(true) {

                val audioBuffer = audioRecorder.readRingBuffer(recordSize)

                if(audioBuffer != null) {
                    val mels = featureExtractor.signalToMel(audioBuffer, 1.0F)
                    val result = audioRecognizer.runDetection(mels)

                    if(result != 0) {
                        detectedCallback?.invoke(result)
                    }
                    //FIXME: Remove Sleep after Reading Ring Buffer is blocking
                    Thread.sleep(100)
                } else {
                    Thread.sleep(100)
                    //println("Failed to read audio Buffer")
                }
            }
        }
    }

}





