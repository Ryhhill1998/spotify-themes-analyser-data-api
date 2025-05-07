from unittest.mock import MagicMock, AsyncMock
import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_spotify_auth_service
from api.main import app
from api.models.models import TokenData
from api.services.spotify.spotify_auth_service import SpotifyAuthService, SpotifyAuthServiceException


# 1. Test /auth/tokens/refresh returns 401 error if SpotifyAuthServiceException occurs.
# 2. Test /auth/tokens/refresh returns 500 error if any other exception occurs.
# 3. Test /auth/tokens/refresh returns 422 error if request data type invalid.
# 4. Test /auth/tokens/refresh returns 500 error if response data type invalid.
# 5. Test /auth/tokens/refresh returns expected data.


@pytest.fixture
def mock_spotify_auth_service() -> MagicMock:
    return MagicMock(spec=SpotifyAuthService)


@pytest.fixture
def mock_refresh_request() -> dict[str, str]:
    return {"refresh_token" : "refresh"}


@pytest.fixture
def client(mock_spotify_auth_service):
    app.dependency_overrides[get_spotify_auth_service] = lambda: mock_spotify_auth_service

    yield TestClient(app, follow_redirects=False, raise_server_exceptions=False)

    app.dependency_overrides = {}


# 1. Test /auth/tokens/refresh returns 401 error if SpotifyAuthServiceException occurs.
def test_refresh_tokens_returns_401_error_if_spotify_auth_service_exception_occurs(
        client,
        mock_spotify_auth_service,
        mock_refresh_request
):
    mock_refresh_tokens = AsyncMock()
    mock_refresh_tokens.side_effect = SpotifyAuthServiceException("Test")
    mock_spotify_auth_service.refresh_tokens = mock_refresh_tokens

    res = client.post(url="/auth/tokens/refresh", json=mock_refresh_request)

    assert res.status_code == 401 and res.json() == {"detail" : "Invalid refresh token."}


# 2. Test /auth/tokens/refresh returns 500 error if any other exception occurs.
def test_refresh_tokens_returns_500_error_if_other_exception_occurs(
        client,
        mock_spotify_auth_service,
        mock_refresh_request
):
    mock_refresh_tokens = AsyncMock()
    mock_refresh_tokens.side_effect = Exception("Test")
    mock_spotify_auth_service.refresh_tokens = mock_refresh_tokens

    res = client.post(url="/auth/tokens/refresh", json=mock_refresh_request)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 3. Test /auth/tokens/refresh returns 422 error if request data type invalid.
def test_refresh_tokens_returns_422_error_if_request_data_type_invalid(
        client,
        mock_spotify_auth_service,
        mock_refresh_request
):
    res = client.post(url="/auth/tokens/refresh", json="invalid")

    assert res.status_code == 422


# 4. Test /auth/tokens/refresh returns 500 error if response data type invalid.
def test_refresh_tokens_returns_500_error_if_response_data_type_invalid(
        client,
        mock_spotify_auth_service,
        mock_refresh_request
):
    mock_refresh_tokens = AsyncMock()
    mock_refresh_tokens.return_value = {}
    mock_spotify_auth_service.refresh_tokens = mock_refresh_tokens

    res = client.post(url="/auth/tokens/refresh", json=mock_refresh_request)

    assert res.status_code == 500


# 4. Test /auth/tokens/refresh returns expected data.
def test_refresh_tokens_returns_expected_data(client, mock_spotify_auth_service, mock_refresh_request):
    mock_refresh_tokens = AsyncMock()
    mock_refresh_tokens.return_value = TokenData(access_token="access", refresh_token="refresh")
    mock_spotify_auth_service.refresh_tokens = mock_refresh_tokens

    res = client.post(url="/auth/tokens/refresh", json=mock_refresh_request)

    assert res.status_code == 200 and res.json() == {"access_token": "access", "refresh_token": "refresh"}
