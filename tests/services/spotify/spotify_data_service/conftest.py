import pytest

from api.services.spotify.spotify_data_service import SpotifyDataService

TEST_URL = "http://test-url.com"
TEST_CLIENT_ID = "client_id"
TEST_CLIENT_SECRET = "client_secret"
TEST_REDIRECT_URI = "http://redirect-test-url.com"


@pytest.fixture
def spotify_data_service(mock_endpoint_requester) -> SpotifyDataService:
    return SpotifyDataService(
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET,
        base_url=TEST_URL,
        endpoint_requester=mock_endpoint_requester
    )


@pytest.fixture
def mock_track_data() -> dict:
    return {
        "id": "1",
        "name": "track_name",
        "album": {
            "name": "album_name",
            "images": [{"height": 100, "width": 100, "url": "album_image_url"}],
            "release_date": "album_release_date"
        },
        "artists": [{"id": "1", "name": "artist_name"}],
        "external_urls": {"spotify": "spotify_url"},
        "explicit": True,
        "duration_ms": 180000,
        "popularity": 50
    }


@pytest.fixture
def mock_artist_data() -> dict:
    return {
        "id": "1",
        "name": "artist_name",
        "images": [{"height": 100, "width": 100, "url": "image_url"}],
        "external_urls": {"spotify": "spotify_url"},
        "followers": {"total": 100},
        "genres": ["genre1", "genre2", "genre3"],
        "popularity": 50
    }
