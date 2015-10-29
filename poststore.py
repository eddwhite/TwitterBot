#!/usr/bin/python
# PostStore class
# Author - Edward White
# Date - 27/10/2015
# -----------------------------------------------------------------------------
# This handles the storage of all reddit posts, along with adding new posts to
# the database

import json, os, re, time
import praw # for testing

class PostStore:
	def __init__(self):
		# Create/open post database
		if not os.path.exists('post_database.txt'):
			fo = open('post_database.txt', 'w')
			json.dump([], fo)
			fo.close()
		with open('post_database.txt', 'r') as fi:
			self.posts = json.load(fi)
		# Open animal database
		with open('animal_database.txt', 'r') as fi:
			self.animals = json.load(fi)

	def add(self, post):
		# separate file extension from url
		post['url'], post['ext'] = os.path.splitext(post['url'])
		url_parts = post['url'].split('/')
		# Check url is a valid, non gallery/album imgur
		if not (('i.imgur.com' in url_parts) or ('imgur.com' in url_parts)):
			return
		if 'a' in url_parts or 'gallery' in url_parts:
			return
		# Only store the 7 digit ID at the end of the link
		post['url'] = [part for part in url_parts if len(part)==7].pop()
		# make sure post would fit in a tweet
		if len(post['url']+post['title']) + 20 > 140:
			return
		post['last_used'] = 0
		post['animal'] = []
		# check for references to animals(s) in the image
		for word in re.findall('\w+', post['title']):
			for species in self.animals:
				if word.lower() in species or word.lower().rstrip('s') in species:
					post['animal'].append(species[0])
				if word.lower() == 'reddit'
					return
		# check link is not already in database
		if [match for match in self.posts if match['url'] == post['url']]:
			return
		self.posts.append(post)

	def get(self, text, max_str_len):
		# create a fresh post based on input text
		# find all animal references in input text
		keywords = set()
		for word in re.findall('\w+', text):
			for species in self.animals:
				if word.lower() in species or word.lower().rstrip('s') in species:
					keywords.add(species[0])
		# return the post with the highest match that has the smallest last used
		x = self.posts[0]
		x_rating = 0
		for post in self.posts:
			if len(post['title']) + 20 <= max_str_len:
				match_rating = len(keywords.intersection(post['animal']))
				if match_rating > x_rating:
					x = post
					x_rating = match_rating
				elif match_rating==x_rating and post['last_used']<x['last_used']:
					x = post
					x_rating = match_rating
		# update last used (changing x will update database)
		x['last_used'] = int(time.time())
		# create post string
		string = '\"' + x['title'] + '\"\nimgur.com/' + x['url']
		return string

	def flush(self):
		with open('post_database.txt', 'w') as fo:
			json.dump(self.posts, fo, indent = 4)
		with open('animal_database.txt', 'w') as fo:
			json.dump(self.animals, fo, indent = 4)

# use for testing
if __name__ == "__main__":
	posts = PostStore()
	# Reddit stuff
	user_agent = ("CheerMeUp Scraper v0.1")
	r = praw.Reddit(user_agent = user_agent)

	subreddit = r.get_subreddit("aww") # lolcats and awwgifs also could be good

	for submission in subreddit.get_top(limit = 100):
		posts.add({'title': submission.title, 'url': submission.url})
	print(posts.get('I want a kitten to cheer me up please', 100))
	posts.flush()
