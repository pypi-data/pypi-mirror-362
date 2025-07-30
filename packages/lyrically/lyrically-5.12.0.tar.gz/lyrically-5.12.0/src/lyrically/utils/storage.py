"""Storage utilities for determining and creating database file paths."""

import logging
from pathlib import Path

import platformdirs

from .errors import LyricallyError

logger = logging.getLogger(__name__)


def _create_db_path(storage_dir: str | Path | None = None) -> Path:
    """Determine and create the full path for the database file.

    If a storage directory is provided, it will be used. Otherwise, a
    default directory is created in the user's standard data location.

    Args:
        storage_dir: An optional path to a directory for storing the database.

    Returns:
        The complete Path object for the database file.

    Raises:
        LyricallyError: If the storage directory cannot be created due to
            permission errors or other OS-level issues.

    """
    try:
        if storage_dir:
            storage_dir_path = Path(storage_dir)
            logger.debug("Using provided storage directory: %s", storage_dir_path)
        else:
            storage_dir_path = Path(platformdirs.user_data_dir("lyrically"))
            logger.debug(
                "No storage directory provided, using default: %s", storage_dir_path
            )

        # Ensure the directory exists
        storage_dir_path.mkdir(parents=True, exist_ok=True)

        db_path = storage_dir_path / "lyrically.db"
        logger.debug("Database path set to: %s", db_path)
        return db_path

    except (OSError, PermissionError) as e:
        raise LyricallyError(
            f"Failed to create or access storage directory: {e}"
        ) from e
