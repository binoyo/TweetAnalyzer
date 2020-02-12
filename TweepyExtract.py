#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import re
import nltk
import json
import datetime
import sys, os

#Variables that contains the user credentials to access Twitter API
access_token = "93149823-gLrOgrsKEkVfde6Sx4sig9N5urfmqVtR7vxB05s8z"
access_token_secret = "MPBCCRMGmxskQDhSUBXhRHuVAzIPu7ZeQN5r5uv28KGyN"
consumer_key = "sUpudDY6WII7bGcXrib7FcBPa"
consumer_secret = "DNuU8HhcHJVo4c0g6t0XrYsSm3TC6wvOip6bEL2JV7rgo0yYSr"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet_id = data["id"]
            old_Date = data["timestamp_ms"]
            new_date = str(datetime.datetime.fromtimestamp(int(old_Date)/1e3)).split(" ")[0]
            user_id = data["user"]["id"]
            tweet = data["text"].encode("utf-8")

            tweets = data["text"]
            initCsvFile = open('int_altcoin.csv', 'ab+')
            initCsvFile.write(new_date + ", " + str(tweet_id) + ", " + str(user_id) + ", ")
            initCsvFile.writelines(tweets)
            initCsvFile.write('\n')
            initCsvFile.close()

            tweet = re.sub(r"http\S+", "", tweet, flags=re.MULTILINE)
            tweet = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)","", tweet, flags=re.MULTILINE)
            tweet = re.sub(r"\d+", "", tweet)
            tweet = re.sub(r'altcoin', "", tweet, flags=re.IGNORECASE)
            tokens_text = nltk.word_tokenize(tweet)
            stopwords = nltk.corpus.stopwords.words('english')
            New_List = [word for word in tokens_text if len(word.lower()) > 4 not in stopwords]
            csvFile = open('altcoin.csv', 'ab+')
            print(new_date + ", " + str(tweet_id) + ", " + str(user_id)+ ", " + str(New_List))
            csvFile.write(new_date + ", " + str(tweet_id) + ", " + str(user_id)+ ", " )
            csvFile.writelines((word + ", ") for word in New_List)
            csvFile.write('\n')
            csvFile.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e), exc_type, fname, exc_tb.tb_lineno)

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['Altcoin'], languages=["en"])
