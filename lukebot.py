from cobe.brain import Brain
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import time
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('twitterKeys.ini')

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

class ReplyToTweet(StreamListener):

    def on_data(self, data):
        print data
        tweet = json.loads(data.strip())
        b = Brain("cobe.brain")

        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == account_user_id

        if retweeted is not None and not retweeted and not from_self:

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')

            chatResponse = b.reply(tweetText)

            replyText = '@' + screenName + ' ' + chatResponse

            #check if repsonse is over 140 char
            if len(replyText) > 140:
                replyText = replyText[0:137] + '...'

            print('Tweet ID: ' + tweetId)
            print('From: ' + screenName)
            print('Tweet Text: ' + tweetText)
            print('Reply Text: ' + replyText)

            # If rate limited, the status posts should be queued up and sent on an interval
            api.update_status(status=replyText, in_reply_to_status_id=tweetId)

    def on_error(self, status):
        print status

for follower in tweepy.Cursor(api.followers).items():
	print(follower.screen_name)

streamListener = ReplyToTweet()
twitterStream = Stream(auth, streamListener)
twitterStream.userstream(_with='user')



