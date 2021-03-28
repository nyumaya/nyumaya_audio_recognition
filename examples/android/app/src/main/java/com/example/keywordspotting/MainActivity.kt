package com.example.keywordspotting

import android.Manifest
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.ServiceConnection
import android.content.pm.PackageManager
import android.media.MediaPlayer
import android.os.Bundle
import android.os.IBinder
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.google.android.material.snackbar.Snackbar
import com.nyumaya.audiorecognition.nyumaya_listener
import kotlinx.android.synthetic.main.activity_main.*


class MainActivity : AppCompatActivity() {

    private val RECORD_REQUEST_CODE = 101
    private var mp: MediaPlayer ? = null

    private fun requestPermission(){
        ActivityCompat.requestPermissions(this,
            arrayOf(Manifest.permission.RECORD_AUDIO),
            RECORD_REQUEST_CODE)
    }

    fun keywordDetectedCallback(keywordID:Int)
    {
        println("keywordDetectedCallback: " + keywordID)
        mp?.start()
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        when (requestCode) {
            RECORD_REQUEST_CODE -> {

                if (grantResults.isEmpty() || grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(this,"Permission Denied",Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this,"Permission Granted",Toast.LENGTH_SHORT).show()
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
        mp = MediaPlayer.create(this, R.raw.ding)

        requestPermission()

        startService(Intent(this, nyumaya_listener::class.java))

        var myService: nyumaya_listener? = null
        var isBound = false

        val myConnection = object : ServiceConnection {
            override fun onServiceConnected(className: ComponentName,
                                            service: IBinder) {
                val binder = service as nyumaya_listener.nyumaya_listener_binder
                myService = binder.getService()
                isBound = true
                myService?.setDetectedCallback(::keywordDetectedCallback)
                myService?.listen()
            }

            override fun onServiceDisconnected(name: ComponentName) {
                isBound = false
            }
        }

        val intent = Intent(this, nyumaya_listener::class.java)
        bindService(intent, myConnection, Context.BIND_AUTO_CREATE)
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
