from cobe.brain import Brain
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import time
import json

consumer_key = '8BweTt1eTRnHPYFpBxYxiA1n7'
consumer_secret = 'HdNaf3pBRddlcCjVyhNeZqk7nvefUJKdqvWCIyW89eiWr0019w'
access_token = '866308102534176768-5OjIWdbwFk4uNcGlOADXCK8Fr2BPzxU'
access_token_secret = 'fthxy4IR9yBeuckDdrQhHhfSia52tf1OigzOoY8ohWifi'
account_screen_name = 'lukennethbot'
stream_rule = '@lukennethbot'
account_user_id = '866308102534176768'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        
        return True

    def on_error(self, status):
        print(status)

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


streamListener = ReplyToTweet()
twitterStream = Stream(auth, streamListener)
twitterStream.userstream(_with='user')

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
# 	print tweet.text

# l = StdOutListener()
# stream = Stream(auth, l)
# stream.filter(track=['@LuKenneth_'])


