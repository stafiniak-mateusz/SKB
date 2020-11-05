import sys
import tweepy
import datetime
import time
TWEET_AUTH = ['Q5eYhiDb7cbnWT6ayiM6ofnEi', '86uNG87qQEbsnDvfm7V7MgCTBK6xmbRxoC4yrZe2BZoOZNGrXw',
              '1271574958053998597-KHBfGfJTJ9ScxbGRf6RMJDsFFvEmD0', 'svnpz5KGamsyblihTwhf7Y50B4wKc4kjIoRmjZK4iGO8w']


auth = tweepy.OAuthHandler(TWEET_AUTH[0], TWEET_AUTH[1])
auth.set_access_token(TWEET_AUTH[2], TWEET_AUTH[3])
api = tweepy.API(auth)


def get_tweets(api, username):
    page = 1
    deadend = False
    while True:
        tweets = api.user_timeline(username, page=page)
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days < 14:
                title = tweet.user.name
                try:
                    summary = tweet.text.split('https://')[0]
                except:
                    summary = 'Not Provided'
                try:
                    href = 'https://'+tweet.text.split('https://')[1]
                except:
                    href = 'Not Provided'

                print("\n")
                if(summary != 'Not Provided' and href != 'Not Provided'):
                    print(title)
                    print(summary)
                    print(href)
            else:
                deadend = True
                return
        if not deadend:
            page+1
            time.sleep(500)


get_tweets(api, "CERT_OPL")
