# Full credit to the tutorial below for helping me get started!
# http://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/

import tweepy
from keys import *

class TwitterAPI:
    def __init__(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)

if __name__ == "__main__":
    twitter = TwitterAPI()
    twitter.tweet("I'm posting a tweet! Step 1 complete ... ")