"""
    model have translate english to french, speech to text conversion, text to text conversion methods,these methods are used by flask api for english to french translation
"""

import base64
from flask import request
from google.cloud import speech
from google.cloud import texttospeech
from pydub import AudioSegment
import tensorflow as tf

import config
from prediction import Prediction


class Load:

    """
       Load the trained model form disk and create object of Prediction calss to translate english to french 
    """
    def __init__(self):
        self.text_client = texttospeech.TextToSpeechClient()
        self.speech_client = speech.SpeechClient()
        self.model = tf.keras.models.load_model("../../trained_model")
        self.pred_object = Prediction()

    def text_to_speech_conversion(self):
        """
            route for text to speech conversion, convert rquested french text to speech using google textToSpeech Api

            :return:
                :byte: bytes of converted speech from french_text
        """
        txt = str(request.data)
        synthesis_input = texttospeech.SynthesisInput(text=txt)
        voice = texttospeech.VoiceSelectionParams(language_code=config.
                                                  language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3)

        response = self.text_client.synthesize_speech(input=synthesis_input,
                   voice=voice,
                                                 audio_config=audio_config)
        return base64.b64encode(response.audio_content)

    def speech_to_text(self, audio_bytes):
        """
            converts input audio bytes to text using google speech to text api

            Args:
                audio_bytes: bytes object that needs to be transcribed to text
            return:
                string: transcribed text from the input audio
        """

        audio = speech.RecognitionAudio(content=audio_bytes)
        recog_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=config.sampling_rate,
            language_code="en-US")

        response = self.speech_client.recognize(config=recog_config, audio=audio)
        transcription_list = []
        for result in response.results:
            transcription_list.append(result.alternatives[0].transcript)   
        transcription = " ".join(transcription_list)
         
        return transcription

    def speech_tot_ext_conversion(self):
        """
            route call single_channel function to convert double channel audio into single channel and then convert single channel audio  into string(sentence)   

            return: 
                spoken word in string form as a sentence
        """
        f = request.files['file']

        # convert stereo audio into mono audio for google speech to text api
        stereo_audio = AudioSegment.from_file(f, format="wav")
        mono_audios = stereo_audio.split_to_mono()
        audio_bytes = mono_audios[0].raw_data

        transcribed_text = self.speech_to_text(audio_bytes)
        if not transcribed_text:
            transcribed_text = ""   
        return transcribed_text

    def translate(self):
        """
            route pass requested sentence(englsih sentence from frontend) to the trained model for prediciton to translate english sentence  to french sentence

            Return:
                :string: french sentence
        """
        sentence = request.data
        sentence = sentence.decode()
        sentence = self.pred_object.final_predictions(self.model, sentence)
        return sentence
