"""
    calculate accuracy of the model on the test set
"""

class accuracy:

    def test_accuracy(self,model, preproc_english_sentences_test,preproc_french_sentences_test):
        """
            :param model: trained model.
            :param preproc_english_sentences_test: english test data set
            :param preproc_french_sentences_test: french test data set
            :return: accurecy on test data set
        """
        result = model.evaluate(preproc_english_sentences_test,preproc_french_sentences_test, batch_size=1024)
        return result