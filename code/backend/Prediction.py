from Preprocessing import preprocessing
from tensorflow.keras.preprocessing.sequence import pad_sequences


class predict_class:

    def final_predictions(self, model, sentence, french_tokenizer, english_tokenizer, max_len):
        """
           Turn logits from a neural network into text using the tokenizer
           :param sentence: sequence of string or single sentence
           :param french_tokenizer: tokenize form of french dataa set
           :param english_tokenizer:tokenize form of english data set
           :param preproc_english_sentences
           :return: predicted english sentece
        """


        sentence_token=[]
        
        for word in sentence.split(" "):
            if not english_tokenizer.word_index.get(word):
                return "some words that you spoke are not in my vocabulary"
            else:
                sentence_token.append(english_tokenizer.word_index.get(word))    
        print(sentence_token);
        sentence_token=pad_sequences([sentence_token],maxlen=max_len,padding='post')        
        sentence_token = model.predict(sentence_token, len(sentence_token))
        # reshaping because after prediction size is (1,21,345)
        sentence_token = sentence_token.reshape(21, 345)

        #object of preprocessing class
        prep=preprocessing()

        res = prep.logits_to_text(sentence_token, french_tokenizer)

        return res