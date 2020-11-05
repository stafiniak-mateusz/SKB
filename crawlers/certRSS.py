import feedparser
import time
from urllib.parse import urlparse

NewsSource = "https://www.cert.pl/feed/"
NewsFeed = feedparser.parse(NewsSource)


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def concatenate_with_zero(value):
    if(int(value) < 10):
        return f'0{value}'
    else:
        return value


print(NewsFeed.entries[9]['tags'])
# parsedDomain = urlparse(NewsFeed.entries[9]['link'])
# print(parsedDomain.netloc.replace('www.', '').replace('www.', ''))
# print(NewsFeed.entries[9]['title'])
# d = NewsFeed.entries[9]['published_parsed']

# print(f'{d.tm_year}-{concatenate_with_zero(d.tm_mon)}-{concatenate_with_zero(d.tm_mday)}T{concatenate_with_zero(d.tm_hour)}:{concatenate_with_zero(d.tm_min)}:{concatenate_with_zero(d.tm_sec)}')
# print(remove_html_tags(NewsFeed.entries[0]['summary']))
# print()
