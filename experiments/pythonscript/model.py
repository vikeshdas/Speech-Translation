"""
    Train model with dataset
    compile model
    save model on disk
"""
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, TimeDistributed, RepeatVector, Bidirectional, Dropout
from tensorflow.keras.losses import sparse_categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Embedding



class Model:

    def create_model(self, input_shape, output_sequence_length,
                     english_vocab_size,french_vocab_size):
        """
            input_shpae=dimention of english data

            Build and train a model that incorporates embedding, encoder-decoder, and bidirectional RNN on x and y
            :param input_shape: Tuple of input shape
            :param output_sequence_length: Length of output sequence
            :param english_vocab_size: Number of unique English words in the dataset
            :param french_vocab_size: Number of unique French words in the dataset
            :return: Keras model built, but not trained
        """
        # TODO: Implement

        # Hyperparameters
        learning_rate = 0.003
        # Build the layers
        model = Sequential()
        # Embedding
        model.add(Embedding(english_vocab_size, 128, 
                           input_length=input_shape[1],
                           input_shape=input_shape[1:]))
        # Encoder
        model.add(Bidirectional(GRU(128)))
        model.add(RepeatVector(output_sequence_length))
        # Decoder
        model.add(Bidirectional(GRU(128, return_sequences=True)))
        model.add(TimeDistributed(Dense(512, activation='relu')))
        model.add(Dropout(0.5))
        model.add(TimeDistributed(Dense(french_vocab_size, 
                                        activation='softmax')))
        model.compile(loss=sparse_categorical_crossentropy,
                      optimizer=Adam(learning_rate), metrics=['accuracy'])
        return model


    def train_model(self, preproc_english_sentences_train,
                   preproc_french_sentences_train, model):
        """ 
            train model
            :param preproc_english_sentences_train:english train data set in tokenize form
            param: preproc_french_sentences_train: french train data set in tokenize form
           """
        model.summary()
        model.fit(preproc_english_sentences_train, preproc_french_sentences_train, batch_size=1024, epochs=1,validation_split=0.2)


    def save_model(self,model, path):
        """
            save model on disk
            :param model trained model:
            :param path: path where to save the model
            :return:
        """
        print("inside save_model")
        model.save(path)


    def load_model(self,path):
        """
            load model from disk
            :param path: path where model is saved
            :return: saved model
        """
        model = tf.keras.models.load_model(path)
        return model