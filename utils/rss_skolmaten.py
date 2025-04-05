import feedparser
import re

def fetch_skolmat():
    url = "https://skolmaten.se/api/4/rss/week/furulund?locale=sv"
    feed = feedparser.parse(url)

    for entry in feed.entries:
        entry.description = re.sub(r'<br\s*/?>', ' || ', entry.description)  # Ersätter <br> eller <br /> med mellanslag

    return feed.entries
