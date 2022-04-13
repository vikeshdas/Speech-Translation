import Preprocessing
import Model
import TestAccurecy
import Prediction
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    # data set
    english_sentences = 'data/small_vocab_en'
    french_sentences = 'data/small_vocab_fr'

    # preprocessing
    preproc = Preprocessing.preprocessing()
    english_sentences = preproc.load_data(english_sentences)
    french_sentences = preproc.load_data(french_sentences)

    preproc_english_sentences,\
    preproc_french_sentences,\
    english_tokenizer,\
    french_tokenizer = preproc.preprocess(english_sentences, french_sentences)

    preproc_english_sentences_train, preproc_english_sentences_test, preproc_french_sentences_train, preproc_french_sentences_test = train_test_split(
        preproc_english_sentences, preproc_french_sentences, test_size=0.33,
        random_state=42)

    # training
    trn = Model.model()
    model = trn.train_model(preproc_english_sentences_train.shape,
                            preproc_french_sentences_train.shape[1],
                            len(english_tokenizer.word_index) + 1,
                            len(french_tokenizer.word_index) + 1)
    trn.Compile_model(preproc_english_sentences_train,
                      preproc_french_sentences_train, model)

    # testaccurecy
    tacc = TestAccurecy.accurecy()
    tacc.test_accuracy(model, preproc_english_sentences_test,
                       preproc_french_sentences_test)

    # prediction
    pred = Prediction.predict()
    sentence = 'he saw a old yellow truck'
    result = pred.final_predictions(model, sentence, french_tokenizer,
                                    english_tokenizer,
                                    preproc_english_sentences)
    print(result)
