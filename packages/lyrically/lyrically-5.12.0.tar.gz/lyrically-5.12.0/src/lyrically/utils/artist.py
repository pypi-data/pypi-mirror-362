"""Artist utilities for URL creation, parsing, and discography extraction."""

import re
import unicodedata
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from ..config import BASE_URL
from ..utils.errors import LyricallyError, LyricallyParseError
from .models import Album, Artist, Track


def _create_artist_url(artist: str, base_url: str) -> str:
    """Create a standardized URL for an artist based on their name.

    Args:
        artist: The name of the music artist.
        base_url: The base URL of the website.

    Returns:
        The full URL to the artist's page.

    Raises:
        LyricallyError: If the artist's name is empty or results in an
            invalid format after cleaning.

    """
    if not artist or not artist.strip():
        raise LyricallyError("Artist name cannot be empty.")

    try:
        # Normalize to remove accents and special characters
        normalized = unicodedata.normalize("NFKD", artist)
        ascii_name = normalized.encode("ASCII", "ignore").decode("utf-8")
    except Exception as e:
        raise LyricallyError(f"Failed to normalize artist name: {artist}") from e

    # Perform common substitutions and clean the name
    substituted_name = ascii_name.replace("!", "i").replace("$", "s")
    cleaned = re.sub(r"[^a-z0-9]", "", substituted_name.lower())

    if not cleaned:
        raise LyricallyError(
            f"Cleaning artist name '{artist}' resulted in an empty string."
        )

    # Determine the URL prefix based on the first character
    first_char = cleaned[0]
    prefix = "19" if first_char.isdigit() else first_char

    # Construct the final URL
    full_path = f"/{prefix}/{cleaned}.html"
    artist_url = urljoin(base_url, full_path)

    return artist_url


def _create_artist_object(artist_page_html: BeautifulSoup, url: str) -> Artist:
    """Create an artist object from the HTML page.

    Args:
        artist_page_html: The soup object representing the artist's discography
            page.
        url: A string containing the URL to the artist's discography page.

    Returns:
        An Artist object with the official name and URL.

    Raises:
        LyricallyParseError: If the title tag cannot be found or parsed.

    """
    title_tag = artist_page_html.find("title")
    if title_tag is None:
        msg = f"Could not find title tag on page {url} to extract artist name."
        raise LyricallyParseError(msg)
    title_text = title_tag.get_text()
    official_artist_name = title_text.split(" Lyrics")[0]
    return Artist(official_artist_name, url)


def _extract_album_title(element: Tag) -> str | None:
    """Extract album title from an album element.

    Args:
        element: BeautifulSoup element containing album information.

    Returns:
        Cleaned album title or None if not found.

    """
    album_title_tag = element.find("b")
    if album_title_tag is None:
        return None
    album_title_raw = album_title_tag.get_text()
    if not isinstance(album_title_raw, str):
        return None
    album_title = album_title_raw.strip()
    if album_title.startswith('"') and album_title.endswith('"'):
        album_title = album_title[1:-1]
    return album_title


def _create_track_from_element(element: Tag) -> Track:
    """Create a Track object from a track element.

    Args:
        element: BeautifulSoup element containing track information.

    Returns:
        Track object with title and URL.

    Raises:
        LyricallyParseError: If track attributes cannot be found.

    """
    raw_track_attrs = element.find("a")
    if not isinstance(raw_track_attrs, Tag):
        raise LyricallyParseError("Could not find track attributes in element.")
    track_title = raw_track_attrs.get_text()
    href = raw_track_attrs.get("href")
    if not isinstance(href, str):
        raise LyricallyParseError("Track element missing href attribute.")
    track_url = urljoin(BASE_URL, href)
    return Track(track_title, track_url)


def _create_album_track_objects(
    artist_page_html: BeautifulSoup, url: str
) -> list[Album]:
    """Create Album and Track objects from the artist's discography page.

    Args:
        artist_page_html: The soup object representing the artist's discography page.
        url: A string containing the URL to the artist's discography page.

    Returns:
        A list of Album objects containing their respective tracks.

    Raises:
        LyricallyParseError: If the listAlbum div cannot be found or if track
            attributes are missing.

    """
    music_containers = artist_page_html.find("div", {"id": "listAlbum"})
    if not isinstance(music_containers, Tag):
        raise LyricallyParseError(f"listAlbum div is not a valid container for {url}.")
    music_container_divs = music_containers.find_all("div")
    albums = []
    current_album = None

    for element in music_container_divs:
        if not isinstance(element, Tag):
            continue
        if not element.has_attr("class"):
            continue
        classes = element["class"]
        if not isinstance(classes, list):
            continue
        if "album" in classes:
            # Save current album if it has tracks
            if current_album and current_album.tracks:
                albums.append(current_album)
            # Create new album
            album_title = _extract_album_title(element)
            current_album = Album(album_title) if album_title else None
        elif "listalbum-item" in classes and current_album:
            track = _create_track_from_element(element)
            current_album.tracks.append(track)

    # Add the last album if it has tracks
    if current_album and current_album.tracks:
        albums.append(current_album)

    return albums


def _create_music_objects(artist_page_html: BeautifulSoup, url: str) -> Artist:
    """Create a complete Artist object with albums and tracks from HTML.

    Args:
        artist_page_html: The soup object representing the artist's discography
            page.
        url: A string containing the URL to the artist's discography page.

    Returns:
        A complete Artist object populated with albums and tracks.

    Raises:
        LyricallyParseError: If any part of the HTML parsing fails.

    """
    artist = _create_artist_object(artist_page_html, url)
    albums = _create_album_track_objects(artist_page_html, url)

    for album in albums:
        artist.albums.append(album)

    return artist
