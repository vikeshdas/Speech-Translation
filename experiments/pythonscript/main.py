from model import Model
from preprocessing import Preprocessing
from prediction import Prediction
from sklearn.model_selection import train_test_split
# from sentence_prediction import SentencePrediction

if __name__ == "__main__":
    # sentece='yellow'
    # print(sentece)
    # md=SentencePrediction().predict_sentence(sentece)
    # print(md)
    print("inside main")
    english_sentences = '../../data/small_vocab_en'
    french_sentences = '../../data/small_vocab_fr'
    # preprocessing
    print("doing prepocessing")
    preproc = Preprocessing()
    english_sentences = preproc.load_data(english_sentences)
    french_sentences = preproc.load_data(french_sentences)
    
    
    preproc_english_sentences,preproc_french_sentences,english_tokenizer,\
    french_tokenizer = preproc.preprocess(english_sentences, french_sentences)

    

    print("doing spliting")
    preproc_english_sentences_train, preproc_english_sentences_test, preproc_french_sentences_train, preproc_french_sentences_test = train_test_split(preproc_english_sentences, 
                     preproc_french_sentences, est_size=0.33,random_state=42)
    
    # training
    print("model training")
    trn =Model()
    model = trn.create_model(preproc_english_sentences_train.shape,
                            preproc_french_sentences_train.shape[1],
                            len(english_tokenizer.word_index) + 1,
                            len(french_tokenizer.word_index) + 1)

    trn.train_model(preproc_english_sentences_train,
                    preproc_french_sentences_train, model)
    

    
    # prediction
    print("predicting")
    pred = Prediction()
    sentence = 'summer'
    result = pred.final_predictions(model,sentence,
                                    french_tokenizer,
                                    english_tokenizer, preproc_english_sentences.shape[-1])
    
    print(result)
