"""Lyrically: Async Python client for fetching artist lyrical discographies."""

import logging
from pathlib import Path

import aiohttp

from .config import BASE_URL, HEADERS
from .database import Database
from .request import RequestHandler
from .utils.artist import _create_artist_url, _create_music_objects
from .utils.errors import (
    LyricallyConnectionError,
    LyricallyDatabaseError,
    LyricallyDataError,
    LyricallyError,
    LyricallyParseError,
    LyricallyRequestError,
)
from .utils.storage import _create_db_path

# Public API exports
__all__ = [
    "Lyrically",
    "LyricallyError",
    "LyricallyDatabaseError",
    "LyricallyConnectionError",
    "LyricallyDataError",
    "LyricallyParseError",
    "LyricallyRequestError",
]

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Lyrically:
    """An asynchronous Python client for fetching artist lyrical discographies."""

    def __init__(self, storage_dir: str | Path | None = None) -> None:
        """Initialize the Lyrically client.

        Args:
            storage_dir: Path to store the database. Defaults to a user-specific
                data directory.

        """
        db_path = _create_db_path(storage_dir)
        self._db = Database(db_path)
        self._session: aiohttp.ClientSession | None = None
        self._request_handler: RequestHandler | None = None
        logger.info("Lyrically instance has been initialized.")

    async def __aenter__(self) -> "Lyrically":
        """Async context manager entry to manage the session."""
        self._session = aiohttp.ClientSession(headers=HEADERS)
        self._request_handler = RequestHandler(self._session)
        await self._db.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        """Async context manager exit to clean up resources."""
        await self._db.__aexit__(exc_type, exc_val, exc_tb)
        if self._session and not self._session.closed:
            await self._session.close()

    async def get_artist_discography(self, artist_name: str) -> None:
        """Fetch and store an artist's complete discography in the database.

        Args:
            artist_name: The name of the artist to scrape.

        Raises:
            LyricallyError: If any part of the scraping process fails.
            ValueError: If the artist name is empty.

        """
        if not artist_name or not artist_name.strip():
            raise ValueError("Artist name cannot be empty")

        if not self._request_handler:
            raise LyricallyError(
                "RequestHandler not initialized. Use 'async with Lyrically(...)'"
            )

        try:
            logger.info("Starting discography scrape for artist: %s", artist_name)
            await self._db._initialize_schema()

            artist_url = _create_artist_url(artist_name, BASE_URL)
            # Use the correct method name for RequestHandler
            artist_page_html = await self._request_handler._get_html(artist_url)

            if not artist_page_html:
                raise LyricallyError(
                    f"Could not retrieve artist page for {artist_name}"
                )

            artist = _create_music_objects(artist_page_html, artist_url)
            await self._db._insert_artist(artist)

            logger.info("Discography metadata fetching process has been completed.")
            logger.info("Starting lyric fetching process.")

            tracks = [track for album in artist.albums for track in album.tracks]

            if tracks:
                await self._request_handler.get_lyrics(tracks)

            else:
                raise LyricallyError(f"No track objects were created for {artist.name}")

            logger.info("Lyric fetching process completed.")
            logger.info(
                "Successfully completed discography scrape for: %s", artist_name
            )
        except LyricallyError:
            raise
        except Exception as e:
            raise LyricallyError(
                f"An unexpected error occurred while scraping for {artist_name}"
            ) from e
