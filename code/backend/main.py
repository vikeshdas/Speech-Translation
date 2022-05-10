# from Preprocessing import preprocessing
# import pickle
# import numpy as np
# from Model import ModelClass
# from TestAccurecy import accurecy
# from Prediction import predict_class
# from sklearn.model_selection import train_test_split

from SentencePrediction import MainClass


if __name__ == "__main__":
    md=MainClass()
    sentence = 'she dislikes that little red truck'
    res=md.predictsentence(sentence)
    print(res)

    # print("inside main")
    # # data set
    # english_sentences = '../data/small_vocab_en'
    # french_sentences = '../data/small_vocab_fr'
    
    # # preprocessing
    # print("doing prepocessing")
    # preproc = preprocessing()
    # english_sentences = preproc.load_data(english_sentences)
    # french_sentences = preproc.load_data(french_sentences)
    
    
    # preproc_english_sentences,\
    # preproc_french_sentences,\
    # english_tokenizer,\
    # french_tokenizer = preproc.preprocess(english_sentences, french_sentences)
    # print("type of preprocess_english",preproc_english_sentences)
    # print("type of french_tokenizer", type(french_tokenizer))
    
    # # saving tokenizers
    # with open('french_tokenizer.pickle', 'wb') as handle:
    #     pickle.dump(french_tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    # with open('english_tokenizer.pickle', 'wb') as handle:
    #     pickle.dump(english_tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    # # np.save('preproc_english_sentences', preproc_english_sentences)
    
    # print("doing spliting")
    # preproc_english_sentences_train, preproc_english_sentences_test, preproc_french_sentences_train, preproc_french_sentences_test = train_test_split(
    #     preproc_english_sentences, preproc_french_sentences, test_size=0.33,
    #     random_state=42)
    
    # # training
    # print("model training")
    # trn =ModelClass()
    # model = trn.create_model(preproc_english_sentences_train.shape,
    #                         preproc_french_sentences_train.shape[1],
    #                         len(english_tokenizer.word_index) + 1,
    #                         len(french_tokenizer.word_index) + 1)
    # trn.train_model(preproc_english_sentences_train,
    #                   preproc_french_sentences_train, model)
    
    # #save model
    # print("saving model")
    # model.save("model")
    # print("model saved")
    
    # # testaccurecy
    # # tacc = TestAccurecy.accurecy()
    # # tacc.test_accuracy(model, preproc_english_sentences_test,
    # #                    preproc_french_sentences_test)
    
    # # prediction
    # print("predicting")
    # pred = predict_class()
    # sentence = 'summer'
    # result = pred.final_predictions(model,sentence,french_tokenizer,english_tokenizer,preproc_english_sentences.shape[-1])
    
    # print(result)
