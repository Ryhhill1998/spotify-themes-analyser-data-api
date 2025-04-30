from enum import Enum


class TimeRange(str, Enum):
    SHORT = "short_term"
    MEDIUM = "medium_term"
    LONG = "long_term"
