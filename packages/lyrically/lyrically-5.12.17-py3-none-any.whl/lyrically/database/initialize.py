"""Database schema initialization for lyrically (table creation, setup routines)."""

import logging

import aiosqlite

from ..utils.errors import LyricallyDataError

logger = logging.getLogger(__name__)


async def _initialize_database(conn: aiosqlite.Connection | None) -> None:
    """Create all necessary tables for the database.

    Args:
        conn: An active aiosqlite.Connection to the database.

    Raises:
        LyricallyDataError: If table creation fails.

    """
    if not conn:
        raise LyricallyDataError("Database connection is not available.")

    logger.debug("Executing schema creation queries.")
    try:
        # Artists table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                url TEXT UNIQUE NOT NULL
            )
            """
        )

        # Albums table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS albums (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                artist_id INTEGER NOT NULL,
                FOREIGN KEY (artist_id) REFERENCES artists (id)
                    ON DELETE CASCADE,
                UNIQUE (artist_id, title)
            )
            """
        )

        # Tracks table
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                lyrics TEXT,
                album_id INTEGER NOT NULL,
                FOREIGN KEY (album_id) REFERENCES albums (id)
                    ON DELETE CASCADE,
                UNIQUE (album_id, title)
            )
            """
        )

        await conn.commit()
        logger.info("Database schema verified and up to date.")

    except aiosqlite.Error as e:
        raise LyricallyDataError("Failed to initialize database schema") from e
