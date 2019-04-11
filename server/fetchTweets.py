import sys
import tweepy
import json
import os
import pandas as pd
from datetime import datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
filePath = os.path.join(THIS_FOLDER, 'files')

tmpFilePath = os.path.join(THIS_FOLDER, 'tempFiles')

keysFile = os.path.join(THIS_FOLDER, 'access_keys.json')
with open(keysFile) as f:
    configKeysData = json.load(f)

serverFile = os.path.join(THIS_FOLDER, 'server_config.json')
with open(serverFile) as f:
    configData = json.load(f)

# keys
consumer_key = configKeysData["consumer_key"]
consumer_secret = configKeysData["consumer_secret"]
access_token = configKeysData["access_token"]
access_token_secret = configKeysData["access_token_secret"]

TWEET_LIMIT = configData["tweet_limit"]
TIME_OUT_SECONDS = configData["fetch_timeout_seconds"]


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api=None, filename='tempFile.txt'):
        self.n = 0
        self.api = api
        self.filename = filename
        self.dataList = []
        self.starttime = datetime.now()

    def on_status(self, status):
        try:
            name = status.author.screen_name
            textTwitter = status.text

            # print(name)
            # print(textTwitter)
            # print('\n')

            self.dataList.append((name, textTwitter, textTwitter))

            self.n = self.n+1
            timediff = datetime.now() - self.starttime
            if (self.n < int(TWEET_LIMIT)) and (timediff.seconds < int(TIME_OUT_SECONDS)):
                return True
            else:
                df = pd.DataFrame.from_records(self.dataList)
                df.to_csv(os.path.join(tmpFilePath, self.filename),
                          index=False, header=False)
                print('maxnum = '+str(self.n))
                return False

        except Exception as e:
            print(e)

    def on_error(self, status_code):
        # print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        # print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream


def streamTweets(vQueries, vFilename):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    TweetsData = tweepy.streaming.Stream(
        auth, CustomStreamListener(filename=vFilename))

    setTerms = vQueries

    TweetsData.filter(None, setTerms, languages=["en"])
