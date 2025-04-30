import pytest

from api.services.endpoint_requester import EndpointRequesterException
from api.services.spotify.spotify_auth_service import SpotifyAuthService, SpotifyAuthServiceException

TEST_URL = "http://test-url.com"
TEST_CLIENT_ID = "client_id"
TEST_CLIENT_SECRET = "client_secret"

# 1. Test that auth_header generates the authorisation header correctly.
# 2. Test that refresh_tokens raises SpotifyAuthServiceException if Spotify API request fails.
# 3. Test that refresh_tokens raises SpotifyAuthServiceException if access_token not returned by Spotify.
# 4. Test that refresh_tokens returns expected TokenData.
# 5. Test that refresh_tokens only updates refresh_token if new one returned by Spotify.
# 6. Test that refresh_tokens keeps refresh_token if new one not returned by Spotify.

@pytest.fixture
def spotify_auth_service(mock_endpoint_requester) -> SpotifyAuthService:
    return SpotifyAuthService(
        client_id=TEST_CLIENT_ID,
        client_secret=TEST_CLIENT_SECRET,
        base_url=TEST_URL,
        endpoint_requester=mock_endpoint_requester
    )


@pytest.fixture
def mock_request_tokens_response() -> dict[str, str]:
    return {"access_token": "new_access", "refresh_token": "new_refresh"}


def test_auth_header(spotify_auth_service):
    auth_header = spotify_auth_service._auth_header
    expected_auth_header = "Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="

    assert auth_header == expected_auth_header


@pytest.mark.asyncio
async def test_refresh_tokens_request_failure(spotify_auth_service, mock_endpoint_requester):
    mock_endpoint_requester.post.side_effect = EndpointRequesterException()

    with pytest.raises(SpotifyAuthServiceException, match="Spotify API token request failed"):
        await spotify_auth_service.refresh_tokens("refresh")


@pytest.mark.asyncio
async def test_refresh_tokens_invalid_response_data(spotify_auth_service, mock_endpoint_requester):
    mock_endpoint_requester.post.return_value = {"refresh_token": "refresh"}

    with pytest.raises(SpotifyAuthServiceException, match="No access token returned"):
        await spotify_auth_service.refresh_tokens("refresh")


@pytest.mark.asyncio
async def test_refresh_tokens_success(spotify_auth_service, mock_endpoint_requester, mock_request_tokens_response):
    mock_endpoint_requester.post.return_value = mock_request_tokens_response

    tokens = await spotify_auth_service.refresh_tokens("refresh")

    assert tokens.access_token == "new_access" and tokens.refresh_token == "new_refresh"


@pytest.mark.asyncio
async def test_refresh_tokens_new_refresh_token_returned(
        spotify_auth_service,
        mock_endpoint_requester,
        mock_request_tokens_response
):
    mock_endpoint_requester.post.return_value = mock_request_tokens_response

    tokens = await spotify_auth_service.refresh_tokens("old_refresh")

    assert tokens.access_token == "new_access" and tokens.refresh_token == "new_refresh"


@pytest.mark.asyncio
async def test_refresh_tokens_no_new_refresh_token_returned(
        spotify_auth_service,
        mock_endpoint_requester,
        mock_request_tokens_response
):
    old_refresh_token = "old_refresh"
    mock_endpoint_requester.post.return_value = mock_request_tokens_response
    mock_request_tokens_response.pop("refresh_token")

    tokens = await spotify_auth_service.refresh_tokens(old_refresh_token)

    assert (
            tokens.access_token == "new_access" and
            tokens.refresh_token != "new_refresh" and
            tokens.refresh_token == old_refresh_token
    )
