import feedparser
import re
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from urllib.parse import urlparse
from api.models import News, Tag


class Command(BaseCommand):
    help = 'Parses RSS Feed and saves into Database'

    def remove_html_tags(self, text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def concatenate_with_zero(self, value):
        return f'0{value}' if int(value) < 10 else value

    def handle(self, *args, **options):
        self.stdout.write('Parsing process has started')
        NewsSources = ["https://feeds.feedburner.com/niebezpiecznik/",
                       "http://feeds.feedburner.com/sekurak", "https://www.cert.pl/feed/"]
        for NewsSource in NewsSources:
            NewsFeed = feedparser.parse(NewsSource)
            entry = NewsFeed.entries
            for entry in reversed(NewsFeed.entries):
                if (NewsSource == "https://www.cert.pl/feed/"):
                    href = entry['link']
                    d = entry['published_parsed']
                    updated_date = f'{d.tm_year}-{self.concatenate_with_zero(d.tm_mon)}-{self.concatenate_with_zero(d.tm_mday)}T{self.concatenate_with_zero(d.tm_hour)}:{self.concatenate_with_zero(d.tm_min)}:{self.concatenate_with_zero(d.tm_sec)}Z'
                elif (NewsSource == "http://feeds.feedburner.com/sekurak"):
                    href = entry['feedburner_origlink']
                    d = entry['published_parsed']
                    updated_date = f'{d.tm_year}-{self.concatenate_with_zero(d.tm_mon)}-{self.concatenate_with_zero(d.tm_mday)}T{self.concatenate_with_zero(d.tm_hour)}:{self.concatenate_with_zero(d.tm_min)}:{self.concatenate_with_zero(d.tm_sec)}Z'
                else:
                    href = entry['feedburner_origlink']
                    updated_date = entry['updated']
                parsedDomain = urlparse(href)
                source = parsedDomain.netloc.replace('www.', '')
                title = entry['title']
                summary = entry['summary']

                news, news_created = News.objects.get_or_create(
                    title=title, summary=self.remove_html_tags(summary), source=source, href=href, date=datetime.strptime(updated_date, '%Y-%m-%dT%H:%M:%SZ'))
                if(news_created):
                    for tag_entry in entry['tags']:
                        tag, _ = Tag.objects.get_or_create(
                            name=tag_entry['term'])
                        news.tags.add(tag)
                    self.stdout.write(f'Successfuly saved news: [{news}]')
        self.stdout.write('Parsing process has finished')
