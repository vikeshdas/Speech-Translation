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
    sentence = 'that cat was my most loved animal'
    res=md.predictsentence(sentence)
    print(res)

    # print("inside main")
    # # data set
    # english_sentences = '/home/jai/Documents/projects/translator/data/small_vocab_en'
    # french_sentences = '/home/jai/Documents/projects/translator/data/small_vocab_fr'
    
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
    
    # np.save('preproc_english_sentences', preproc_english_sentences)
    
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
    # model.save("model")
    
    # # testaccurecy
    # # tacc = TestAccurecy.accurecy()
    # # tacc.test_accuracy(model, preproc_english_sentences_test,
    # #                    preproc_french_sentences_test)
    
    # # prediction
    # pred = predict_class()
    # sentence = 'good morning'
    # result = pred.final_predictions(model,sentence,french_tokenizer,english_tokenizer,preproc_english_sentences)
    
    # print(result)