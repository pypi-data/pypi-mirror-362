"""Data models for tracks, albums, and artists in lyrically."""

from dataclasses import dataclass, field


@dataclass
class Track:
    """Represents a music track with title, URL, and optional lyrics."""

    title: str
    url: str
    lyrics: str | None = None


@dataclass
class Album:
    """Represents a music album containing multiple tracks."""

    title: str
    tracks: list[Track] = field(default_factory=list)


@dataclass
class Artist:
    """Represents a music artist with their discography."""

    name: str
    url: str
    albums: list[Album] = field(default_factory=list)
