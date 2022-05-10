
var startRecordingButton = document.getElementById("startRecordingButton");
var stopRecordingButton = document.getElementById("stopRecordingButton");
var playRecordedAudio = document.getElementById("playButton");
var playResult = document.getElementById("resultButton");
var Translate = document.getElementById("send");
var speach_to_Text = document.getElementById("speach-text");
var Text_to_Speach = document.getElementById("text-speach");
var french_text = document.getElementById("transOutput");

var txt = "";
var french_output = "";
var leftchannel = [];
var rightchannel = [];
var recorder = null;
var recordingLength = 0;
var volume = null;
var mediaStream = null;
var sampleRate = 44100;

var context = null;
var blob = null;
var res_blob = null;
var text_blob = null;


function startRecording() {
    sampleRate = 44100;
    res_blob = null;
    text_blob = null;
    french_output = "";
    txt = "";
    blob = null;
    recorder = null;
    context = null;
    mediaStream = null;
    leftchannel = [];
    rightchannel = [];
    recordingLength = 0;
    // var startRecordingButton = document.getElementById("startRecordingButton");
    startRecordingButton.style.backgroundColor = "#ffffff";
    startRecordingButton.style.color = "#FF0000"
    startRecordingButton.style.borderColor = "#000000"
    // Initialize recorder
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    navigator.getUserMedia(
        {
            audio: true
        },
        function (e) {
            console.log("user consent");

            document.getElementById("output").innerHTML = txt;
            document.getElementsByClassName("loader")[0].style.display = "none";
            document.getElementsByClassName("loader")[0].style.display = "none";
            document.getElementById("transOutput").innerHTML = french_output;
            // creates the audio context
            window.AudioContext = window.AudioContext || window.webkitAudioContext;
            context = new AudioContext();

            // creates an audio node from the microphone incoming stream
            mediaStream = context.createMediaStreamSource(e);

            // https://developer.mozilla.org/en-US/docs/Web/API/AudioContext/createScriptProcessor 
            // bufferSize: the onaudioprocess event is called when the buffer is full        
            var bufferSize = 2048;
            var numberOfInputChannels = 2;
            var numberOfOutputChannels = 2;
            if (context.createScriptProcessor) {
                recorder = context.createScriptProcessor(bufferSize, numberOfInputChannels, numberOfOutputChannels);
            } else {
                recorder = context.createJavaScriptNode(bufferSize, numberOfInputChannels, numberOfOutputChannels);
            }

            recorder.onaudioprocess = function (e) {
                leftchannel.push(new Float32Array(e.inputBuffer.getChannelData(0)));
                rightchannel.push(new Float32Array(e.inputBuffer.getChannelData(1)));
                recordingLength += bufferSize;
            }

            // we connect the recorder
            mediaStream.connect(recorder);
            recorder.connect(context.destination);
        },
        function (e) {
            console.error(e);
        });
}



function stopRecording() {

    // stop recording
    if (context == null) {
        alert("first start recording");
        return;
    }
    sampleRate = 44100;
    recorder.disconnect(context.destination);
    mediaStream.disconnect(recorder);


    var leftBuffer = flattenArray(leftchannel, recordingLength);
    var rightBuffer = flattenArray(rightchannel, recordingLength);
    var interleaved = interleave(leftBuffer, rightBuffer);

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
    view.setUint32(24, sampleRate, true); // dwSamplesPerSec
    view.setUint32(28, sampleRate * 4, true); // dwAvgBytesPerSec
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
    blob = new Blob([view], { type: 'audio/wav' });
    startRecordingButton.style.backgroundColor = "#807d7d";
    startRecordingButton.style.color = "#000000"
    var url = window.URL.createObjectURL(blob);
    playRecordedAudio.src = url;

}


async function speachToText(flag) {
    if (blob == null) {
        stopRecording();
    }
    document.getElementsByClassName("loader")[0].style.display = "block";
    var data = new FormData();
    data.append("file", blob);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", 'http://127.0.0.1:8000/speach-text', flag);

    xmlHttp.onprogress = function () {
        console.log("on progress speachToText");
    }
    xmlHttp.onload = function () {
        txt = this.responseText;
        document.getElementById("output").innerHTML = txt;
        document.getElementsByClassName("loader")[0].style.display = "none";
    }
    xmlHttp.send(data);
};

async function EnglishToFrench() {
    if (blob === null) {
        stopRecording();
    }
    if (txt === "") {
        await speachToText(true);
    }
    document.getElementsByClassName("loader")[0].style.display = "block";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", 'http://127.0.0.1:8000/translate', true);
    xmlHttp.onprogress = function () {
        console.log("on progress inside EnglishToFrench");
    }
    xmlHttp.onload = function () {
        french_output = this.responseText
        document.getElementsByClassName("loader")[0].style.display = "none";
        document.getElementById("transOutput").innerHTML = french_output;
    };
    xmlHttp.send(txt);

};
function TextToSpeach() {
    if (french_output == "") {
        alert("First Translate");
        return;
    }
    document.getElementsByClassName("loader")[0].style.display = "block";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onload = function (e) {
        var myBuffer = base64DecToArr(this.response).buffer;
        text_blob = new Blob([myBuffer], { type: 'audio/wav' });
        var url = window.URL.createObjectURL(text_blob);
        var audio = new Audio(url);
        document.getElementsByClassName("loader")[0].style.display = "none";
        audio.play();
    };
    xmlHttp.open("POST", 'http://127.0.0.1:8000/text-speach', async = true);
    xmlHttp.send(french_output);
}


function flattenArray(channelBuffer, recordingLength) {
    var result = new Float32Array(recordingLength);
    var offset = 0;
    for (var i = 0; i < channelBuffer.length; i++) {
        var buffer = channelBuffer[i];
        result.set(buffer, offset);
        offset += buffer.length;
    }
    return result;
}

function interleave(leftChannel, rightChannel) {
    var length = leftChannel.length + rightChannel.length;
    var result = new Float32Array(length);

    var inputIndex = 0;

    for (var index = 0; index < length;) {
        result[index++] = leftChannel[inputIndex];
        result[index++] = rightChannel[inputIndex];
        inputIndex++;
    }
    return result;
}

function writeUTFBytes(view, offset, string) {
    for (var i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
    }
}





