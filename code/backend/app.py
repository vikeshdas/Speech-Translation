"""
    backend api for audio translation
    has routes for speech to text conversion, text to text translation
"""


from flask import Flask
from flask_cors import CORS

from load import Load


app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/text-speech", methods=['POST'])
def text_speech():
    return obj.text_to_speech_conversion()


@app.route("/speech-text", methods=['POST', 'GET'])
def speech_to_text():
    return obj.speech_tot_ext_conversion()


@app.route("/translate", methods=['POST', 'GET'])
def englsi_to_french_translate():
    return obj.translate()

if __name__ == '__main__':
    obj = Load()
    app.run(debug=True, port=8000)

