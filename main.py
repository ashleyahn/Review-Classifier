import math
import bayes_classifier as nbc
import unittest
import numpy

# calculates an f-score that takes into account the precision and recall of the classifier for a given class
def f_score(data,predict):

    actual = []

    for line in data:
        line = line.replace('\n','')
        fields = line.split('|')
        wID = int(fields[1])
        sentiment = fields[0]
        actual.append(sentiment)

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    for i in range(len(actual)):
        if predict[i] == '5' and actual[i] == '5':
            tp = tp + 1
        if predict[i] == '5' and actual[i] == '1':
            fp = fp + 1
        if predict[i] == '1' and actual[i] == '1':
            tn = tn + 1
        if predict[i] == '1' and actual[i] == '5':
            fn = fn + 1

    precision = float(tp)/float(tp+fp)
    recall = float(tp)/float(tp+fn)
    f_score_p = float(2.0)*precision*recall/(precision+recall)

    precision = float(tn)/float(tn+fn)
    recall = float(tn)/(fp+tn)
    f_score_n = float(2.0)*precision*recall/(precision+recall)    

    return(f_score_p, f_score_n)

data = []

# saves data in text file into global var data
def load_data():
    global data
    f = open('alldata.txt', "r")
    data = f.readlines()
    f.close()

class NaiveBayesTest(unittest.TestCase):
    # f-score for classifying positive reviews should be greater than 0.9
    # f-score for classifying negative reviews should be greater than 0.6


    # trains using first 90% of data and classifies/checks for accuracy using last 10% of data
    def test1(self):
        classifier = nbc.Bayes_Classifier()
        classifier.train(data[:12478])
        predictions = classifier.classify(data[12478:])
        fp, fn = f_score(data[12478:],predictions)
        print(fp,fn)
        self.assertGreater(fp,0.90)
        self.assertGreater(fn,0.60)

    # makes all reviews 5 stars
    # tests that we aren't using the rating fields for classifying accidentally
    def test2(self):
        classifier = nbc.Bayes_Classifier()
        classifier.train(data[:12478])
        datacopy = ["5"+d[1:] for d in data]
        predictions = classifier.classify(datacopy[12478:])
        fp, fn = f_score(data[12478:],predictions)
        print(fp,fn)
    
    # tests with random sets of the data
    def test_random(self):
        trials = 20
        for _ in range(trials):
            numpy.random.shuffle(data)
            training, test = data[:12478], data[12478:]
            classifier = nbc.Bayes_Classifier()
            classifier.train(training)
            predictions = classifier.classify(test)
            fp, fn = f_score(test,predictions)
            print(fp,fn)
            self.assertGreater(fp,0.90)
            self.assertGreater(fn,0.60)

if __name__ == "__main__":
    load_data()
    unittest.main()


