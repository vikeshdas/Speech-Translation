"""
    translate single sentence from english to french
"""
import tensorflow as tf
import numpy as np
from prediction import Prediction
import pickle


class SentencePrediction:
    """
        load saved french tokenizer from disk and 
        load saved english tokenizer form disk
        load saved max length of sentence

        Attributes:
            french_tokenizer:store french tokenizer
            english_tokenizer:store english tokenzier
            max_len:lenth of sentece with max length from whole data set
    """
    
    def __init__(self):
        # data set
        with open('../../data/french_tokenizer.pickle', 'rb') as handle:
            self.french_tokenizer = pickle.load(handle)
    
        with open('../../data/english_tokenizer.pickle', 'rb') as handle:
            self.english_tokenizer = pickle.load(handle)

        self.max_len = np.load("../../data/max_len_arr.npy").tolist()[0]

    def predict_sentence(self, sentence):
    
        """
            tranlate enslish sentence to french
            :param sentence: englsih single sentence or list of word 
            :return: french sentence
        """
        # print("type os sentence is",type(sentence))
        model = tf.keras.models.load_model("../../trained_model")
        pred = Prediction()
        result = pred.final_predictions(
                model, sentence.lower(), 
                self.french_tokenizer, 
                self.english_tokenizer, self.max_len)
        return result
