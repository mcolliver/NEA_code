import csv
import tweepy
from tweepy import OAuthHandler
import sentiment_mod as s
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re

"""csvFile = open('train_tweets.csv', 'a', encoding="utf-8", newline="")
                csvWriter = csv.writer(csvFile)
                self.tweet_text = re.sub(r"http\S+", "", tweet.full_text)
                self.tweet_text = re.sub(r"\W+|_", " ", self.tweet_text)
                sentiment_pol = s.sentiment(self.tweet_text)
                csvWriter.writerow([tweet.created_at, self.tweet_text,sentiment_pol])
                csvFile.close()"""


# keys recieved when creating a developer account on twitter
consumer_key = "2f4kN1axhPOUY2TdN33ugh65P"
consumer_secret = "mkHFVL6XRHUOmhFjgoxdjzu7a1t3foRQq7doAJOOyCr3MgkI7j"
access_token = "1274365795867463681-02F6f7KEyQ2V2P1jpq6qc2kPLRT6tF"
access_token_secret = "3gp0wxDQZ1isDhvte9sUK2mD0lmfJF7ZuEWMXrmv8DGre"

class cursor_tweets():
    def __init__(self,api):
        super(cursor_tweets, self).__init__()
        self.api = api
        self.tweet_text = []
    def tweet_cursor(self):
        try:
            for tweet in tweepy.Cursor(self.api.search,q="microsoft OR #msft OR msft OR azure OR microsoft office OR microsoft word OR #Microsoft -filter:retweets ",lang="en",since="2019-11-03",tweet_mode='extended').items(500):
                csvFile = open('train_tweets.csv', 'a', encoding="utf-8", newline="")
                csvWriter = csv.writer(csvFile)
                self.tweet_text = re.sub(r"http\S+", "", tweet.full_text)
                self.tweet_text = re.sub(r"\W+|_", " ", self.tweet_text)
                sentiment_pol = s.sentiment(self.tweet_text)
                csvWriter.writerow([tweet.created_at, self.tweet_text, sentiment_pol])
                csvFile.close()
        except tweepy.TweepError as e:
            print(f"error is {e}")





if __name__ == "__main__":
    keywords_msft = "microsoft OR #msft OR msft OR azure OR microsoft office OR microsoft word OR #microsoft OR #Microsoft"


    auth = OAuthHandler(consumer_key, consumer_secret)
    # create OAuthHandler object, so keys can be exchanged to authenticate a connection

    auth.set_access_token(access_token, access_token_secret)
    # sets the access token by passing the access token and secret as parameters for the function

    twitter_api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)



    '''csvFile = open('train_tweets.csv', 'a', encoding="utf-8", newline="")
    csvWriter = csv.writer(csvFile)
    headers = ["date", "tweet_text","Sentiment"]
    csvWriter.writerow(headers)
    csvFile.close()'''

    tweetwriter = cursor_tweets(twitter_api)
    tweetwriter.tweet_cursor()


