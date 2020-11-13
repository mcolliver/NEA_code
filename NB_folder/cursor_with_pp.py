from NB_folder import sentiment_analyser as s, preprocessor as pp
import csv
import tweepy
from tweepy import OAuthHandler
import datetime
# keys recieved when creating a developer account on twitter
consumer_key = "2f4kN1axhPOUY2TdN33ugh65P"
consumer_secret = "mkHFVL6XRHUOmhFjgoxdjzu7a1t3foRQq7doAJOOyCr3MgkI7j"
access_token = "1274365795867463681-02F6f7KEyQ2V2P1jpq6qc2kPLRT6tF"
access_token_secret = "3gp0wxDQZ1isDhvte9sUK2mD0lmfJF7ZuEWMXrmv8DGre"


class get_tweets():
    def __init__(self):
        # initialise class variables
        self.tweet_text = ""
        self.tweet_date = ""
        self.list = []#list to keep tweets to later be stored in csv
        self.date_list = []#list to keep datea of tweets to later be stored in csv
        self.time_list = []
        self.cleaned_text = ""

    def tweet_cursor(self, api):
        try:
            for tweet in tweepy.Cursor(api.search,
                                       q="microsoft OR #msft OR msft OR azure OR microsoft office OR microsoft word OR #Microsoft -filter:retweets ",
                                       lang="en", since="2019-11-03", tweet_mode='extended').items(250):
                self.tweet_text = tweet.full_text
                self.tweet_date = datetime.datetime.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S')
                date_of_tweet = self.tweet_date.date()
                time_of_tweet = self.tweet_date.time()
                #date_time_obj = datetime.datetime.strptime(tweet.created_at, '%Y-%m-%d %H:%M')
                self.cleaned_text = pp.get_text(self.tweet_text)#pass tweet text to get_text and preprocess the text
                self.list.append(self.cleaned_text)#add cleaned text to list
                self.date_list.append(date_of_tweet)#add date to list
                self.time_list.append(time_of_tweet)
            #print(self.list)

        except tweepy.TweepError as e:
            #error handling, so tweepy error are flagged up
            print(f"error is {e}")

    def write_to_csv(self):
        for i in range(len(self.list)):
            msft_csv = open('train_tweets9.csv', 'a', encoding="utf-8", newline="")
            #opens a file to write tweets and replaces newlines with empty string
            csvWriter = csv.writer(msft_csv)#creates writer object to srite data to csv
            sentiment_pol = s.sentiment(self.list[i])#gets sentiment of tweets
            csvWriter.writerow([self.date_list[i],self.time_list[i] ,self.list[i], sentiment_pol])#writes row of data to csv
            msft_csv.close()

    '''def graph_sentiment(self):
        tweet_df = pd.read_csv('train_tweets9.csv',header=0)
        #tweet_df['date'] = pd.to_datetime(tweet_df['date'])
        #tweet_df.set_index('date', inplace=True)
        tweet_df['polarity'] = tweet_df['Sentiment'].apply(lambda x: 1 if x == "pos" else -1)
        tweet_df.info()''' #still in progress



if __name__ == "__main__":
    auth = OAuthHandler(consumer_key, consumer_secret)
    # create OAuthHandler object, so keys can be exchanged to authenticate a connection

    auth.set_access_token(access_token, access_token_secret)
    # sets the access token by passing the access token and secret as parameters for the function

    twitter_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    #creates api object to connect cursor to the API

    csvFile = open('train_tweets9.csv', 'a', encoding="utf-8", newline="")
    csvWriter = csv.writer(csvFile)
    headers = ["date","time" ,"tweet_text","Sentiment"]
    csvWriter.writerow(headers)
    csvFile.close()

    cursor_obj = get_tweets() #creates class object
    cursor_obj.tweet_cursor(twitter_api)#calls tweet_curosr method with twitter api as a parameter
    cursor_obj.write_to_csv()#calls write_to_csv method to write tweets to csv file
    #cursor_obj.graph_sentiment()

