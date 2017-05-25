import tweepy
import random
import ConfigParser
from time import sleep

config = ConfigParser.ConfigParser()
config.read('twitterKeys.ini')
file = open("tweets.txt", "r")

consumer_key = config.get('apikey', 'key')
consumer_secret = config.get('apikey', 'secret')
access_token = config.get('token', 'token')
access_token_secret = config.get('token', 'secret')
account_screen_name = config.get('app', 'account_screen_name')
stream_rule = config.get('app', 'rule')
account_user_id = config.get('app', 'account_user_id')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

while(True):
	file = open("tweets.txt", "r")
	lines = file.readlines()
	random_line = random.choice(lines)

	api.update_status(random_line)
	print("tweeted")

	file.close()
	file = open("tweets.txt","w")
	fileUsed = open("usedTweets.txt", "a")
	for line in lines:
		if line != random_line:
			file.write(line)
		else:
			fileUsed.write(line)
	file.close()

	sleep(32500)
