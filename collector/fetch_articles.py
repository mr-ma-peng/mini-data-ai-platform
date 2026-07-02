"""Data collectors — fetch articles from RSS feeds and other sources."""

from dataclasses import dataclass
from datetime import datetime

import feedparser

DEFAULT_FEEDS = [
    "https://hnrss.org/frontpage",
    "https://blog.langchain.dev/rss/",
]


@dataclass
class Article:
    title: str
    url: str
    content: str
    published_at: datetime | None = None
    source: str = ""


def fetch_rss(feed_url: str, limit: int = 50) -> list[Article]:
    """Parse an RSS feed and return up to `limit` articles."""
    feed = feedparser.parse(feed_url)
    articles: list[Article] = []
    for entry in feed.entries[:limit]:
        published = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6])
        articles.append(
            Article(
                title=entry.get("title", ""),
                url=entry.get("link", ""),
                content=entry.get("summary", entry.get("description", "")),
                published_at=published,
                source=feed_url,
            )
        )
    return articles


def fetch_all(feeds: list[str] | None = None, limit_per_feed: int = 50) -> list[Article]:
    """Fetch articles from multiple RSS feeds."""
    feeds = feeds or DEFAULT_FEEDS
    articles: list[Article] = []
    for feed_url in feeds:
        articles.extend(fetch_rss(feed_url, limit=limit_per_feed))
    return articles
