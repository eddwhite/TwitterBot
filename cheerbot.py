# Full credit to the tutorial below for helping me get started!
# http://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/
# List of free Python PaaS sites
# https://wiki.python.org/moin/FreeHosts

import tweepy
from keys import consumer_key,consumer_secret,access_token,access_token_secret

class TwitterAPI:
	def __init__(self):
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth)

	def tweet(self, message):
		self.api.update_status(status=message)

	def reply(self, original_id, op_screen_name, message):
		self.api.update_status(in_reply_to_status_id=original_id,
								status="@"+op_screen_name+" "+message)

	def get_mentions(self):
		last_tweet = self.api.me().status.id
		mentions = self.api.mentions_timeline(since_id=last_tweet)
		for mention in mentions:
			print(mention.user.screen_name)
			print(mention.text)
		return mentions
		

if __name__ == "__main__":
	twitter = TwitterAPI()
	mentions = twitter.get_mentions()
	for mention in mentions:
		reply_str = "I'm not ready yet!!!"
		twitter.reply(mention.id, mention.user.screen_name, reply_str)