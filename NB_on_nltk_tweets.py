import nltk
import random
from nltk.corpus import twitter_samples
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB

import pickle
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re


class featurise_tweet_data():
    def __init__(self):
        self.punct_set = set(string.punctuation) 
        self.stopwords = set(stopwords.words('english'))
        self.pos_train = [(t, "pos") for t in twitter_samples.strings("positive_tweets.json")]
        self.neg_train = [(t, "neg") for t in twitter_samples.strings("negative_tweets.json")]
        self.lemmantizer = WordNetLemmatizer()
        self.adj_tag = ["J"]
        self.vocab_list = []
        self.train_list = []
        self.word_feats = []
        self.feature_set = []


    def process_pos_train(self):

        for p in self.pos_train:
            self.train_list.append(p)
            words = word_tokenize(p[0])
            pos = nltk.pos_tag(words)
            for w in pos:
                if w[1][0] in self.adj_tag:
                    if w[0] not in self.punct_set:
                        if w[0] not in self.stopwords:
                            new_word = self.lemmantizer.lemmatize(w[0])
                            self.vocab_list.append(new_word.lower())
        print("process pos train")
    def process_neg_train(self):

        for p in self.neg_train:
            self.train_list.append(p)
            words = word_tokenize(p[0])
            pos = nltk.pos_tag(words)
            for w in pos:
                if w[1][0] in self.adj_tag:
                    if w[0] not in self.punct_set:
                        if w[0] not in self.stopwords:
                            new_word = self.lemmantizer.lemmatize(w[0])
                            self.vocab_list.append(new_word.lower())
        print("process neg train")

    def get_word_features(self):
        all_words = nltk.FreqDist(self.vocab_list)

        word_features = list(all_words.keys())[:5500]
        for (tweets, category) in self.train_list:
            words = word_tokenize(tweets)
            features = {}
            for w in word_features:
                features[w] = (w in words)
            self.feature_set.append((features,category))
        random.shuffle(self.feature_set)
        print("process words train")
        return self.feature_set

    def pickle_feats(self):
        pickle_train_list = open("nltk_tr_tweets.pickle","wb")
        pickle.dump(self.train_list, pickle_train_list)
        pickle_train_list.close()

        save_word_features = open("word_feats_nltk_twt.pickle","wb")
        pickle.dump(self.word_feats, save_word_features)
        save_word_features.close()

        save_features_set = open("featsets_nltk.pickle","wb")
        pickle.dump(self.feature_set, save_features_set)
        save_features_set.close()

class NB_classifiers():
    def __init__(self,feat_sets):
        self.train_set = feat_sets[:9500]
        self.test_set = feat_sets[9500:]
        self.Multinomial_classifier = SklearnClassifier(MultinomialNB())
        self.bernoulli_classifier = SklearnClassifier(BernoulliNB())
        self.naivebayes_classifier = NaiveBayesClassifier.train(self.train_set)

    def multinomialNB(self):
        self.Multinomial_classifier.train(self.train_set)
        return "MultinomialNB accuracy percent:", nltk.classify.accuracy(self.Multinomial_classifier, self.test_set) * 100

    def BernoulliNB(self):
        self.bernoulli_classifier.train(self.train_set)
        return "BernoulliNB accuracy percent:", nltk.classify.accuracy(self.bernoulli_classifier, self.test_set)

    def NaiveBayes(self):
        return "normal nb Classifier accuracy percent:", (nltk.classify.accuracy(self.naivebayes_classifier, self.test_set)) * 100

    def pickle_classifiers(self):
        save_naivebayes = open("originalnaivebayes_nltk_twts.pickle","wb")
        pickle.dump(self.naivebayes_classifier, save_naivebayes)
        save_naivebayes.close()
        save_multinomial = open("MNB_classifier_nltk_twts.pickle", "wb")
        pickle.dump(self.Multinomial_classifier, save_multinomial)
        save_multinomial.close()
        save_bernoulli = open("BernoulliNB_classifier_nltk_twts.pickle", "wb")
        pickle.dump(self.bernoulli_classifier, save_bernoulli)
        save_bernoulli.close()



featuriser = featurise_tweet_data()
featuriser.process_neg_train()
featuriser.process_pos_train()
feature_wordset = featuriser.get_word_features()
featuriser.pickle_feats()
classifiers_obj = NB_classifiers(feature_wordset)
print(classifiers_obj.multinomialNB())
print(classifiers_obj.BernoulliNB())
print(classifiers_obj.NaiveBayes())
classifiers_obj.pickle_classifiers()







