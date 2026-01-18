import os
import sys
import logging
from yt_crawler import YouTubeCrawler


def main_crawler() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    logger = logging.getLogger(__name__)

    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        logger.error("Environment variable YOUTUBE_API_KEY is not set")
        sys.exit(1)

    links = [
        "https://www.youtube.com/watch?v=ULgcPz8iXmk"
    ]

    try:
        crawler = YouTubeCrawler(api_key=api_key)
        video_df, comments_df = crawler.crawl(links)

        logger.info("Crawling finished successfully")
        logger.info("Video metadata rows: %s", len(video_df))
        logger.info("Comments rows: %s", len(comments_df))

    except Exception:
        logger.exception("Error while running YouTubeCrawler")
        sys.exit(1)


if __name__ == "__main__":
    main_crawler()