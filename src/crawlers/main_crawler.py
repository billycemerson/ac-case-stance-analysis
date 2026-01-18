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
        "https://www.youtube.com/shorts/L32I6RUneEg",
        "https://www.youtube.com/watch?v=5paK9KdQviI",
        "https://www.youtube.com/watch?v=vm38zk-SMes",
        "https://www.youtube.com/watch?v=7Qwx_FSk6OU",
        "https://www.youtube.com/shorts/H3K9tD3u1Ag",
        "https://www.youtube.com/watch?v=Yb_6S-DzfHQ",
        "https://www.youtube.com/shorts/8Vbr2XWe17c",
        "https://www.youtube.com/watch?v=EbLJ6qZLkrA",
        "https://www.youtube.com/watch?v=siTm0_lsl7Y",
        "https://www.youtube.com/watch?v=suty-eFK-u4",
        "https://www.youtube.com/watch?v=awVtH5DOPJg",
        "https://www.youtube.com/watch?v=H7eBuVaPELE",
        "https://www.youtube.com/shorts/kCyNeUxdKCQ",
        "https://www.youtube.com/watch?v=AHWTpT2HV9k",
        "https://www.youtube.com/shorts/TtW3gc0rHBc",
        "https://www.youtube.com/shorts/Iq_JKcqUIyY" 
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