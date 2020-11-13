import random
import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):# * means there are multiple arguements
        self._classifiers = classifiers #list of classifiers

    def classify(self, features):
        votes = []#stores the sentiment given by the classifiers
        for c in self._classifiers:
            v = c.classify(features)#classify the tweet
            votes.append(v)#add the sentiment to the list

        return mode(votes)#return the most common element


train_tweets = open("nltk_tr_tweets.pickle", "rb")
tweet_file = pickle.load(train_tweets)
train_tweets.close()




word_feature_tweets = open("word_feats_nltk_twt.pickle", "rb")
word_features = pickle.load(word_feature_tweets)
word_feature_tweets.close()


def find_features(msft_tweet): #takes in tweet from cursor after its been preprocessed
    words = word_tokenize(msft_tweet)#tokenises the tweet into list of individual words
    features = {}
    for w in word_features:
        features[w] = (w in words)
        #if word is in word_features then store in dictionary with a 1, else store the word with a 0

    return features



featuresets_tweets = open("featsets_nltk.pickle", "rb")
featuresets = pickle.load(featuresets_tweets)
featuresets_tweets.close()

random.shuffle(featuresets)
#print(len(featuresets))

testing_set = featuresets[9500:]
training_set = featuresets[:9500]



NB_file = open("originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(NB_file)
NB_file.close()


MNB_file = open("MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(MNB_file)
MNB_file.close()



BNB_file = open("BernoulliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(BNB_file)
BNB_file.close()

voted_classifier = VoteClassifier(classifier,MNB_classifier,BernoulliNB_classifier)

def get_sentiment(text):
    feats = find_features(text)#get features from the tweets
    return voted_classifier.classify(feats)#classify the tweet