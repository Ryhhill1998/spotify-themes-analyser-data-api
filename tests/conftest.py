from unittest.mock import MagicMock

import pytest

from api.models.models import SpotifyTrack, SpotifyImage, SpotifyTrackArtist
from api.services.spotify.spotify_data_service import SpotifyDataService


@pytest.fixture
def mock_spotify_data_service() -> MagicMock:
    return MagicMock(spec=SpotifyDataService)


@pytest.fixture
def mock_spotify_track_factory():
    def _create(track_id: str = "1", artist_id: str = "1") -> SpotifyTrack:
        return SpotifyTrack(
            id=track_id,
            name="track_name",
            images=[SpotifyImage(height=100, width=100, url="image_url")],
            spotify_url="spotify_url",
            artist=SpotifyTrackArtist(id=artist_id, name="artist_name"),
            release_date="release_date",
            album_name="album_name",
            explicit=False,
            duration_ms=180000,
            popularity=50
        )

    return _create


@pytest.fixture
def mock_spotify_tracks(mock_spotify_track_factory) -> list[SpotifyTrack]:
    return [mock_spotify_track_factory(track_id=str(i), artist_id=str(i)) for i in range(1, 6)]
