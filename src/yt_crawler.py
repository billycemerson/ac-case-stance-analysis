import os
import sys
import logging
import time
from typing import List, Dict, Tuple, Optional
from urllib.parse import urlparse, parse_qs
from pathlib import Path

import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors

from dotenv import load_dotenv
load_dotenv()


class YouTubeCrawler:
    def __init__(self, api_key: str, sleep_seconds: int = 1) -> None:
        self.api_key = api_key
        self.sleep_seconds = sleep_seconds

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        self.youtube = googleapiclient.discovery.build(
            "youtube",
            "v3",
            developerKey=self.api_key
        )

    def extract_video_id(self, url: str) -> Optional[str]:
        """Get the YouTube id from given url"""

        if not url:
            return None

        parsed = urlparse(url)


        if parsed.hostname in ("www.youtube.com", "youtube.com"):
            if parsed.path == "/watch":
                return parse_qs(parsed.query).get("v", [None])[0]
            elif parsed.path.startswith("/shorts/"):
                return parsed.path.split("/shorts/")[1].split("?")[0]

        if parsed.hostname == "youtu.be":
            return parsed.path.lstrip("/")

        return None

    def extract_video_ids(self, urls: List[str]) -> List[str]:
        return [
            vid for vid in (self.extract_video_id(url) for url in urls)
            if vid
        ]

    def get_video_metadata(self, video_id: str) -> Optional[Dict]:
        request = self.youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id
        )

        response = request.execute()

        if not response.get("items"):
            return None

        item = response["items"][0]

        return {
            "video_id": video_id,
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "channel_id": item["snippet"]["channelId"],
            "channel_title": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"],
            "view_count": item["statistics"].get("viewCount"),
            "like_count": item["statistics"].get("likeCount"),
            "comment_count": item["statistics"].get("commentCount"),
            "duration": item["contentDetails"]["duration"],
        }

    def get_comments(self, video_id: str) -> List[Dict]:
        comments = []
        page_token = None

        while True:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=page_token,
                textFormat="plainText"
            )
            response = request.execute()

            comments.extend(response.get("items", []))

            page_token = response.get("nextPageToken")
            if not page_token:
                break

            time.sleep(self.sleep_seconds)

        return comments

    def crawl(self, urls: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Crawl video metadata and comments from a list of YouTube URLs
        and save results to CSV files.
        """
        video_ids = self.extract_video_ids(urls)

        video_metadata_rows: List[Dict] = []
        comments_rows: List[Dict] = []

        for video_id in video_ids:
            print(f"Processing video_id={video_id}")

            meta = self.get_video_metadata(video_id)
            if meta:
                video_metadata_rows.append(meta)

            try:
                comments = self.get_comments(video_id)
                for cm in comments:
                    snippet = cm["snippet"]["topLevelComment"]["snippet"]

                    comments_rows.append({
                        "video_id": video_id,
                        "comment_id": cm["snippet"]["topLevelComment"]["id"],
                        "author_name": snippet["authorDisplayName"],
                        "author_channel_id": snippet.get(
                            "authorChannelId", {}
                        ).get("value"),
                        "text_display": snippet["textDisplay"],
                        "text_original": snippet["textOriginal"],
                        "like_count": snippet["likeCount"],
                        "published_at": snippet["publishedAt"],
                        "updated_at": snippet["updatedAt"],
                    })

            except googleapiclient.errors.HttpError as e:
                print(f"[ERROR] Failed fetching comments | video_id={video_id} | {e}")

        video_metadata_df = pd.DataFrame(video_metadata_rows)
        comments_df = pd.DataFrame(comments_rows)

        output_dir = Path("../data")
        output_dir.mkdir(parents=True, exist_ok=True)

        video_metadata_df.to_csv(
            output_dir / "video_metadata.csv",
            index=False,
            encoding="utf-8-sig"
        )
        comments_df.to_csv(
            output_dir / "comments_data.csv",
            index=False,
            encoding="utf-8-sig"
        )

        return video_metadata_df, comments_df