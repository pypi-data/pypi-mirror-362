"""Request package: HTTP requests and HTML parsing for Lyrically."""

import logging

import aiohttp
from bs4 import BeautifulSoup

from ..utils.errors import LyricallyRequestError
from ..utils.models import Track

logger = logging.getLogger(__name__)


class RequestHandler:
    """Manages the sending and validation of HTTP requests."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the RequestHandler.

        Args:
            session: An aiohttp.ClientSession to be used for all requests.

        """
        self._session = session

    async def _get_html(self, url: str) -> BeautifulSoup | None:
        """Fetch and parse the HTML content from a given URL.

        Args:
            url: The URL to fetch the HTML from.

        Returns:
            A BeautifulSoup object if successful, None otherwise.

        Raises:
            LyricallyRequestError: If a network error occurs or the page
                is invalid.

        """
        logger.debug("Fetching HTML from URL: %s", url)
        try:
            async with self._session.get(url) as response:
                response.raise_for_status()
                html_text = await response.text()
                return self._validate_and_parse_html(html_text, url)
        except aiohttp.ClientError as e:
            raise LyricallyRequestError(f"Request failed for {url}") from e

    def _validate_and_parse_html(
        self, html_text: str, url: str
    ) -> BeautifulSoup | None:
        """Validate the HTML content and parse it.

        Args:
            html_text: The raw HTML string.
            url: The URL from which the HTML was fetched.

        Returns:
            A BeautifulSoup object if the HTML is valid, None otherwise.

        Raises:
            LyricallyRequestError: If the page indicates an access error.

        """
        if not html_text or not html_text.strip():
            logger.debug("Received empty HTML content from %s", url)
            return None

        try:
            soup = BeautifulSoup(html_text, "lxml")
        except Exception as e:
            raise LyricallyRequestError(f"Failed to parse HTML from {url}") from e

        # Check for access denied in title
        title_tag = soup.find("title")
        if title_tag:
            title_text = title_tag.get_text(strip=True).lower()
            if "access denied" in title_text:
                raise LyricallyRequestError(f"Access denied when accessing {url}")

        return soup

    async def get_lyrics(self, tracks: list[Track]) -> None:
        """Fetch lyrics for the given tracks.

        Args:
            tracks: An iterable of track objects with a 'url' attribute.

        """
        for track in tracks:
            await self._get_html(track.url)
