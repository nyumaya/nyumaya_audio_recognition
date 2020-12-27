
function run_hotword_detection()
{

	const api = {
		version: Module.cwrap('getVersionString', 'string', []),
		createFeatureExtractor: Module.cwrap('createFeatureExtractor', 'number', ['number','number','number','number','number','number','number']),
		signalToMel: Module.cwrap('signalToMel', 'number', ['number','number','number','number']),
		createAudioRecognition: Module.cwrap('createAudioRecognition', 'number', []),
		deleteAudioRecognition: Module.cwrap('deleteAudioRecognition', 'number', ['string']),
		addModel: Module.cwrap( 'addModel', 'number', ['number','string','number','number']),
		setActive: Module.cwrap('setActive','number', ['number','number','number']),
		runDetection: Module.cwrap( 'runDetection', 'number', ['number','number','number']),
		setSensitivity: Module.cwrap( 'setSensitivity', '', ['number','number','number'])
	};

	var detector = api.createAudioRecognition();
	var model_paths = {};

	console.log(api.version());
	FeatureExtractor = api.createFeatureExtractor(512,40,16000,20,8000,0.03,0.01)

	load_file_from_server("alexa_v1.2.0.premium","Alexa");
	load_file_from_server("marvin_v1.2.0.premium","Marvin");
	load_file_from_server("sheila_v1.2.0.premium","Sheila");
	load_file_from_server("firefox_v1.2.0.premium","Firefox");

	//Buffer for drawing frequency spectrogram
	var arrayData = new Array(4800).fill(0);

	//Buffer holding meldata. Used for feeding the
	//mel_slice_sized parts to the detector
	var melLogback = Array()

	//Buffer for passing back meldata from wasm to js
	var mel_result = Module._malloc(2080)

	var first = true //For printing Info once
	var label_index = 0; //FIXME: Temporary while we don't use real keyword ids yet
	var mel_slice_size=800
	var prediction_heap  = Module._malloc(mel_slice_size * 1);
	var pcm_heap = Module._malloc(1600 * 2); //1486


	function save_file_to_storage(data,name,path){
		console.log("Saving Model " + path);
		console.log("DataLen " + data.byteLength);
		var stream = FS.open(path, 'w+');
		var uint8View = new Uint8Array(data);
		FS.write(stream, uint8View, 0, data.byteLength, 0);
		FS.close(stream);
		model_paths[name] = path;
	}

	function load_file_from_server(url,model_name){
		var xhr=new XMLHttpRequest();
		xhr.open("GET","models/Hotword/"+url, true);
		xhr.responseType = 'arraybuffer';
		xhr.addEventListener('load',function(){
			if (xhr.status === 200){
				save_file_to_storage(xhr.response,model_name,url)
				addModel(model_name)
			}
		})
		xhr.send();
	}

	function get_filepath(name){
		return model_paths[name];
	}

	function get_switch(name,checked)
	{
		checked_markup = '">'
		if(checked){
			checked_markup = '" checked>' 
		}
		markup = 	'<div class="onoffswitch">' +
				'<input type="checkbox" name="onoffswitch'+name +
				'" class="onoffswitch-checkbox" id="myonoffswitch' + name +checked_markup +
				'<label class="onoffswitch-label" for="myonoffswitch' + name + '">' + 
				'	<span class="onoffswitch-inner"></span>' + 
				'	<span class="onoffswitch-switch"></span>' +
				'</label></div>'
		return markup
	}

	function get_slider(name)
	{
		markup = '<td><input id="detect_sensitivity'+name+'" type="range" min="0" max="100" step="1" value="50"></td>' +
			'<td><div id="sliderAmount'+name+'">0.5</div></td>'
		return markup
	}

	function append_setting(name,checked,currentIndex)
	{
		console.log("Appending Setting " + name);
		markup =" <tr><td>"+ name + "</td><td>" + get_switch(name,checked) + "</td>" + get_slider(name) + "</tr>"

		$("table tbody").append(markup);

		add_label(name,currentIndex);

		document.getElementById("myonoffswitch"+name).onclick = function() {
			switch_model_active(currentIndex,this.checked);
		};

		var slide = document.getElementById('detect_sensitivity'+name);
		var sliderDiv = document.getElementById("sliderAmount"+name);
	
		slide.onchange = function() {
			sliderDiv.innerHTML = this.value/100.0;
			api.setSensitivity(detector,this.value/100.0,currentIndex);
			console.log("Setting Sensitivity of " + name + " to: " + this.value/100.0)
		}
	}

	function add_label(name,currentIndex)
	{
		console.log("Adding label " + name);
		var div = document.createElement('h1');
		div.className = 'rcorners';
		div.id=currentIndex + "_lbl" ;
		div.innerHTML = name;
		document.getElementById('detectionArea').appendChild(div)
	}

	function switch_model_active(currentIndex,checked)
	{
		console.log("Switching Model Active " + currentIndex + " " + checked);
		api.setActive(detector,checked,currentIndex)
	}

	function remove_label(name)
	{
		console.log("Removing label " + name);
		var lbl_name = (index+1) + "_lbl" ;
		document.getElementById(lbl_name).remove();
	}

	function addModel(name)
	{
		console.log("Adding Model " + name);
		//var modelIndex = label_index;
		label_index = label_index + 1; //FIXME use addModel index
		var modelIndex = 0;
		transfer32ToHeap(pcm_heap,modelIndex);
		success = api.addModel(detector,get_filepath(name),0.5,pcm_heap)
		append_setting(name,true,label_index);

		if(success == 0){
			console.log("Added Model " + name);
		} else {
			console.log("Failed to add Model " + name);
		}

		api.setSensitivity(detector,0.5,label_index);
	}

	function remove_detector(name)
	{
		console.log("Removing Detector " + name);
		delete detectors[name];
	}

	//Extract features from audio
	function set_mel(event)
	{
		var input_buffer = event.inputBuffer.getChannelData(0);
		var resampled = interpolateArray(input_buffer, 16000, event.inputBuffer.sampleRate)
		var pcm_data = floatTo16BitPCM(resampled)

		transfer16ToHeap(pcm_heap,pcm_data)

		var gain = 1.0

		if(first == true){
			console.log("SampleRate: " +  event.inputBuffer.sampleRate)
			console.log("PCMLength: " +  pcm_data.length)
			first = false
		}

		const res = api.signalToMel(FeatureExtractor,pcm_heap,pcm_data.length,mel_result,gain)

		for (let v=0; v<res; v++) {
			arrayData.shift()
			dataelem = Module.HEAPU8[mel_result/Uint8Array.BYTES_PER_ELEMENT+v]
			arrayData.push(dataelem)
			melLogback.push(dataelem)
		}

		draw(arrayData)
	}

	//Use audio, extract features and run detection
	function check_audio(event)
	{
		set_mel(event)

		while(melLogback.length > mel_slice_size)
		{
			var prediction_data = melLogback.slice(0,mel_slice_size)
			transfer8ToHeap(prediction_heap,prediction_data)

			detect()
	
			melLogback.splice(0, mel_slice_size);
		}
	}

	function detect()
	{
		var detectionResult = api.runDetection(detector,prediction_heap,mel_slice_size);

		if(detectionResult != 0){
			console.log("Detected!" + Date.now());
			var beep = document.getElementById("beep");
			beep.play();
			console.log(detectionResult + "_lbl")
			var element = document.getElementById(detectionResult + "_lbl");
			element.classList.remove("trigger-animation");
			void element.offsetWidth;
			element.classList.add("trigger-animation");
		}
	}

	if (!check_media()){
		alert("No media")
	} else {
		start_media(check_audio)
	}
}



function draw(data)
{
	var canvas = document.getElementById("viewport"); 
	var context = canvas.getContext("2d");

	const width = canvas.width;
	const height = canvas.height;
 
	var imagedata = context.createImageData(width, height);
 
	function createImage() {

		for (var x=0; x<width; x++) {
			for (var y=0; y<height; y++) {

				var pixelindex = (x + y * width) * 4;
				var dataindex = (x * height + 40-y );
	
				imagedata.data[pixelindex]   = 255 - data[dataindex] * 2
				imagedata.data[pixelindex+1] = 255 - data[dataindex]
				imagedata.data[pixelindex+2] = 255 - data[dataindex]
				imagedata.data[pixelindex+3] = 255;
			}
		}
	}

	createImage();
	
	context.putImageData(imagedata, 0, 0);
	context.rect(0, 0, width, height);
	context.stroke();
}

//Poor mans way to downsample data to 16000 Hertz
function interpolateArray(data, newSampleRate, oldSampleRate)
{
	const fitCount = Math.round(data.length*(newSampleRate/oldSampleRate));
	var newData = new Array(fitCount);

	const springFactor = (data.length - 1) / (fitCount - 1);

	newData[0] = data[0]; // for new allocation
	for ( var i = 1; i < fitCount - 1; i++) {
		const tmp = i * springFactor;

		const before = Math.floor(tmp);
		const after = Math.ceil(tmp);

		const atPoint = tmp - before;
		const data_before = data[before]
		const data_after = data[after]

		newData[i] = data_before + (data_after - data_before) * atPoint;
		
	}
	newData[fitCount - 1] = data[data.length - 1]; // for new allocation
	return newData;
};

function transfer32ToHeap(heapSpace,arr)
{
	Module.HEAP32.set(arr, heapSpace >> 1);
	return heapSpace;
}

function transfer16ToHeap(heapSpace,arr)
{
	Module.HEAP16.set(arr, heapSpace >> 1);
	return heapSpace;
}

function transfer8ToHeap(heapSpace,arr)
{
	Module.HEAPU8.set(arr, heapSpace);
	return heapSpace;
}


function floatTo16BitPCM(input)
{
	const in_len = input.length
	var newData = new Int16Array(in_len);

	for (var i = 0; i < in_len; i++){
		newData[i] = input[i]*32000;
	}

	return newData
}



function check_media()
{
	if (!navigator.getUserMedia)
		navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia ||
		navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.mediaDevices.getUserMedia;

	if (navigator.getUserMedia){
		return true
	} else {
		return false
	}
}

function start_media(callback)
{
	navigator.getUserMedia({audio:true},
		function(stream) {
			start_microphone(stream,callback);
		},
		function(e) {
			alert('Error capturing audio.');
		}
	);
}

function start_microphone(stream,callback)
{
	window.audioContext = new AudioContext();
	window.gain_node = window.audioContext.createGain();

	window.microphone_stream = window.audioContext.createMediaStreamSource(stream);
	window.microphone_stream.connect(window.gain_node);

	window.script_processor_node = window.audioContext.createScriptProcessor(0, 1, 1);
	console.log("Audio buffer size: " + script_processor_node.bufferSize) 
	window.script_processor_node.onaudioprocess = callback;
	window.microphone_stream.connect(window.script_processor_node);
	window.script_processor_node.connect(window.audioContext.destination)
}



