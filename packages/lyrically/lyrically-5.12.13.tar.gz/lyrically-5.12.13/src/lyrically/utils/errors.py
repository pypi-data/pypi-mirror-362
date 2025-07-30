"""Custom exception classes for lyrically package errors."""


class LyricallyError(Exception):
    """Base exception for all lyrically-related errors."""


class LyricallyParseError(LyricallyError):
    """Raised when HTML parsing fails or expected elements are not found."""


class LyricallyDatabaseError(LyricallyError):
    """Base exception for database-related errors."""


class LyricallyConnectionError(LyricallyDatabaseError):
    """Raised when a database connection fails."""


class LyricallyDataError(LyricallyDatabaseError):
    """Raised when a database query or data operation fails."""


class LyricallyRequestError(LyricallyError):
    """Raised for errors related to HTTP requests."""
