import feedparser
from django.core.management.base import BaseCommand, CommandError
from urllib.parse import urlparse
from api.models import News, Tag
import sys
import tweepy
import datetime
import time

TWEET_AUTH = ['Q5eYhiDb7cbnWT6ayiM6ofnEi', '86uNG87qQEbsnDvfm7V7MgCTBK6xmbRxoC4yrZe2BZoOZNGrXw',
              '1271574958053998597-KHBfGfJTJ9ScxbGRf6RMJDsFFvEmD0', 'svnpz5KGamsyblihTwhf7Y50B4wKc4kjIoRmjZK4iGO8w']


class Command(BaseCommand):
    help = 'Scraps Twitter for tweets'

    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(TWEET_AUTH[0], TWEET_AUTH[1])
        auth.set_access_token(TWEET_AUTH[2], TWEET_AUTH[3])
        api = tweepy.API(auth)
        self.stdout.write('Scraping process has started')
        page = 1
        deadend = False
        while True:
            tweets = api.user_timeline("CERT_OPL", page=page)
            for tweet in tweets:
                if (datetime.datetime.now() - tweet.created_at).days < 14:
                    summary = 'From Twitter of '+tweet.user.name
                    try:
                        title = tweet.text.split('https://')[0]
                    except:
                        title = 'Not Provided'
                    try:
                        href = 'https://'+tweet.text.split('https://')[1]
                    except:
                        href = 'Not Provided'
                    if(title != 'Not Provided' and href != 'Not Provided'):
                        news, news_created = News.objects.get_or_create(
                            title=title, summary=summary, source="Orange_Tweets", href=href, date=tweet.created_at)
                    else:
                        news_created = None
                    if(news_created):
                        tagOrange, _ = Tag.objects.get_or_create(
                            name='Orange CERT')
                        tagTwitter, _ = Tag.objects.get_or_create(
                            name='Twitter')
                        news.tags.add(tagOrange)
                        news.tags.add(tagTwitter)
                        self.stdout.write(f'Successfuly saved news: [{news}]')
                else:
                    deadend = True
                    return
            if not deadend:
                page+1
                time.sleep(500)
        self.stdout.write('Parsing process has finished')
