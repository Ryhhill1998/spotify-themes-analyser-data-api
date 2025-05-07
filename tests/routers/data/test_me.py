from unittest.mock import MagicMock

import pytest

from api.models.models import SpotifyProfile, SpotifyImage
from api.services.insights_service import InsightsServiceException
from api.services.spotify.spotify_data_service import SpotifyDataServiceException, \
    SpotifyDataServiceUnauthorisedException

# -------------------- GET PROFILE -------------------- #
# 1. Test /data/me/profile returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/profile returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/profile returns 500 error if general exception occurs.
# 4. Test /data/me/profile returns 422 error if request sends no POST body.
# 5. Test /data/me/profile returns 422 error if request missing access token.
# 6. Test /data/me/profile returns 500 error if response data type invalid.
# 7. Test /data/me/profile returns expected response.

# -------------------- GET TOP ARTISTS -------------------- #
# 1. Test /data/me/top/artists returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/artists returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/artists returns 500 error if general exception occurs.
# 4. Test /data/me/top/artists returns 422 error if request sends no POST body.
# 5. Test /data/me/top/artists returns 422 error if request missing access token.
# 6. Test /data/me/top/artists returns 422 error if request missing time range.
# 7. Test /data/me/top/artists returns 422 error if request invalid time range.
# 8. Test /data/me/top/artists returns 422 error if request missing limit.
# 9. Test /data/me/top/artists returns 422 error if request invalid limit.
# 10. Test /data/me/top/artists returns 500 error if response data type invalid.
# 11. Test /data/me/top/artists returns expected response.

# -------------------- GET TOP TRACKS -------------------- #
# 1. Test /data/me/top/tracks returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/tracks returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/tracks returns 500 error if general exception occurs.
# 4. Test /data/me/top/tracks returns 422 error if request sends no POST body.
# 5. Test /data/me/top/tracks returns 422 error if request missing access token.
# 6. Test /data/me/top/tracks returns 422 error if request missing time range.
# 7. Test /data/me/top/tracks returns 422 error if request invalid time range.
# 8. Test /data/me/top/tracks returns 422 error if request missing limit.
# 9. Test /data/me/top/tracks returns 422 error if request invalid limit.
# 10. Test /data/me/top/tracks returns 500 error if response data type invalid.
# 11. Test /data/me/top/tracks returns expected response.

# -------------------- GET TOP GENRES -------------------- #
# 1. Test /data/me/top/genres returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/genres returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/genres returns 500 error if general exception occurs.
# 4. Test /data/me/top/genres returns 422 error if request sends no POST body.
# 5. Test /data/me/top/genres returns 422 error if request missing access token.
# 6. Test /data/me/top/genres returns 422 error if request missing time range.
# 7. Test /data/me/top/genres returns 422 error if request invalid time range.
# 8. Test /data/me/top/genres returns 422 error if request missing limit.
# 9. Test /data/me/top/genres returns 422 error if request invalid limit.
# 10. Test /data/me/top/genres returns 500 error if response data type invalid.
# 11. Test /data/me/top/genres returns expected response.

# -------------------- GET TOP EMOTIONS -------------------- #
# 1. Test /data/me/top/emotions returns 500 error if SpotifyDataServiceException occurs.
# 2. Test /data/me/top/emotions returns 500 error if general exception occurs.
# 3. Test /data/me/top/emotions returns 422 error if request sends no POST body.
# 4. Test /data/me/top/emotions returns 422 error if request missing access token.
# 5. Test /data/me/top/emotions returns 422 error if request missing time range.
# 6. Test /data/me/top/emotions returns 422 error if request invalid time range.
# 7. Test /data/me/top/emotions returns 422 error if request missing limit.
# 8. Test /data/me/top/emotions returns 422 error if request invalid limit.
# 9. Test /data/me/top/emotions returns 500 error if response data type invalid.
# 10. Test /data/me/top/emotions returns expected response.

BASE_URL = "/data/me"

# -------------------- GET USER PROFILE -------------------- #
PROFILE_URL = f"{BASE_URL}/profile"


# 1. Test /data/me/profile returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
def test_get_user_profile_returns_401_error_if_spotify_data_service_unauthorised_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_user_profile.side_effect = SpotifyDataServiceUnauthorisedException("Test")

    res = client.post(url=PROFILE_URL, json=mock_access_token_request)

    assert res.status_code == 401 and res.json() == {"detail": "Invalid access token"}

# 2. Test /data/me/profile returns 500 error if SpotifyDataServiceException occurs.
def test_get_user_profile_returns_500_error_if_spotify_data_service_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_user_profile.side_effect = SpotifyDataServiceException("Test")

    res = client.post(url=PROFILE_URL, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Failed to retrieve the user's profile"}


# 3. Test /data/me/profile returns 500 error if general exception occurs.
def test_get_user_profile_returns_500_error_if_general_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_user_profile.side_effect = Exception("Test")

    res = client.post(url=PROFILE_URL, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 4. Test /data/me/profile returns 422 error if request sends no POST body.
def test_get_user_profile_returns_422_error_if_request_sends_no_post_body(client):
    res = client.post(url=PROFILE_URL)

    assert res.status_code == 422


# 5. Test /data/me/profile returns 422 error if request missing access token.
def test_get_user_profile_returns_422_error_if_request_missing_access_token(client):
    res = client.post(url=PROFILE_URL, json={"refresh_token": "refresh"})

    assert res.status_code == 422


# 6. Test /data/me/profile returns 500 error if response data type invalid.
def test_get_user_profile_returns_500_error_if_response_data_type_invalid(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_user_profile.return_value = {}

    res = client.post(url=PROFILE_URL, json=mock_access_token_request)

    assert res.status_code == 500



# 7. Test /data/me/profile returns expected response.
def test_get_user_profile_returns_expected_response(client, mock_spotify_data_service, mock_access_token_request):
    mock_spotify_data_service.get_user_profile.return_value = SpotifyProfile(
        id="1",
        display_name="display_name",
        email="email",
        href="href",
        images=[SpotifyImage(height=100, width=100, url="image_url")],
        followers=10
    )

    res = client.post(url=PROFILE_URL, json=mock_access_token_request)

    expected_json = {
        "id": "1",
        "display_name": "display_name",
        "email": "email",
        "href": "href",
        "images": [{"height": 100, "width": 100, "url": "image_url"}],
        "followers": 10
    }
    assert res.status_code == 200 and res.json() == expected_json


# -------------------- GET TOP ARTISTS -------------------- #
# 1. Test /data/me/top/artists returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/artists returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/artists returns 500 error if general exception occurs.
# 4. Test /data/me/top/artists returns 422 error if request sends no POST body.
# 5. Test /data/me/top/artists returns 422 error if request missing access token.
# 6. Test /data/me/top/artists returns 422 error if request missing time range.
# 7. Test /data/me/top/artists returns 422 error if request invalid time range.
# 8. Test /data/me/top/artists returns 422 error if request missing limit.
# 9. Test /data/me/top/artists returns 422 error if request invalid limit.
# 10. Test /data/me/top/artists returns 500 error if response data type invalid.
# 11. Test /data/me/top/artists returns expected response.

# -------------------- GET TOP TRACKS -------------------- #
# 1. Test /data/me/top/tracks returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/tracks returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/tracks returns 500 error if general exception occurs.
# 4. Test /data/me/top/tracks returns 422 error if request sends no POST body.
# 5. Test /data/me/top/tracks returns 422 error if request missing access token.
# 6. Test /data/me/top/tracks returns 422 error if request missing time range.
# 7. Test /data/me/top/tracks returns 422 error if request invalid time range.
# 8. Test /data/me/top/tracks returns 422 error if request missing limit.
# 9. Test /data/me/top/tracks returns 422 error if request invalid limit.
# 10. Test /data/me/top/tracks returns 500 error if response data type invalid.
# 11. Test /data/me/top/tracks returns expected response.

# -------------------- GET TOP GENRES -------------------- #
# 1. Test /data/me/top/genres returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/genres returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/genres returns 500 error if general exception occurs.
# 4. Test /data/me/top/genres returns 422 error if request sends no POST body.
# 5. Test /data/me/top/genres returns 422 error if request missing access token.
# 6. Test /data/me/top/genres returns 422 error if request missing time range.
# 7. Test /data/me/top/genres returns 422 error if request invalid time range.
# 8. Test /data/me/top/genres returns 422 error if request missing limit.
# 9. Test /data/me/top/genres returns 422 error if request invalid limit.
# 10. Test /data/me/top/genres returns 500 error if response data type invalid.
# 11. Test /data/me/top/genres returns expected response.

# -------------------- GET TOP EMOTIONS -------------------- #
# 1. Test /data/me/top/emotions returns 500 error if SpotifyDataServiceException occurs.
# 2. Test /data/me/top/emotions returns 500 error if general exception occurs.
# 3. Test /data/me/top/emotions returns 422 error if request sends no POST body.
# 4. Test /data/me/top/emotions returns 422 error if request missing access token.
# 5. Test /data/me/top/emotions returns 422 error if request missing time range.
# 6. Test /data/me/top/emotions returns 422 error if request invalid time range.
# 7. Test /data/me/top/emotions returns 422 error if request missing limit.
# 8. Test /data/me/top/emotions returns 422 error if request invalid limit.
# 9. Test /data/me/top/emotions returns 500 error if response data type invalid.
# 10. Test /data/me/top/emotions returns expected response.