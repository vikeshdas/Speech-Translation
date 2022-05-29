""" 
    model translate a english sentence to french sentence
    from trained model
"""

from distutils.command.config import config
import numpy as np
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

import config

class Prediction:
    """
        load the saved English tokenizer, french tokenizer and max length of sentence in the data set from the disk using pickle library, to predict English sentence to french sentence from the trained model
    """
    def __init__(self):
        with open('../../data/french_tokenizer.pickle', 'rb') as handle:
            self.french_tokenizer = pickle.load(handle)

        with open('../../data/english_tokenizer.pickle', 'rb') as handle:
            self.english_tokenizer = pickle.load(handle)

        self.max_len = np.load("../../data/max_len_arr.npy").tolist()[0]

    def final_predictions(self, model, sentence):
        """
        take predictions by hitting the model

        :Args:
              sentence: 
                   sequence of string or single sentence
              model:
                  Trained nueral network model for english to french translation    
              
              Return: predicted french sentece
        """

        sentence_token = []

        for word in sentence.split(" "):
            if not self.english_tokenizer.word_index.get(word):
                return "some words that you spoke are not in my vocabulary"
            else:
                sentence_token.append(
                    self.english_tokenizer.word_index.get(word))

        sentence_token = pad_sequences([sentence_token],
                                       maxlen=self.max_len, padding='post')
        sentence_token = model.predict(sentence_token, len(sentence_token))
        sentence_token = sentence_token.reshape(config.Shape)

        res = self.logits_to_text(sentence_token, self.french_tokenizer)

        return res

    def logits_to_text(self, logits, tokenizer):
        """
        transforms predicted logits from a neural network into text using the tokenizer

        Args:
            logits:
                predicted logits from the model
            tokenizer:
                Keras Tokenizer fits on the labels
        
        Returns:
            string that represents the predicted text from the logits
        """

        index_to_words = {}
        for word, _id in tokenizer.word_index.items():
            index_to_words[_id] = word
        index_to_words[0] = '<PAD>'

        res = ""
        for prediction in np.argmax(logits, 1):
            if prediction:
                res = res + " " + index_to_words[prediction]

        return res
