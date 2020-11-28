from yahoo_fin import stock_info
from textblob import TextBlob
import csv
from datetime import timedelta
import tweepy
from tweepy import OAuthHandler
import datetime
import re
import pandas as pd

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
                                       q="$MSFT -filter:retweets",
                                       lang="en", since="2019-11-03", tweet_mode='extended').items(100):
                self.tweet_text = re.sub(r"http\S+", "", tweet.full_text)
                self.tweet_date = datetime.datetime.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S')
                date_of_tweet = self.tweet_date.date()
                time_of_tweet = self.tweet_date.time()
                #date_time_obj = datetime.datetime.strptime(tweet.created_at, '%Y-%m-%d %H:%M')
                self.cleaned_text = re.sub(r"[^a-zA-Z0-9]+", ' ', self.tweet_text)#pass tweet text to get_text and preprocess the text
                self.list.append(self.cleaned_text.lower())#add cleaned text to list
                self.date_list.append(date_of_tweet)#add date to list
                self.time_list.append(time_of_tweet)
            #print(self.list)

        except tweepy.TweepError as e:
            #error handling, so tweepy error are flagged up
            print(f"error is {e}")

    def write_to_csv(self):
        total_sent = 0
        #avg_sent = []
        for i in range(len(self.list)):
            msft_csv = open('msft5.csv', 'a', encoding="utf-8", newline="")
            #opens a file to write tweets and replaces newlines with empty string
            csvWriter = csv.writer(msft_csv)#creates writer object to srite data to csv
            textblob_sent = TextBlob(self.list[i])


            csvWriter.writerow([self.date_list[i],self.time_list[i] ,self.list[i],textblob_sent.sentiment.polarity])#writes row of data to csv
            msft_csv.close()
            if textblob_sent != 0:
                total_sent += textblob_sent.sentiment.polarity

        df = pd.read_csv('msft5.csv')
        df['Sentiment'] = pd.to_numeric(df['Sentiment'])
        most_pos_index = df['Sentiment'].argmax()
        most_neg_index = df['Sentiment'].argmin()
        neg_tweet = [df.iloc[most_neg_index]["tweet_text"],df.iloc[most_neg_index]['Sentiment']]
        pos_tweet = [df.iloc[most_pos_index]["tweet_text"],df.iloc[most_pos_index]['Sentiment']]
        #print(most_neg_index)
        #print(most_pos_index)
        avg_sent = total_sent/len(self.list)
        get_tweets.data_to_graph_sentiment(self,avg_sent,neg_tweet,pos_tweet)



    def data_to_graph_sentiment(self,avgerage_sent,most_neg_twt,most_pos_twt):
        time_now = datetime.datetime.now()
        now = time_now.replace(second=0, microsecond=0, minute=0, hour=time_now.hour-5)
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")


        weekno = datetime.datetime.today().weekday()
        current_time = datetime.datetime.now().time()
        start_time = datetime.time(9, 30)
        end_time = datetime.time(16, 15)
        msft_price = stock_info.get_live_price('msft')
        if weekno < 5:
            if now.time()> start_time and now.time()< end_time:
                print("date is within trading hours")
                '''csvFile = open('sent_stock_data3.csv', 'a', encoding="utf-8", newline="")
                csvWriter = csv.writer(csvFile)
                headers = ["date_time","avg_sentiment","stock_price","most_pos_tweet","most_neg_tweet"]
                csvWriter.writerow(headers)
                csvFile.close()'''

                sent_stock_csv = open('sent_stock_data3.csv', 'a', encoding="utf-8", newline="")
                # opens a file to write tweets and replaces newlines with empty string
                csvWriter = csv.writer(sent_stock_csv)  # creates writer object to srite data to csv

                csvWriter.writerow([dt_string, avgerage_sent, msft_price,most_pos_twt,most_neg_twt])  # writes row of data to csv
                sent_stock_csv.close()
                print("stock market price for msft stored in csv")
            else:
                print("time is outside trading hours")
                csvFile = open('sentiment_data.csv', 'a', encoding="utf-8", newline="")
                csvWriter = csv.writer(csvFile)
                headers = ["datetime", "Sentiment_value"]
                csvWriter.writerow(headers)
                csvFile.close()
                csvFile = open('sentiment_data.csv', 'a', encoding="utf-8", newline="")
                csvWriter = csv.writer(csvFile)

                csvWriter.writerow([dt_string, avgerage_sent])
                csvFile.close()


        else:
            print("date is weekend, which is outside trading hours")
            csvFile = open('sentiment_data.csv', 'a', encoding="utf-8", newline="")
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow([dt_string, avgerage_sent])
            csvFile.close()

        





if __name__ == "__main__":
    auth = OAuthHandler(consumer_key, consumer_secret)
    # create OAuthHandler object, so keys can be exchanged to authenticate a connection

    auth.set_access_token(access_token, access_token_secret)
    # sets the access token by passing the access token and secret as parameters for the function

    twitter_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    #creates api object to connect cursor to the API

    '''csvFile = open('msft5.csv', 'a', encoding="utf-8", newline="")
    csvWriter = csv.writer(csvFile)
    headers = ["date","time" ,"tweet_text","Sentiment"]
    csvWriter.writerow(headers)
    csvFile.close()'''

    cursor_obj = get_tweets() #creates class object
    cursor_obj.tweet_cursor(twitter_api)#calls tweet_curosr method with twitter api as a parameter
    cursor_obj.write_to_csv()#calls write_to_csv method to write tweets to csv file
    #cursor_obj.graph_sentiment()

