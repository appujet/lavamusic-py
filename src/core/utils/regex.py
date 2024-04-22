import re

# Regex for matching YouTube URLs
YOUTUBE_URL_REGEX = re.compile(
    r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)"
    r"(?:/watch\?v=|/playlist\?list=|/album/|/channel/|/c/|/user/)"
    r"|(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)"
    r"(?:/shorts/)"
    r"([a-zA-Z0-9\-_]+)"
)

# regex for url
URL = re.compile(r"^(?:http|ftp)s?://")


def is_youtube_url(url: str) -> bool:
    """Check if a URL is a YouTube URL."""
    return YOUTUBE_URL_REGEX.match(url) is not None


def is_url(url: str) -> bool:
    """Check if a URL or not"""
    return URL.match(url) is not None
