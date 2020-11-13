from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re


class preprocessor:
    def __init__(self):
        #super().__init__()
        self.punct_set = set(string.punctuation)
        self.stopwords_set = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()#class object of nltk lemmantizer
        self.text = ""
        self.temp = []
        # self.tokensied = word_tokenise(self.txt)

    def remove_digits(self,text):
        remove_characters = [",", "\n", "#", "//", "_", "'"]

        self.text = re.sub(r"\d +", "", text)#regex expression to replace digits with empty string
        self.text = re.sub(r"http\S+", "", self.text)#regex expression to remove urls at end of tweets
        self.text = self.text.lower()#normalise the text by putting it in lower case
        for c in remove_characters:
            self.text.replace(c, " ")#removes other chars like hash tags and underscores
        #print(self.text)

    def remove_emojis(self):
        RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)#compile all emojis
        self.tokenise = word_tokenize(self.text)#tokenise the text into list of words
        for word in self.tokenise:
            word = RE_EMOJI.sub(r'', word)#if a word is in the emoji set then replace blank space
            self.temp.append(word)#add word to temporary list
            self.temp.append(" ")
        self.text = "".join(self.temp)#joins the words to empty string to get the sentence

    def remove_punctuation(self,text):
        self.tokenise = word_tokenize(self.text)
        self.temp = []
        #print(self.text)
        for word in self.tokenise:
            #print(word)
            if word not in self.punct_set:
                self.temp.append(word)
                self.temp.append(" ")

        self.text = "".join(self.temp)

        #print("punctuation removed")

    def remove_stopwords(self,text):
        self.tokenise = word_tokenize(self.text)
        self.temp = []
        for word in self.tokenise:
            if word not in self.stopwords_set:
                self.temp.append(word)
                self.temp.append(" ")

        self.text = "".join(self.temp)


       # print("stopwords removed")

    def lemmantize_tweets(self,text):
        self.tokenise = word_tokenize(self.text)
        self.temp = []
        for word in self.tokenise:
            word = self.lemmatizer.lemmatize(word)#lemmantise the word
            self.temp.append(word)
            self.temp.append(" ")
        self.text = "".join(self.temp)
        #print(self.text)
        return self.text



def get_text(text):
    processed_obj = preprocessor()#create class object of preprocessor
    processed_obj.remove_digits(text)#call remove digits
    processed_obj.remove_punctuation(text)#call remove punctuation
    processed_obj.remove_stopwords(text)#call remove stopwords
    return processed_obj.lemmantize_tweets(text)#call lemmantise


