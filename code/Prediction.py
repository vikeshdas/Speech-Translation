import Preprocessing
from tensorflow.keras.preprocessing.sequence import pad_sequences


class predict:

    def final_predictions(self,model, sentence, french_tokenizer, english_tokenizer,preproc_english_sentences):
        """
           Turn logits from a neural network into text using the tokenizer
           :param sentence: sequence of string or single sentence
           :param french_tokenizer: tokenize form of french dataa set
           :param english_tokenizer:tokenize form of english data set
           :param preproc_english_sentences
           :return: predicted english sentece
        """
        sentence = [english_tokenizer.word_index[word] for word in sentence.split()]
        sentence = pad_sequences([sentence],maxlen=preproc_english_sentences.shape[-1],padding='post')
        sentence = model.predict(sentence, len(sentence))
        # reshaping because after prediction size is (1,21,345)
        sentence = sentence.reshape(21, 345)

        #object of preprocessing class
        prep=Preprocessing.preprocessing()

        res = prep.logits_to_text(sentence, french_tokenizer)
        return res