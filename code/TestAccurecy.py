class accurecy:
    def test_accuracy(self,model, preproc_english_sentences_test,preproc_french_sentences_test):
        """
            Pad x
            :param model: trained model.
            :param preproc_english_sentences_test: english test data set
            :param preproc_french_sentences_test: french test data set
            :return: accurecy on test data set
        """
        result = model.evaluate(preproc_english_sentences_test,preproc_french_sentences_test, batch_size=1024)
        return result