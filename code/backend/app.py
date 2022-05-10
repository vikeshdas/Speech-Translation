from asyncore import read
from crypt import methods
import imp
from sys import flags
from telnetlib import DO
from time import sleep
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import base64
from google.cloud import speech
from google.cloud import texttospeech
import sys
from SentencePrediction import MainClass


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/jai/Documents/projects/translator/jai-dev-mlconsole-poc.json"

app = Flask(__name__)
md=MainClass()
CORS(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})


def speech_to_text(audio_bytes):
    speech_client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        language_code="en-US",
    )

    response = speech_client.recognize(
        config=config, audio=audio)  # hit the api

    # get the transcription
    transcription_list = []
    for result in response.results:
        transcription_list.append(result.alternatives[0].transcript)
       
    transcription = " ".join(transcription_list)
    return transcription


def text_to_speech(french_text):
    # Instantiates a client
    text_client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=french_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = text_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # # The response's audio_content is binary.
    # with open("output.mp3", "wb") as out:
    #     # Write the response to the output file.
    #     out.write(response.audio_content)
    #     print('Audio content written to file "output.mp3"')
    return response.audio_content

@app.route("/text-speach",methods=['POST'])
def text_to_speach_conversion():
    txt=request.data
    speach=text_to_speech(str(txt))
   
    return base64.b64encode(speach)


@app.route("/speach-text", methods=['POST','GET'])
def func1():
    
    f = request.files['file']


    with open('audio.wav', 'wb') as audio:
        f.save(audio)



    with subprocess.Popen("ffmpeg -i audio.wav -ac 1 mono.wav -y",
                         stdout=subprocess.PIPE, shell=True) as proc:
        pass
    
    with open('mono.wav', 'rb') as audio:
        audio_bytes = audio.read()
    

    transcribed_text = speech_to_text(audio_bytes)

    return transcribed_text

@app.route("/translate", methods=['POST','GET'])
def func():
    sentence=request.data
    sentence = sentence.decode()
    print("SENTENCE IS :",sentence)
    sentence=md.predictsentence(sentence)
    return sentence;



if __name__ == '__main__':
    app.run(debug=True, port = 8000)


"""
TODO
 -> play the response back on frontend
 -> remove the usage of ffmpeg by using mono audio -> either do in js frontend before making request or do at backend in python
"""
