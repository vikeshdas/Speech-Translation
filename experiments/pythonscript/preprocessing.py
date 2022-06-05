"""
    load data set from disk and preprocess it perform tokenization,pading

"""

import os
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


class Preprocessing:
 
    def load_data(self, path):
        """
            load data set from disk
            :param path is path of data set
            return clear data set in list of sentences
        """
        
        input_file = os.path.join(path)
        with open(input_file, "r") as f:
            data = f.read()
        return data.split('\n')

    def tokenize(self, x):
        """
            tokenize list of senteces
            :param x: Feature List of sentences
            :return: numpy array
        """
        # TODO: Implement
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(x)
        # it return object->tokenizer and tokenize form of data(sentesces)

        return tokenizer.texts_to_sequences(x), tokenizer

    def pad(self, x, length=None):
        """
            Pad x
            :param x: List of sequences.
            :param length: Length to pad the sequence to.  If None, use length of longest sequence in x.
            :return: Padded numpy array of sequences
        """
        # TODO: Implement
        return pad_sequences(x, maxlen=length, padding='post')

    def logits_to_text(self, logits, tokenizer):
        """
            Turn logits from a neural network into text using the tokenizer
            :param logits: Logits from a neural network
            :param tokenizer: Keras Tokenizer fit on the labels
            :return: String that represents the text of the logits
        """

        index_to_words = {}
        for word, _id in tokenizer.word_index.items():
            index_to_words[_id] = word
        index_to_words[0] = '<PAD>'

        res = ""
        for prediction in np.argmax(logits, 1):
            if prediction:
                res = res + " " + index_to_words[prediction]

        return res;

    def preprocess(self,x, y, en_max_len=None, fr_max_len=None):
        """
            Preprocess english  and french data set
            :param x: Feature List of english sentences
            :param y: Label List of French sentences
            :return: Tuple of (Preprocessed x, Preprocessed y, x tokenizer, y tokenizer)
        """
        preprocess_x, x_tk = self.tokenize(x)
        preprocess_y, y_tk = self.tokenize(y)
        
        preprocess_x = self.pad(preprocess_x, en_max_len)
        preprocess_y = self.pad(preprocess_y, fr_max_len)

        preprocess_y = preprocess_y.reshape(*preprocess_y.shape, 1)

        return preprocess_x, preprocess_y, x_tk, y_tk



