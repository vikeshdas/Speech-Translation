from unittest.util import _MAX_LENGTH
import tensorflow as tf
import numpy as np
from Prediction import predict_class
import pickle

class MainClass:

    def __init__(self):
    # data set
        with open('french_tokenizer.pickle', 'rb') as handle:
            self.french_tokenizer = pickle.load(handle)

        with open('english_tokenizer.pickle', 'rb') as handle:
            self.english_tokenizer = pickle.load(handle)

        self.max_len= np.load("max_len_arr.npy")
        self.max_len.tolist()
        self.max_len=self.max_len.item()




    # prediction
    def predictsentence(self, sentence):
        print("type os sentence is",type(sentence))
        model = tf.keras.models.load_model("model")
        pred = predict_class()
        result = pred.final_predictions(model,sentence.lower(), self.french_tokenizer, self.english_tokenizer,self.max_len)
        return result
