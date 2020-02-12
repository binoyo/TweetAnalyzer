#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys, os

#Variables that contains the user credentials to access Twitter API
access_token = "93149823-gLrOgrsKEkVfde6Sx4sig9N5urfmqVtR7vxB05s8z"
access_token_secret = "MPBCCRMGmxskQDhSUBXhRHuVAzIPu7ZeQN5r5uv28KGyN"
consumer_key = "sUpudDY6WII7bGcXrib7FcBPa"
consumer_secret = "DNuU8HhcHJVo4c0g6t0XrYsSm3TC6wvOip6bEL2JV7rgo0yYSr"

# Make a temporary file that can load all the tweets coming. Keep it open throughout the application run
csvFile = open('MainAltcoin.csv', 'ab+')

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    # Read each data and write it into the csv file
    def on_data(self, data):
        try:
            csvFile.write(data)
            csvFile.write('\n')
        except Exception as e:

            # Capture all the exceptions from OS level that can occur in this application.
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

    #This line filter Twitter Streams to capture data by the keywords: 'Altcoin'
    stream.filter(track=['Altcoin'], languages=["en"])

csvFile.close()
