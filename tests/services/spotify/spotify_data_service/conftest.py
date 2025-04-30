import pytest

from api.services.spotify.spotify_data_service import SpotifyDataService

TEST_URL = "http://test-url.com"
TEST_CLIENT_ID = "client_id"
TEST_CLIENT_SECRET = "client_secret"
TEST_REDIRECT_URI = "http://redirect-test-url.com"
TEST_SCOPE = "user-top-read"


@pytest.fixture
def spotify_data_service(mock_endpoint_requester) -> SpotifyDataService:
    return SpotifyDataService(
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET,
        base_url=TEST_URL,
        endpoint_requester=mock_endpoint_requester
    )
