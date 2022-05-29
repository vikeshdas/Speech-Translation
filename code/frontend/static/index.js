
/**
* methods of this model hit the flask API from the front end when the button is * clicked to translate and transcribe
*/
 
let startRecordingButton;
let stopRecordingButton;
let playRecordedAudio;
let playResult;
let Translate;
let speech_to_Text;
let Text_to_speech;
let french_text;

/*
* this class initialize all the varibles
*/ 
class JsClass {
    constructor() {
        this.isrecorded = false;
        this.isrecording = false;
        this.txt = "";
        this.french_output = "";
        this.leftchannel = [];
        this.rightchannel = [];
        this.recorder = null;
        this.recordingLength = 0;
        this.volume = null;
        this.mediaStream = null;
        this.sampleRate = 44100;

        this.context = null;
        this.blob = null;
        this.res_blob = null;
        this.text_blob = null;
    }
}


/**
* This function gets media permission and starts recording, recording is done
* in stereo form
*/

function startRecording() {
    obj.sampleRate = 44100;
    obj.res_blob = null;
    obj.text_blob = null;
    obj.french_output = "";
    obj.txt = "";
    obj.blob = null;
    obj.recorder = null;
    obj.context = null;
    obj.mediaStream = null;
    obj.leftchannel = [];
    obj.rightchannel = [];
    obj.recordingLength = 0;
    obj.isrecording = true;
    obj.isrecorded = true;

    startRecordingButton.style.backgroundColor = "#ffffff";
    startRecordingButton.style.color = "#FF0000"
    startRecordingButton.style.borderColor = "#000000"

    // startRecordingButton.classList.add("onstartButton");
    //  startRecordingButton.className="onstartButton"; 
    // Initialize recorder
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    navigator.mediaDevices.getUserMedia(
        {
            audio: true
        }).then(
            function (e) {
                document.getElementById("output").innerHTML = obj.txt;
                document.getElementsByClassName("loader")[0].style.display = "none";
                document.getElementsByClassName("loader")[0].style.display = "none";
                document.getElementById("transOutput").innerHTML = obj.french_output;
                // creates the audio context
                window.AudioContext = window.AudioContext || window.webkitAudioContext;
                obj.context = new AudioContext();

                // creates an audio node from the microphone incoming stream
                obj.mediaStream = obj.context.createMediaStreamSource(e);

                var bufferSize = 2048;
                var numberOfInputChannels = 2;
                var numberOfOutputChannels = 2;
                if (obj.context.createScriptProcessor) {
                    obj.recorder = obj.context.createScriptProcessor(bufferSize, numberOfInputChannels, numberOfOutputChannels);
                } else {
                    obj.recorder = obj.context.createJavaScriptNode(bufferSize, numberOfInputChannels, numberOfOutputChannels);
                }

                obj.recorder.onaudioprocess = function (e) {
                    obj.leftchannel.push(new Float32Array(e.inputBuffer.getChannelData(0)));
                    obj.rightchannel.push(new Float32Array(e.inputBuffer.getChannelData(1)));
                    obj.recordingLength += bufferSize;
                }

                // we connect the recorder
                obj.mediaStream.connect(obj.recorder);
                obj.recorder.connect(obj.context.destination);
            }).then(
                function (e) {
                    console.error(e);
                });

}


/**
 * method stop recording if recording is being done and makes blob object of
 * recorded audio
 */
function stopRecording() {
    if (obj.isrecording === false) {
        alert("first start recording");
        return 1;
    }
    // sampleRate = 44100;
    obj.isrecording = false
    obj.recorder.disconnect(obj.context.destination);
    obj.mediaStream.disconnect(obj.recorder);

    var leftBuffer = new Float32Array(obj.recordingLength);
    var offset = 0;
    for (var i = 0; i < obj.leftchannel.length; i++) {
        var buffer = obj.leftchannel[i];
        leftBuffer.set(buffer, offset);
        offset += buffer.length;
    }
    var rightBuffer = new Float32Array(obj.recordingLength);
    var offset = 0;
    for (var i = 0; i < obj.rightchannel.length; i++) {
        var buffer = obj.rightchannel[i];
        rightBuffer.set(buffer, offset);
        offset += buffer.length;
    }

    var length = leftBuffer.length + rightBuffer.length;
    interleaved = new Float32Array(length);

    var inputIndex = 0;

    for (var index = 0; index < length;) {
        interleaved[index++] = leftBuffer[inputIndex];
        interleaved[index++] = rightBuffer[inputIndex];
        inputIndex++;
    }

    // we create our wav file
    var buffer = new ArrayBuffer(44 + interleaved.length * 2);
    var view = new DataView(buffer);

    // RIFF chunk descriptor
    writeUTFBytes(view, 0, 'RIFF');
    view.setUint32(4, 44 + interleaved.length * 2, true);
    writeUTFBytes(view, 8, 'WAVE');
    // FMT sub-chunk
    writeUTFBytes(view, 12, 'fmt ');
    view.setUint32(16, 16, true); // chunkSize
    view.setUint16(20, 1, true); // wFormatTag
    view.setUint16(22, 2, true); // wChannels: stereo (2 channels)
    // view.setUint16(22, 1, true); // wChannels: mono (1 channel)
    view.setUint32(24, obj.sampleRate, true); // dwSamplesPerSec
    view.setUint32(28, obj.sampleRate * 4, true); // dwAvgBytesPerSec
    view.setUint16(32, 4, true); // wBlockAlign
    view.setUint16(34, 16, true); // wBitsPerSample
    // data sub-chunk
    writeUTFBytes(view, 36, 'data');
    view.setUint32(40, interleaved.length * 2, true);

    // write the PCM samples
    var index = 44;
    var volume = 1;
    for (var i = 0; i < interleaved.length; i++) {
        view.setInt16(index, interleaved[i] * (0x7FFF * volume), true);
        index += 2;
    }

    // our final blob
    obj.blob = new Blob([view], { type: 'audio/wav' });
    startRecordingButton.style.backgroundColor = "#807d7d";
    startRecordingButton.style.color = "#000000"
    var url = window.URL.createObjectURL(obj.blob);
    playRecordedAudio.src = url;
    isrecorded = true;

}


/**
 * method hit flask api with recorded audio blob object using 
 * XMLHttpRequest() which convert recorded sound to text
 * @param {boolean} for asynchronous request 
 */

async function speechToText(flag) {
    if (obj.isrecording === true) {
        stopRecording();

    }
    if (obj.isrecorded === false) {
        window.alert("recording is not started yet");
    }
    document.getElementsByClassName("loader")[0].style.display = "block";
    var data = new FormData();
    data.append("file", obj.blob);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", 'http://127.0.0.1:8000/speech-text', flag);

    xmlHttp.onprogress = function () {
        console.log("on progress speechToText");
    }
    xmlHttp.onload = function () {
        obj.txt = this.responseText;
        document.getElementById("output").innerHTML = obj.txt;
        document.getElementsByClassName("loader")[0].style.display = "none";
    }
    xmlHttp.send(data);
};


/**
 * method hit flask api with english sentence in string form using 
 * XMLHttpRequest() which translate english sentence to french sentence
 */
async function EnglishToFrench() {

    if (obj.isrecording === true)
        stopRecording();
    if (obj.isrecorded === false) {
        window.alert("recording is not started yet");
        return;
    }

    document.getElementsByClassName("loader")[0].style.display = "block";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", 'http://127.0.0.1:8000/translate', true);
    xmlHttp.onprogress = function () {
        console.log("on progress inside EnglishToFrench");
    }
    xmlHttp.onload = function () {
        obj.french_output = this.responseText
        document.getElementsByClassName("loader")[0].style.display = "none";
        document.getElementById("transOutput").innerHTML = obj.french_output;
    };
    xmlHttp.send(obj.txt);
};

/**
 * method hit flask api with french text  using XMLHttpRequest() which 
 * convert french sentence to english sentece
 * @param {boolean} for asynchronous request 
 */

function TextTospeech() {
    if (obj.isrecording === true)
        stopRecording();
    if (obj.isrecorded === false) {
        window.alert("recording is not started yet");
        return;
    }
    if (obj.french_output === "") {
        alert("First Translate");
        return;
    }
    document.getElementsByClassName("loader")[0].style.display = "block";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onload = function (e) {
        var myBuffer = base64DecToArr(this.response).buffer;
        obj.text_blob = new Blob([myBuffer], { type: 'audio/wav' });
        var url = window.URL.createObjectURL(obj.text_blob);
        var audio = new Audio(url);
        document.getElementsByClassName("loader")[0].style.display = "none";
        audio.play();
    };
    xmlHttp.open("POST", 'http://127.0.0.1:8000/text-speech', async = true);
    xmlHttp.send(obj.french_output);
}


/**
 * store an unsigned 8-bit integer at the specified location i.e, at byte
 * offset from the start of the dataView. 
 * @param {object} view 
 * @param {integer} offset 
 * @param {string} string 
 */
function writeUTFBytes(view, offset, string) {
    for (var i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
    }
}


let obj = new JsClass();

window.addEventListener('load', (event) => {
    
    startRecordingButton = document.getElementById("startRecordingButton");
    stopRecordingButton = document.getElementById("stopRecordingButton");
    playRecordedAudio = document.getElementById("playButton");
    playResult = document.getElementById("resultButton");
    Translate = document.getElementById("send");
    speech_to_Text = document.getElementById("speech-text");
    Text_to_speech = document.getElementById("text-speech");
    french_text = document.getElementById("transOutput");


    startRecordingButton.addEventListener("click", startRecording);
    stopRecordingButton.addEventListener("click", stopRecording);
    Translate.addEventListener("click", EnglishToFrench);
    speech_to_Text.addEventListener("click", speechToText);
    Text_to_speech.addEventListener("click", TextTospeech);

});











