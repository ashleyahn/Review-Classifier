import math

class Bayes_Classifier:

    def __init__(self):
        self.my_dict = {}
        self.positiveReviewsCount = 0
        self.negativeReviewsCount = 0
        self.positiveWordsCount = 0
        self.negativeWordsCount = 0
        # stop words are "neutral" words such as articles and prepositions
        self.stopList = ['the', 'a', 'it', 'a', 'an', 'of', 'from', 'and']

    # trains the classifier by counting how many times a word is in a positive or negative review
    def train(self, lines):
        for line in lines:
            # saves data of a line thats split into 3 (number of stars, ID #, review text) into a list fields
            line = line.replace('\n','')
            fields = line.split('|')
            # counts the number of positive and negative reviews
            numStars = int(fields[0])
            self.incrementReviewCount(numStars)
            text = fields[2].lower() # the review text in all lowercase
            # counts the number of times a word shows up in a positive and/or negative review and saves to a dict
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

    # helper function that increments the positive and negative review count
    def incrementReviewCount(self, numStars):
        if numStars == 5:
            self.positiveReviewsCount += 1
        else: 
            self.negativeReviewsCount += 1

    # returns a list of classifications for each review in respective indices
    def classify(self, lines):
        classifications = []
        for line in lines:
            line = line.replace('\n','')
            fields = line.split('|')
            text = fields[2].lower().split()
            # tests if review's probability of being pos vs neg and appends higher probablity to list classifications
            if self.probabilityPos(text) > self.probabilityNeg(text):
                classifications.append('5')
            else:
                classifications.append('1')
        return classifications
            
    # calculates probabililty that a review is positive given the "features" or words in the review
    def probabilityPos(self, features):
        probPos = (self.positiveReviewsCount / (self.positiveReviewsCount + self.negativeReviewsCount))
        # log probabiltiies used to prevent underflow of very small numbers
        prob = math.log10(probPos)
        for f in features:
            if f not in self.stopList:
                if f in self.my_dict:
                    fprob = (self.my_dict[f][0] + 1) / (self.positiveWordsCount + len(self.my_dict))
                else:
                    # if word is not observed in training set - smoothing technique
                    fprob = 1 / (self.positiveWordsCount + len(self.my_dict))
                # products become sums with logs
                prob += math.log10(fprob)
        return prob
    
    # calculates probabililty that a review is negative given the "features" or words in the review
    def probabilityNeg(self, features):
        probNeg = self.negativeReviewsCount / (self.positiveReviewsCount + self.negativeReviewsCount)
        prob = math.log10(probNeg)
        for f in features:
            if f not in self.stopList:
                if f in self.my_dict:
                    fprob = (self.my_dict[f][1] + 1) / (self.negativeWordsCount + len(self.my_dict))
                else:
                    # if word is not observed in training set - smoothing technique
                    fprob = 1 / (self.negativeWordsCount + len(self.my_dict))
                prob += math.log10(fprob)
        return prob

    # deletes punctuation from dataset - not implemented
    def punctuation(self, string): 
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for x in string.lower(): 
            if x in punctuations: 
                string = string.replace(x, "") 
        return string
