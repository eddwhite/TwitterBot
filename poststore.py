#!/usr/bin/python
# PostStore class
# Author - Edward White
# Date - 27/10/2015
# -----------------------------------------------------------------------------
# This handles the storage of all reddit posts, along with adding new posts to
# the database

import json, os

class PostStore:
	posts = []
	animals = [[]]
	def __init__(self):
		# Create/open post database
		if not os.path.exists('post_database.txt'):
			fo = open('post_database.txt', 'w')
			json.dump([], fo)
			fo.close()
		with open('post_database.txt', 'r') as fi:
			posts = json.load(fi)
		# Open animal database
		with open('animal_database.txt', 'r') as fi:
			animals = json.load(fi)

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
		# make sure post would fit in a tweet (10 for imgur link and space)
		if len(post['url']+post['title']) + 11 > 140:
			return
		post['last_used'] = 0
		post['animal'] = []
		# check for references to animals(s) in the image
		for word in post['title'].split():
			for species in animals:
				if word.lower() in species:
					post['animal'].append(species[0])
		# check link is not already in database
		posts.append(post)

	def get(self, text):
		# create a fresh post based on text if possible

	def flush(self):
		with open('post_database.txt', 'w') as fo:
			json.dump(posts, fo, indent = 4)
		with open('post_database.txt', 'w') as fo:
			json.dump(animals, fo, indent = 4)
