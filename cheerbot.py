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
		#for mention in mentions:
		#	print(mention.user.screen_name)
		#	print(mention.text)
		return mentions

	def get_my_username(self):
		return self.api.auth.get_username()

	def get_tweet(self, status_id):
		return self.api.get_status(id=status_id)

def get_users_mentioned(text):
	users=[]
	for word in text.split():
		if word.startswith('@'):
			users.append(word[1:])
	return users

def new_user_mentioned(api, mention):
	users = get_users_mentioned(mention.text)
	users.remove(api.get_my_username())
	prev_status = api.get_tweet(mention.in_reply_to_status_id_str)
	prev_users = get_users_mentioned(prev_status.text)
	#need to remove the original person mentioned
	print(prev_users)
	new_users = set(users) - set(prev_users)
	if not new_users:
		return False
	else:
		return True

def create_reply_string(api, mention):
	# If in reply to a tweet by bot, change string!
	string = ""
	if mention.in_reply_to_screen_name == api.get_my_username():
		if new_user_mentioned(api, mention):
			string = "Thanks for spreading the word!"
		else:
			string = "You can tweet at me all you like, I can't cheer you up quite yet!"
	else:
		string = "I'm not quite ready yet, but I'm sure my creator Edd will say when I'm done!"
	return string

if __name__ == "__main__":
	twitter = TwitterAPI()
	mentions = twitter.get_mentions()
	for mention in mentions:
		reply_str = create_reply_string(twitter, mention)
		print(reply_str)
		#twitter.reply(mention.id, mention.user.screen_name, reply_str)