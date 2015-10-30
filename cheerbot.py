#!/usr/bin/python
# Cheerbot main code
# Author - Edward White
# Date - 27/10/2015
# -----------------------------------------------------------------------------
# ToDo
# Move strings into a separate file, with relevant functions
# Create script logger for debugging!
# Create functions to store and manage data from reddit
# Improve reply generation function (keywords, minimise similar tweets, etc)
# -----------------------------------------------------------------------------
# Full credit to the tutorial below for helping me get started with tweepy!
# http://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/

import tweepy, praw, poststore, time, re
from keys import consumer_key,consumer_secret,access_token,access_token_secret

class TwitterAPI:
	def __init__(self):
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth)

	def tweet(self, message):
		self.api.update_status(status=message)

	def reply(self, original_id, message):
		self.api.update_status(in_reply_to_status_id=original_id,
								status=message)

	def get_mentions(self):
		last_tweet = self.api.me().status.id
		return self.api.mentions_timeline(since_id=last_tweet)

	def get_my_username(self):
		return self.api.auth.get_username()

	def get_tweet(self, status_id):
		return self.api.get_status(id=status_id)

def get_users_mentioned(text):
	users=[]
	for word in text.split():
		if word.startswith('@'):
			users.append(word[1:]) # remove leading @ symbol
	return users

def new_user_mentioned(api, mention):
	users = get_users_mentioned(mention.text)
	users.remove(api.get_my_username()) # mentions must contain bots username, so remove
	if not users:
		return False
	else:
		return True

def in_reply_to_user(username, mention):
	if mention.in_reply_to_screen_name == username:
		return True
	else:
		return False

def create_reply_string(twitter, mention):
	# Potential case. User tweets @ both cheer bot and someone-else.
	# The other person may reply, which would involve a mention to cheerbot
	# (but status not a reply to cheerbot). Should be treated differently!
	string = ""
	if mention.in_reply_to_screen_name == None:
		if new_user_mentioned(twitter, mention):
			string = "Thanks for spreading the word!\n"
		else:
			string = "Here you go!\n"
	else:
		if in_reply_to_user(twitter.get_my_username(), mention):
			if new_user_mentioned(twitter, mention):
				string = "Thank You! Now more people can be cheered up ...\n"
			else:
				string = "Want more? I hope you like this one as well\n"
		else:
			string = "Woo, go word of mouth! Happiness for all\n"
	return string

if __name__ == "__main__":
	# Database initialisation
	posts = poststore.PostStore()

	# Reddit stuff - only do every half hour
	# so hacky!
	cur_minute = time.localtime().tm_min
	if cur_minute in [0, 1, 30, 31]:
		user_agent = ("CheerMeUp Scraper v0.1")
		r = praw.Reddit(user_agent = user_agent)
		subreddit = r.get_subreddit("aww") # lolcats and awwgifs also could be good
		for submission in subreddit.get_hot(limit = 50):
			posts.add({'title': submission.title, 'url': submission.url})

	# Twitter stuff
	twitter = TwitterAPI()
	mentions = twitter.get_mentions()
	for mention in mentions:
		reply_str = '@'+mention.user.screen_name+' '
		reply_str += create_reply_string(twitter, mention)
		reply_str += posts.get(re.sub(r'@\w+',r'',mention.text), 140-len(reply_str))
		twitter.reply(mention.id, reply_str)
	# Update database
	posts.flush()
