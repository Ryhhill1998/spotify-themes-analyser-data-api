from enum import Enum


class SpotifyItemType(str, Enum):
    ARTIST = "artist"
    TRACK = "track"


class TimeRange(str, Enum):
    SHORT = "short_term"
    MEDIUM = "medium_term"
    LONG = "long_term"
