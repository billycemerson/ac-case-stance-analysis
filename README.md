# Academy Crypto (AC) Case Stance Analysis

A YouTube crawler for collecting video metadata and comments for stance analysis on the AC (Academy Crypto) case.

## Prerequisites

- Git
- Python 3.10 or higher
- YouTube Data API v3 key

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ac-case-stance-analysis.git
cd ac-case-stance-analysis
```

### 2. Install uv

`uv` is an extremely fast Python package installer and resolver.

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, restart your terminal or reload your shell configuration.

Verify the installation:
```bash
uv --version
```

### 3. Install Python (if needed)

If you don't have Python 3.10+ installed, you can use `uv` to install it:

```bash
uv python install 3.10
```

To check your current Python version:
```bash
python --version
```

### 4. Sync Dependencies

Use `uv` to create a virtual environment and install all project dependencies:

```bash
uv sync
```

This command will:
- Create a virtual environment in `.venv/`
- Install Python dependencies listed in `pyproject.toml`
- Lock the dependencies in `uv.lock`

## Configuration

### Set Environment Variables

Create a `.env` file in the project root directory:

```bash
# On Windows (PowerShell)
New-Item -Path .env -ItemType File

# On macOS/Linux
touch .env
```

Add your YouTube API key to the `.env` file:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

**How to get a YouTube API key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Go to "Credentials" and create an API key
5. Copy the API key and paste it in your `.env` file

## Usage

### Running the Crawler

To run the YouTube crawler:

```bash
# Using uv run (recommended)
uv run python src/crawlers/main_crawler.py

# Or activate the virtual environment first
# Windows
.venv\Scripts\activate
python src/crawlers/main_crawler.py

# macOS/Linux
source .venv/bin/activate
python src/crawlers/main_crawler.py
```

### Customizing Video URLs

Edit the `links` list in `src/crawlers/main_crawler.py` to add or modify YouTube video URLs:

```python
links = [
    "https://www.youtube.com/watch?v=ULgcPz8iXmk",
    "https://www.youtube.com/watch?v=another_video_id",
    # Add more URLs here
]
```

### Output

The crawler will save two CSV files in the `data/crawler/` directory:
- `video_metadata.csv` - Contains video information (title, description, views, likes, etc.)
- `comments_data.csv` - Contains all comments from the videos

> **Note:** Data files are not stored in Git. See [DATA.md](DATA.md) for data access information.

## Project Structure

```
ac-case-stance-analysis/
├── data/
│   └── crawler/          # Output directory for crawled data
├── src/
│   └── crawlers/
│       ├── __init__.py
│       ├── main_crawler.py    # Main script to run the crawler
│       └── yt_crawler.py      # YouTube crawler implementation
├── .env                   # Environment variables (create this)
├── pyproject.toml         # Project dependencies and metadata
├── uv.lock               # Locked dependencies
└── README.md             # This file
```

## Dependencies

- `google-api-python-client` - YouTube Data API client
- `pandas` - Data manipulation and CSV export
- `python-dotenv` - Environment variable management

## Troubleshooting

### API Key Issues

If you get an error about missing API key:
```
Environment variable YOUTUBE_API_KEY is not set
```
Make sure:
1. The `.env` file exists in the project root
2. The API key is correctly formatted: `YOUTUBE_API_KEY=your_key_here`
3. There are no extra spaces or quotes around the key

### Comments Disabled

If comments are disabled on a video, you'll see an error message but the crawler will continue with other videos.

### API Quota Exceeded

YouTube API has daily quotas. If you exceed them, you'll need to wait until the next day or request a quota increase from Google Cloud Console.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.