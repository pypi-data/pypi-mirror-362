"""Async SQLite management for lyrically (connection, schema, models)."""

import logging
from contextlib import suppress
from pathlib import Path

import aiosqlite

from ..utils.errors import LyricallyConnectionError, LyricallyDatabaseError
from ..utils.models import Album, Artist, Track
from .initialize import _initialize_database

logger = logging.getLogger(__name__)


class Database:
    """Manages all database operations, including connection and schema."""

    def __init__(self, db_path: Path) -> None:
        """Initialize the Database handler.

        Args:
            db_path: The file path for the SQLite database.

        """
        self._db_path = db_path
        self._is_setup = False
        self._conn: aiosqlite.Connection | None = None
        logger.debug("Database instance initialized for path: %s", db_path)

    async def __aenter__(self) -> "Database":
        """Enter the async context manager, establishing the connection."""
        await self._connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        """Exit the async context manager, closing the connection."""
        await self._disconnect()

    async def _connect(self) -> None:
        """Establish and configure the database connection."""
        if self._conn is None:
            logger.debug("Connecting to database.")

            try:
                self._conn = await aiosqlite.connect(self._db_path, timeout=10.0)

                # Enable foreign key support and performance optimizations
                await self._conn.execute("PRAGMA foreign_keys = ON;")
                await self._conn.execute("PRAGMA synchronous = NORMAL;")
                await self._conn.execute("PRAGMA cache_size = -4000;")  # 4MB cache
                await self._conn.execute("PRAGMA temp_store = MEMORY;")

                logger.info("Database connection established.")
            except aiosqlite.Error as e:
                raise LyricallyConnectionError("Failed to connect to database") from e

    async def _disconnect(self) -> None:
        """Close the database connection if it exists."""
        if self._conn:
            logger.debug("Disconnecting from database.")

            try:
                await self._conn.close()
                logger.info("Database connection closed.")
            except aiosqlite.Error as e:
                raise LyricallyConnectionError(
                    "An error occurred while closing the database connection"
                ) from e
            finally:
                self._conn = None

    async def _initialize_schema(self) -> None:
        """Initialize the database schema if it hasn't been set up yet."""
        if not self._is_setup:
            logger.info("Initializing database schema.")

            if not self._conn:
                raise LyricallyConnectionError(
                    "Cannot initialize DB schema, no active connection."
                )
            await _initialize_database(self._conn)
            self._is_setup = True
            logger.info("Database schema initialized successfully.")

    async def _insert_artist(self, artist: Artist) -> None:
        """Insert an artist and their complete discography into the database.

        Args:
            artist: The artist object containing all albums and tracks.

        Raises:
            LyricallyDatabaseError: If database insertion fails.

        """
        if not self._conn:
            raise LyricallyConnectionError("No active database connection")

        logger.debug("Attempting to insert artist '%s' in DB.", artist.name)
        cursor = None

        try:
            cursor = await self._conn.cursor()
            artist_id = await self._insert_artist_record(cursor, artist)
            await self._insert_artist_albums(cursor, artist_id, artist.albums)
            await self._conn.commit()
            logger.info(
                "Artist '%s' (ID: %s) and associated albums/tracks are present "
                "in the DB.",
                artist.name,
                artist_id,
            )

        except aiosqlite.Error as e:
            if self._conn:
                with suppress(Exception):
                    await self._conn.rollback()
            raise LyricallyDatabaseError(
                f"Database error inserting artist '{artist.name}'"
            ) from e
        except Exception as e:
            if self._conn:
                with suppress(Exception):
                    await self._conn.rollback()
            raise LyricallyDatabaseError(
                f"Unexpected error inserting artist '{artist.name}'"
            ) from e
        finally:
            if cursor:
                await cursor.close()

    async def _insert_artist_record(
        self, cursor: aiosqlite.Cursor, artist: Artist
    ) -> int:
        """Insert artist record and return the artist ID.

        Args:
            cursor: The database cursor for transaction.
            artist: The artist to insert.

        Returns:
            The database ID of the inserted artist.

        Raises:
            LyricallyDatabaseError: If artist insertion fails.

        """
        await cursor.execute(
            "INSERT OR IGNORE INTO artists (name, url) VALUES (?, ?)",
            (artist.name, artist.url),
        )

        if cursor.rowcount > 0:
            if cursor.lastrowid is None:
                raise LyricallyDatabaseError(
                    f"Artist insertion failed. No lastrowid for '{artist.name}'"
                )
            return int(cursor.lastrowid)
        else:
            await cursor.execute(
                "SELECT id FROM artists WHERE name = ?", (artist.name,)
            )
            result = await cursor.fetchone()
            if not result or result[0] is None:
                raise LyricallyDatabaseError(
                    f"Artist insertion failed. Could not retrieve ID for "
                    f"'{artist.name}'"
                )
            return int(result[0])

    async def _insert_artist_albums(
        self, cursor: aiosqlite.Cursor, artist_id: int, albums: list[Album]
    ) -> None:
        """Insert all albums for an artist.

        Args:
            cursor: The database cursor for transaction.
            artist_id: The ID of the artist.
            albums: List of albums to insert.

        """
        if albums:
            logger.debug(
                "Artist ID %s has %d albums to insert.", artist_id, len(albums)
            )
            for album in albums:
                await self._insert_album(cursor, artist_id, album)
        else:
            logger.debug("No albums associated with artist ID %s.", artist_id)

    async def _insert_album(
        self, cursor: aiosqlite.Cursor, artist_id: int, album: Album
    ) -> None:
        """Insert an album into the database.

        Args:
            cursor: The database cursor for transaction.
            artist_id: The ID of the artist to attach this album to.
            album: The Album object that will be stored.

        Raises:
            LyricallyDatabaseError: If database insertion fails.

        """
        logger.debug(
            "Attempting to insert album '%s' for artist ID %d.", album.title, artist_id
        )
        try:
            if cursor.rowcount > 0:
                if cursor.lastrowid is None:
                    raise LyricallyDatabaseError(
                        f"Album insertion failed. No lastrowid for '{album.title}'"
                    )
                album_id = int(cursor.lastrowid)
            else:
                await cursor.execute(
                    "SELECT id FROM albums WHERE artist_id = ? AND title = ?",
                    (artist_id, album.title),
                )
                result = await cursor.fetchone()
                if not result or result[0] is None:
                    raise LyricallyDatabaseError(
                        f"Album insertion failed. Could not retrieve ID for "
                        f"'{album.title}'"
                    )
                album_id = int(result[0])

            logger.debug(
                "Album '%s' (ID: %s) is present in the DB. Inserting associated "
                "tracks.",
                album.title,
                album_id,
            )

            # Insert album's associated tracks
            if album.tracks:
                for track in album.tracks:
                    await self._insert_track(cursor, album_id, track)
            else:
                logger.debug("No tracks associated with album '%s'.", album.title)

        except aiosqlite.Error as e:
            raise LyricallyDatabaseError(
                f"Database error inserting album '{album.title}'"
            ) from e
        except Exception as e:
            raise LyricallyDatabaseError(
                f"Unexpected error inserting album '{album.title}'"
            ) from e

    async def _insert_track(
        self, cursor: aiosqlite.Cursor, album_id: int, track: Track
    ) -> None:
        """Insert a track into the database.

        Args:
            cursor: The database cursor for transaction.
            album_id: The ID of the album to attach this track to.
            track: The Track object that will be stored.

        Raises:
            LyricallyDatabaseError: If database insertion fails.

        """
        logger.debug(
            "Attempting to insert track '%s' for album ID %d.", track.title, album_id
        )
        try:
            await cursor.execute(
                "INSERT OR IGNORE INTO tracks (album_id, title, url, lyrics) "
                "VALUES (?, ?, ?, ?)",
                (album_id, track.title, track.url, track.lyrics),
            )

            if cursor.rowcount > 0:
                track_id = cursor.lastrowid
                logger.debug(
                    "Track '%s' (ID: %s) inserted into the DB.", track.title, track_id
                )
            else:
                await cursor.execute(
                    "SELECT id FROM tracks WHERE url = ?", (track.url,)
                )
                result = await cursor.fetchone()
                if result:
                    track_id = result[0]
                    logger.debug(
                        "Track '%s' (ID: %s) already exists in the DB.",
                        track.title,
                        track_id,
                    )
                else:
                    raise LyricallyDatabaseError(
                        f"Track insertion failed. Could not retrieve ID for "
                        f"'{track.title}'"
                    )

        except aiosqlite.Error as e:
            raise LyricallyDatabaseError(
                f"Database error inserting track '{track.title}'"
            ) from e
        except Exception as e:
            raise LyricallyDatabaseError(
                f"Unexpected error inserting track '{track.title}'"
            ) from e
