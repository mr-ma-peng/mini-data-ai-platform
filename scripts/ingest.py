"""End-to-end ingest: collect articles → embed → store in Qdrant."""

import argparse

from collector.fetch_articles import fetch_all
from embedding.pipeline import index_articles


def main():
    parser = argparse.ArgumentParser(description="Ingest articles into vector DB")
    parser.add_argument("--limit", type=int, default=10, help="Max articles per feed")
    args = parser.parse_args()

    print(f"Fetching articles (limit={args.limit} per feed)...")
    articles = fetch_all(limit_per_feed=args.limit)
    print(f"Fetched {len(articles)} articles")

    print("Embedding and indexing...")
    count = index_articles(articles)
    print(f"Indexed {count} articles into Qdrant collection")


if __name__ == "__main__":
    main()
