import math
import re

class Bayes_Classifier:

    def __init__(self):
        self.my_dict = {}
        self.positiveReviewsCount = 0
        self.negativeReviewsCount = 0
        self.positiveWordsCount = 0
        self.negativeWordsCount = 0
        self.stopList = ['the', 'a', 'it', 'a', 'an', 'of', 'from', 'and']


    def train(self, lines):
        for line in lines:
            line = line.replace('\n','')
            fields = line.split('|')
            numStars = int(fields[0])
            if numStars == 5:
                self.positiveReviewsCount += 1
            else: 
                self.negativeReviewsCount += 1
            reviewID = int(fields[1])
            text = fields[2].lower()
            #text = self.punctuation(text)
            for word in text.split():
                if word not in self.stopList:
                    if word not in self.my_dict:
                        if numStars == 5:
                            self.positiveWordsCount += 1
                            self.my_dict[word] = [1, 0]
                        else:
                            self.negativeWordsCount += 1
                            self.my_dict[word] = [0, 1]
                    else:
                        if numStars == 5:
                            self.positiveWordsCount += 1
                            self.my_dict[word][0] += 1
                        else:
                            self.negativeWordsCount += 1
                            self.my_dict[word][1] += 1


    def classify(self, lines):
        classifications = []
        for line in lines:
            line = line.replace('\n','')
            fields = line.split('|')
            text = fields[2].lower().split()
            if self.probabilityPos(text) > self.probabilityNeg(text):
                classifications.append('5')
            else:
                classifications.append('1')
        return classifications
            

    def probabilityPos(self, features):
        probPos = (self.positiveReviewsCount / (self.positiveReviewsCount + self.negativeReviewsCount))
        prob = math.log10(probPos)
        for f in features:
            if f not in self.stopList:
                if f in self.my_dict:
                    fprob = (self.my_dict[f][0] + 1) / (self.positiveWordsCount + len(self.my_dict))
                else:
                    fprob = 1 / (self.positiveWordsCount + len(self.my_dict))
                prob += math.log10(fprob)
        return prob
    
    def probabilityNeg(self, features):
        probNeg = self.negativeReviewsCount / (self.positiveReviewsCount + self.negativeReviewsCount)
        prob = math.log10(probNeg)
        for f in features:
            if f not in self.stopList:
                if f in self.my_dict:
                    fprob = (self.my_dict[f][1] + 1) / (self.negativeWordsCount + len(self.my_dict))
                else:
                    fprob = 1 / (self.negativeWordsCount + len(self.my_dict))
                prob += math.log10(fprob)
        return prob

    def punctuation(self, string): 
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for x in string.lower(): 
            if x in punctuations: 
                string = string.replace(x, "") 
        return string