#!/usr/bin/python
# Cheerbot main code
# Author - Edward White
# Date - 23/10/2015
# -----------------------------------------------------------------------------
# ToDo
# Move strings into a separate file, with relevant functions
# Create script logger for debugging!
# Create functions to store and manage data from reddit
# Improve reply generation function (keywords, minimise local duplicates, etc)
# -----------------------------------------------------------------------------
# Full credit to the tutorial below for helping me get started with tweepy!
# http://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/

import tweepy, praw, json
from keys import consumer_key,consumer_secret,access_token,access_token_secret

class LinkStore:
	def __init__(self):
		# open a JSON file if it exists
		# load objects into list
			# title, link, date last used, reddit id
			# object = {'title': , 'link':, 'last_used':, 'id': }
			# object['title'] = 
		# if no file exists, create one and make empty list

	def add(self, ):
		# add a link to set if not a duplicate
		# add to file

	def get(self, keyword):
		# get a fresh link based on keyword (if provided)
		# update file

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

def create_reply_string(api, mention):
	# Potential case. User tweets @ both cheer bot and someone-else.
	# The other person may reply, which would involve a mention to cheerbot 
	# (but status not a reply to cheerbot). Should be treated differently!
	string = ""
	if mention.in_reply_to_screen_name == None:
		if new_user_mentioned(api, mention):
			string = "Thanks for spreading the word! Here's a cat (=^_^=)"
		else:
			string = "I'm not quite ready yet, but I'm sure my creator Edd will say when I'm done!"
	else:
		if in_reply_to_user(api.get_my_username(), mention):
			if new_user_mentioned(api, mention):
				string = "Thank You! Now more people can be cheered up ... CAT (=^_^=)"
			else:
				string = "You can tweet at me all you like, I can't cheer you up quite yet!"
		else:
			string = "Woo, go word of mouth! Happiness for all"
	return string

if __name__ == "__main__":
	# Reddit stuff
	user_agent = ("CheerMeUp Scraper v0.1")
	r = praw.Reddit(user_agent = user_agent)

	subreddit = r.get_subreddit("aww")

	for submission in subreddit.get_hot(limit = 25):
		print("Title: ", submission.title)
		print("Text: ", submission.url)
		print("Score: ", submission.score)
		print("---------------------------------\n")
		
	# Twitter stuff
	twitter = TwitterAPI()
	mentions = twitter.get_mentions()
	for mention in mentions:
		reply_str = create_reply_string(twitter, mention)
		twitter.reply(mention.id, mention.user.screen_name, reply_str)