# Data Access

This document provides information on accessing the datasets for this project.

## Overview

Large data files are **not** stored in this repository to keep it lightweight and efficient. Instead, they are hosted externally and can be accessed via the links below.

## Dataset Location

### Option 1: Google Drive (Recommended)
📁 **[Download Dataset from Google Drive](https://drive.google.com/drive/folders/16sRGh1YnwKSfIHHmIth9Eda_a9ijtPxB?usp=sharing)**

Replace `#` with your actual Google Drive link once you upload the data.

### Option 2: Generate Your Own Data

You can generate the data yourself by running the crawler:

```bash
uv run python src/crawlers/main_crawler.py
```

This will create the following files in `data/crawler/`:
- `video_metadata.csv` - Video information
- `comments_data.csv` - Comments from videos

## Data Structure

### Directory Layout

```
data/
└── crawler/
    ├── video_metadata.csv
    └── comments_data.csv
```

### File Descriptions

#### `video_metadata.csv`
Contains metadata for each crawled video:
- `video_id` - YouTube video ID
- `title` - Video title
- `description` - Video description
- `published_at` - Publication date
- `view_count` - Number of views
- `like_count` - Number of likes
- `comment_count` - Number of comments
- `channel_title` - Channel name

#### `comments_data.csv`
Contains all comments from crawled videos:
- `video_id` - Associated video ID
- `comment_id` - Unique comment identifier
- `author` - Comment author
- `text` - Comment text
- `published_at` - Comment date
- `like_count` - Number of likes on comment
- `reply_count` - Number of replies

## Setup Instructions

### 1. Download Data (if using shared dataset)

1. Click the Google Drive link above
2. Download the files to your local machine
3. Place them in the appropriate directory:
   ```
   ac-case-stance-analysis/
   └── data/
       └── crawler/
           ├── video_metadata.csv
           └── comments_data.csv
   ```

### 2. Generate Data (if running crawler)

Follow the instructions in the main [README.md](README.md) to:
1. Set up your YouTube API key
2. Configure the video URLs to crawl
3. Run the crawler