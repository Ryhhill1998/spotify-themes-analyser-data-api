from unittest.mock import MagicMock

import pytest

from api.models.models import LyricsResponse
from api.services.analysis_service import AnalysisService
from api.services.insights_service import InsightsService
from api.services.lyrics_service import LyricsService


@pytest.fixture
def mock_lyrics_service() -> MagicMock:
    return MagicMock(spec=LyricsService)


@pytest.fixture
def mock_analysis_service() -> MagicMock:
    return MagicMock(spec=AnalysisService)


@pytest.fixture
def insights_service(mock_spotify_data_service, mock_lyrics_service, mock_analysis_service) -> InsightsService:
    return InsightsService(
        spotify_data_service=mock_spotify_data_service,
        lyrics_service=mock_lyrics_service,
        analysis_service=mock_analysis_service
    )


@pytest.fixture
def mock_lyrics_response_factory():
    def _create(track_id: str) -> LyricsResponse:
        return LyricsResponse(track_id=track_id, artist_name="artist_name", track_title="track_title", lyrics="lyrics")

    return _create
