"""
    backend api for audio translation
    has routes for speech to text conversion, text to text translation
"""

import os

from flask import Flask
from flask_cors import CORS
import config

from load import Load


app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.credential_path

@app.route("/text-speech", methods=['POST'])
def text_speech():
    obj=Load()
    return obj.text_to_speech_conversion()


@app.route("/speech-text", methods=['POST', 'GET'])
def speech_to_text():
    obj=Load()
    return obj.speech_tot_ext_conversion()


@app.route("/translate", methods=['POST', 'GET'])
def englsi_to_french_translate():
    obj=Load()
    return obj.translate()

if __name__ == '__main__':
    # obj = Load()
    app.run(debug=True)

