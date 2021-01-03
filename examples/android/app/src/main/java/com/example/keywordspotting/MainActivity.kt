package com.example.keywordspotting

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.core.app.ActivityCompat

import com.nyumaya.audiorecognition.AudioRecognition
import com.nyumaya.audiorecognition.FeatureExtractor
import com.nyumaya.audiorecognition.NyumayaLibrary


import kotlinx.android.synthetic.main.activity_main.*
import kotlin.concurrent.thread

class MainActivity : AppCompatActivity() {

    private val RECORD_REQUEST_CODE = 101
    private var audioRecorder = AudioRecorder()
    private var nyumayaLib = NyumayaLibrary()
    private var featureExtractor = FeatureExtractor(nyumayaLib)
    private var audioRecognizer = AudioRecognition(nyumayaLib)

    private fun requestPermission(){
        ActivityCompat.requestPermissions(this,
            arrayOf(Manifest.permission.RECORD_AUDIO),
            RECORD_REQUEST_CODE)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        when (requestCode) {
            RECORD_REQUEST_CODE -> {

                if (grantResults.isEmpty() || grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(this,"Permission Denied",Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this,"Permission Granted",Toast.LENGTH_SHORT).show()
                    audioRecorder.startRecording()
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(toolbar)

        fab.setOnClickListener { view ->
            Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                    .setAction("Action", null).show()
        }

        requestPermission()

        //Detection Thread
        thread(start = true) {

            var modelData = application.assets.open("alexa_v1.2.0.premium").readBytes()

            println("Model Data Len =  " + modelData.size)

            var modelNumber = audioRecognizer.addModelFromBuffer(modelData)

            println("Added Model Number" + modelNumber)

            audioRecognizer.setSensitivity(0.5F,modelNumber)
            //var melCount = featureExtractor.getMelcount()
            var recordSize = 6400 //audioRecognizer.getInputDataSize()*2
            nyumayaLib.printVersion()

            while(true) {

                var audioBuffer = audioRecorder.readRingBuffer(recordSize)

                if(audioBuffer != null) {
                    //println("SUCCESSFULLY READ audio Buffer")
                    var mels = featureExtractor.signalToMel(audioBuffer, 1.0F)
                    //println("MEL SIZE: " + mels.size )
                    var result = audioRecognizer.runDetection(mels)

                    if(result != 0)
                        println("Detection result: " + result)

                    //FIXME: Remove Sleep after Reading Ring Buffer is blocking
                    Thread.sleep(100)
                } else {
                    Thread.sleep(100)
                    //println("Failed to read audio Buffer")
                }
            }
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }
}
