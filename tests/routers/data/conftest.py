from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

from api.dependencies import get_spotify_data_service, get_insights_service
from api.main import app
from api.models.models import SpotifyArtist, SpotifyImage
from api.services.insights_service import InsightsService


@pytest.fixture
def mock_access_token_request() -> dict[str, str]:
    return {"access_token": "access"}


@pytest.fixture
def mock_spotify_artist_factory():
    def _create(artist_id: str = "1") -> SpotifyArtist:
        return SpotifyArtist(
            id=artist_id,
            name="artist_name",
            images=[SpotifyImage(height=100, width=100, url="image_url")],
            spotify_url="spotify_url",
            genres=["genre1", "genre2", "genre3"],
            followers=100,
            popularity=50
        )

    return _create


@pytest.fixture
def mock_spotify_artists(mock_spotify_artist_factory) -> list[SpotifyArtist]:
    return [mock_spotify_artist_factory(str(i)) for i in range(1, 6)]


@pytest.fixture
def mock_insights_service() -> MagicMock:
    return MagicMock(spec=InsightsService)


@pytest.fixture
def client(mock_spotify_data_service, mock_insights_service):
    app.dependency_overrides[get_spotify_data_service] = lambda: mock_spotify_data_service
    app.dependency_overrides[get_insights_service] = lambda: mock_insights_service

    yield TestClient(app, follow_redirects=False, raise_server_exceptions=False)

    app.dependency_overrides = {}
