from unittest.mock import AsyncMock

import pytest

from api.models.models import SpotifyTrack, SpotifyImage, SpotifyTrackArtist, LyricsResponse
from api.services.analysis_service import AnalysisService
from api.services.insights_service import InsightsService
from api.services.lyrics_service import LyricsService
from api.services.spotify.spotify_data_service import SpotifyDataService


@pytest.fixture
def mock_spotify_data_service() -> AsyncMock:
    return AsyncMock(spec=SpotifyDataService)


@pytest.fixture
def mock_lyrics_service() -> AsyncMock:
    return AsyncMock(spec=LyricsService)


@pytest.fixture
def mock_analysis_service() -> AsyncMock:
    return AsyncMock(spec=AnalysisService)


@pytest.fixture
def insights_service(mock_spotify_data_service, mock_lyrics_service, mock_analysis_service) -> InsightsService:
    return InsightsService(
        spotify_data_service=mock_spotify_data_service,
        lyrics_service=mock_lyrics_service,
        analysis_service=mock_analysis_service
    )


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
def mock_lyrics_response_factory():
    def _create(track_id: str) -> LyricsResponse:
        return LyricsResponse(track_id=track_id, artist_name="artist_name", track_title="track_title", lyrics="lyrics")

    return _create
