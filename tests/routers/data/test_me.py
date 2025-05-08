from unittest.mock import AsyncMock

import pytest

from api.models.models import SpotifyProfile, SpotifyImage, TopGenre, TopEmotion, EmotionPercentage
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
# 7. Test /data/me/profile calls get_user_profile with expected params.
# 8. Test /data/me/profile returns expected response.

# -------------------- GET TOP ARTISTS -------------------- #
# 1. Test /data/me/top/artists returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/artists returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/artists returns 500 error if general exception occurs.
# 4. Test /data/me/top/artists returns 422 error if request sends no POST body.
# 5. Test /data/me/top/artists returns 422 error if request missing access token.
# 6. Test /data/me/top/artists returns 422 error if request missing time range.
# 7. Test /data/me/top/artists returns 422 error if request time range invalid.
# 8. Test /data/me/top/artists returns 422 error if request limit invalid.
# 9. Test /data/me/top/artists returns 500 error if response data type invalid.
# 10. Test /data/me/top/artists calls get_top_artists with expected params.
# 11. Test /data/me/top/artists returns expected response.

# -------------------- GET TOP TRACKS -------------------- #
# 1. Test /data/me/top/tracks returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/tracks returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/tracks returns 500 error if general exception occurs.
# 4. Test /data/me/top/tracks returns 422 error if request sends no POST body.
# 5. Test /data/me/top/tracks returns 422 error if request missing access token.
# 6. Test /data/me/top/tracks returns 422 error if request missing time range.
# 7. Test /data/me/top/tracks returns 422 error if request time range invalid.
# 8. Test /data/me/top/tracks returns 422 error if request limit invalid.
# 9. Test /data/me/top/tracks returns 500 error if response data type invalid.
# 10. Test /data/me/top/tracks calls get_top_tracks with expected params.
# 11. Test /data/me/top/tracks returns expected response.

# -------------------- GET TOP GENRES -------------------- #
# 1. Test /data/me/top/genres returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/genres returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/genres returns 500 error if general exception occurs.
# 4. Test /data/me/top/genres returns 422 error if request sends no POST body.
# 5. Test /data/me/top/genres returns 422 error if request missing access token.
# 6. Test /data/me/top/genres returns 422 error if request missing time range.
# 7. Test /data/me/top/genres returns 422 error if request time range invalid.
# 8. Test /data/me/top/genres returns 500 error if response data type invalid.
# 9. Test /data/me/top/genres calls get_top_genres with expected params.
# 10. Test /data/me/top/genres returns expected response.

# -------------------- GET TOP EMOTIONS -------------------- #
# 1. Test /data/me/top/emotions returns 500 error if InsightsServiceException occurs.
# 2. Test /data/me/top/emotions returns 500 error if general exception occurs.
# 3. Test /data/me/top/emotions returns 422 error if request sends no POST body.
# 4. Test /data/me/top/emotions returns 422 error if request missing access token.
# 5. Test /data/me/top/emotions returns 422 error if request missing time range.
# 6. Test /data/me/top/emotions returns 422 error if request invalid time range.
# 7. Test /data/me/top/emotions returns 500 error if response data type invalid.
# 8. Test /data/me/top/emotions returns expected response.

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


# 7. Test /data/me/profile calls get_user_profile with expected params.


# 8. Test /data/me/profile returns expected response.
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
ARTISTS_URL = f"{BASE_URL}/top/artists"


@pytest.fixture
def top_artists_request_params() -> dict[str, str | int]:
    return {"time_range": "short_term", "limit": 10}


# 1. Test /data/me/top/artists returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
def test_get_top_artists_returns_401_error_if_spotify_data_service_unauthorised_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_artists_request_params
):
    mock_spotify_data_service.get_top_artists.side_effect = SpotifyDataServiceUnauthorisedException("Test")

    res = client.post(url=ARTISTS_URL, params=top_artists_request_params, json=mock_access_token_request)

    assert res.status_code == 401 and res.json() == {"detail": "Invalid access token"}


# 2. Test /data/me/top/artists returns 500 error if SpotifyDataServiceException occurs.
def test_get_top_artists_returns_500_error_if_spotify_data_service_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_artists_request_params
):
    mock_spotify_data_service.get_top_artists.side_effect = SpotifyDataServiceException("Test")

    res = client.post(url=ARTISTS_URL, params=top_artists_request_params, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Failed to retrieve the user's top artists"}


# 3. Test /data/me/top/artists returns 500 error if general exception occurs.
def test_get_top_artists_returns_500_error_if_general_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_artists_request_params
):
    mock_spotify_data_service.get_top_artists.side_effect = Exception("Test")

    res = client.post(url=ARTISTS_URL, params=top_artists_request_params, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 4. Test /data/me/top/artists returns 422 error if request sends no POST body.
def test_get_top_artists_returns_422_error_if_request_sends_no_post_body(client, top_artists_request_params):
    res = client.post(url=ARTISTS_URL, params=top_artists_request_params)

    assert res.status_code == 422


# 5. Test /data/me/top/artists returns 422 error if request missing access token.
def test_get_top_artists_returns_422_error_if_request_missing_access_token(client, top_artists_request_params):
    res = client.post(url=ARTISTS_URL, params=top_artists_request_params, json={"refresh_token": "refresh"})

    assert res.status_code == 422


# 6. Test /data/me/top/artists returns 422 error if request missing time range.
def test_get_top_artists_returns_422_error_if_request_missing_time_range(
        client,
        mock_access_token_request,
        top_artists_request_params
):
    top_artists_request_params.pop("time_range")

    res = client.post(url=ARTISTS_URL, params=top_artists_request_params, json=mock_access_token_request)

    assert res.status_code == 422


# 7. Test /data/me/top/genres returns 422 error if request time range invalid.
def test_get_top_artists_returns_422_error_if_request_time_range_invalid(
        client,
        mock_access_token_request,
        top_artists_request_params
):
    top_artists_request_params["time_range"] = "short"

    res = client.post(url=ARTISTS_URL, params=top_artists_request_params, json=mock_access_token_request)

    assert res.status_code == 422


# 8. Test /data/me/top/artists returns 422 error if request limit invalid.
@pytest.mark.parametrize("limit", [9, 0, -10, 51, 100])
def test_get_top_artists_returns_422_error_if_request_limit_invalid(
        client,
        mock_access_token_request,
        top_artists_request_params,
        limit
):
    top_artists_request_params["limit"] = limit

    res = client.post(url=ARTISTS_URL, params=top_artists_request_params, json=mock_access_token_request)

    assert res.status_code == 422


# 9. Test /data/me/top/artists returns 500 error if response data type invalid.
def test_get_top_artists_returns_500_error_if_response_data_type_invalid(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_artists_request_params
):
    mock_spotify_data_service.get_top_artists.return_value = {}

    res = client.post(url=ARTISTS_URL, params=top_artists_request_params, json=mock_access_token_request)

    assert res.status_code == 500


# 10. Test /data/me/top/artists calls get_top_artists with expected params.
@pytest.mark.parametrize(
    "time_range, limit, expected_limit",
    [
        ("short_term", None, 50),
        ("medium_term", None, 50),
        ("long_term", None, 50),
        ("short_term", 25, 25),
        ("medium_term", 25, 25),
        ("long_term", 25, 25)
    ]
)
def test_get_top_artists_calls_get_top_artists_with_expected_params(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_artists_request_params,
        time_range,
        limit,
        expected_limit
):
    mock_get_top_artists = AsyncMock()
    mock_spotify_data_service.get_top_artists = mock_get_top_artists
    top_artists_request_params["time_range"] = time_range
    if limit is None:
        top_artists_request_params.pop("limit")
    else:
        top_artists_request_params["limit"] = limit

    client.post(url=ARTISTS_URL, params=top_artists_request_params, json=mock_access_token_request)

    mock_spotify_data_service.get_top_artists.assert_called_once_with(
        access_token="access",
        time_range=time_range,
        limit=expected_limit
    )

# 11. Test /data/me/top/artists returns expected response.
def test_get_top_artists_returns_expected_response(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_artists_request_params,
        mock_spotify_artists
):
    mock_spotify_data_service.get_top_artists.return_value = mock_spotify_artists

    res = client.post(url=ARTISTS_URL, params=top_artists_request_params, json=mock_access_token_request)

    expected_json = [
        {
            "id": "1",
            "name": "artist_name",
            "images": [{"height": 100, "width": 100, "url": "image_url"}],
            "spotify_url": "spotify_url",
            "followers": 100,
            "genres": ["genre1", "genre2", "genre3"],
            "popularity": 50
        },
        {
            "id": "2",
            "name": "artist_name",
            "images": [{"height": 100, "width": 100, "url": "image_url"}],
            "spotify_url": "spotify_url",
            "followers": 100,
            "genres": ["genre1", "genre2", "genre3"],
            "popularity": 50
        },
        {
            "id": "3",
            "name": "artist_name",
            "images": [{"height": 100, "width": 100, "url": "image_url"}],
            "spotify_url": "spotify_url",
            "followers": 100,
            "genres": ["genre1", "genre2", "genre3"],
            "popularity": 50
        },
        {
            "id": "4",
            "name": "artist_name",
            "images": [{"height": 100, "width": 100, "url": "image_url"}],
            "spotify_url": "spotify_url",
            "followers": 100,
            "genres": ["genre1", "genre2", "genre3"],
            "popularity": 50
        },
        {
            "id": "5",
            "name": "artist_name",
            "images": [{"height": 100, "width": 100, "url": "image_url"}],
            "spotify_url": "spotify_url",
            "followers": 100,
            "genres": ["genre1", "genre2", "genre3"],
            "popularity": 50
        }
    ]
    assert res.status_code == 200 and res.json() == expected_json


# -------------------- GET TOP TRACKS -------------------- #
TRACKS_URL = f"{BASE_URL}/top/tracks"


@pytest.fixture
def top_tracks_request_params() -> dict[str, str | int]:
    return {"time_range": "short_term", "limit": 10}


# 1. Test /data/me/top/tracks returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
def test_get_top_tracks_returns_401_error_if_spotify_data_service_unauthorised_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_tracks_request_params
):
    mock_spotify_data_service.get_top_tracks.side_effect = SpotifyDataServiceUnauthorisedException("Test")

    res = client.post(url=TRACKS_URL, params=top_tracks_request_params, json=mock_access_token_request)

    assert res.status_code == 401 and res.json() == {"detail": "Invalid access token"}


# 2. Test /data/me/top/tracks returns 500 error if SpotifyDataServiceException occurs.
def test_get_top_tracks_returns_500_error_if_spotify_data_service_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_tracks_request_params
):
    mock_spotify_data_service.get_top_tracks.side_effect = SpotifyDataServiceException("Test")

    res = client.post(url=TRACKS_URL, params=top_tracks_request_params, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Failed to retrieve the user's top tracks"}


# 3. Test /data/me/top/tracks returns 500 error if general exception occurs.
def test_get_top_tracks_returns_500_error_if_general_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_tracks_request_params
):
    mock_spotify_data_service.get_top_tracks.side_effect = Exception("Test")

    res = client.post(url=TRACKS_URL, params=top_tracks_request_params, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 4. Test /data/me/top/tracks returns 422 error if request sends no POST body.
def test_get_top_tracks_returns_422_error_if_request_sends_no_post_body(client, top_tracks_request_params):
    res = client.post(url=TRACKS_URL, params=top_tracks_request_params)

    assert res.status_code == 422


# 5. Test /data/me/top/tracks returns 422 error if request missing access token.
def test_get_top_tracks_returns_422_error_if_request_missing_access_token(client, top_tracks_request_params):
    res = client.post(url=TRACKS_URL, params=top_tracks_request_params, json={"refresh_token": "refresh"})

    assert res.status_code == 422


# 6. Test /data/me/top/tracks returns 422 error if request missing time range.
def test_get_top_tracks_returns_422_error_if_request_missing_time_range(
        client,
        mock_access_token_request,
        top_tracks_request_params
):
    top_tracks_request_params.pop("time_range")

    res = client.post(url=TRACKS_URL, params=top_tracks_request_params, json=mock_access_token_request)

    assert res.status_code == 422


# 7. Test /data/me/top/genres returns 422 error if request time range invalid.
def test_get_top_tracks_returns_422_error_if_request_time_range_invalid(
        client,
        mock_access_token_request,
        top_tracks_request_params
):
    top_tracks_request_params["time_range"] = "short"

    res = client.post(url=TRACKS_URL, params=top_tracks_request_params, json=mock_access_token_request)

    assert res.status_code == 422


# 8. Test /data/me/top/tracks returns 422 error if request limit invalid.
@pytest.mark.parametrize("limit", [9, 0, -10, 51, 100])
def test_get_top_tracks_returns_422_error_if_request_limit_invalid(
        client,
        mock_access_token_request,
        top_tracks_request_params,
        limit
):
    top_tracks_request_params["limit"] = limit

    res = client.post(url=TRACKS_URL, params=top_tracks_request_params, json=mock_access_token_request)

    assert res.status_code == 422


# 9. Test /data/me/top/tracks returns 500 error if response data type invalid.
def test_get_top_tracks_returns_500_error_if_response_data_type_invalid(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_tracks_request_params
):
    mock_spotify_data_service.get_top_tracks.return_value = {}

    res = client.post(url=TRACKS_URL, params=top_tracks_request_params, json=mock_access_token_request)

    assert res.status_code == 500


# 10. Test /data/me/top/tracks calls get_top_tracks with expected params.
@pytest.mark.parametrize(
    "time_range, limit, expected_limit",
    [
        ("short_term", None, 50),
        ("medium_term", None, 50),
        ("long_term", None, 50),
        ("short_term", 25, 25),
        ("medium_term", 25, 25),
        ("long_term", 25, 25)
    ]
)
def test_get_top_tracks_calls_get_top_tracks_with_expected_params(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_tracks_request_params,
        time_range,
        limit,
        expected_limit
):
    mock_get_top_tracks = AsyncMock()
    mock_spotify_data_service.get_top_tracks = mock_get_top_tracks
    top_tracks_request_params["time_range"] = time_range
    if limit is None:
        top_tracks_request_params.pop("limit")
    else:
        top_tracks_request_params["limit"] = limit

    client.post(url=TRACKS_URL, params=top_tracks_request_params, json=mock_access_token_request)

    mock_spotify_data_service.get_top_tracks.assert_called_once_with(
        access_token="access",
        time_range=time_range,
        limit=expected_limit
    )

# 11. Test /data/me/top/tracks returns expected response.
def test_get_top_tracks_returns_expected_response(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_tracks_request_params,
        mock_spotify_tracks
):
    mock_spotify_data_service.get_top_tracks.return_value = mock_spotify_tracks

    res = client.post(url=TRACKS_URL, params=top_tracks_request_params, json=mock_access_token_request)

    expected_json = [
        {
            "id": "1",
            "name": "track_name",
            "images": [{"height": 100, "width": 100, "url": "image_url"}],
            "spotify_url": "spotify_url",
            "artist": {"id": "1", "name": "artist_name"},
            "release_date": "release_date",
            "album_name": "album_name",
            "explicit": False,
            "duration_ms": 180000,
            "popularity": 50
        },
        {
            "id": "2",
            "name": "track_name",
            "images": [{"height": 100, "width": 100, "url": "image_url"}],
            "spotify_url": "spotify_url",
            "artist": {"id": "2", "name": "artist_name"},
            "release_date": "release_date",
            "album_name": "album_name",
            "explicit": False,
            "duration_ms": 180000,
            "popularity": 50
        },
        {
            "id": "3",
            "name": "track_name",
            "images": [{"height": 100, "width": 100, "url": "image_url"}],
            "spotify_url": "spotify_url",
            "artist": {"id": "3", "name": "artist_name"},
            "release_date": "release_date",
            "album_name": "album_name",
            "explicit": False,
            "duration_ms": 180000,
            "popularity": 50
        },
        {
            "id": "4",
            "name": "track_name",
            "images": [{"height": 100, "width": 100, "url": "image_url"}],
            "spotify_url": "spotify_url",
            "artist": {"id": "4", "name": "artist_name"},
            "release_date": "release_date",
            "album_name": "album_name",
            "explicit": False,
            "duration_ms": 180000,
            "popularity": 50
        },
        {
            "id": "5",
            "name": "track_name",
            "images": [{"height": 100, "width": 100, "url": "image_url"}],
            "spotify_url": "spotify_url",
            "artist": {"id": "5", "name": "artist_name"},
            "release_date": "release_date",
            "album_name": "album_name",
            "explicit": False,
            "duration_ms": 180000,
            "popularity": 50
        }
    ]
    assert res.status_code == 200 and res.json() == expected_json


# -------------------- GET TOP GENRES -------------------- #
GENRES_URL = f"{BASE_URL}/top/genres"


@pytest.fixture
def top_genres_request_params() -> dict[str, str | int]:
    return {"time_range": "short_term"}


# 1. Test /data/me/top/genres returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
def test_get_top_genres_returns_401_error_if_spotify_data_service_unauthorised_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_genres_request_params
):
    mock_spotify_data_service.get_top_genres.side_effect = SpotifyDataServiceUnauthorisedException("Test")

    res = client.post(url=GENRES_URL, params=top_genres_request_params, json=mock_access_token_request)

    assert res.status_code == 401 and res.json() == {"detail": "Invalid access token"}


# 2. Test /data/me/top/genres returns 500 error if SpotifyDataServiceException occurs.
def test_get_top_genres_returns_500_error_if_spotify_data_service_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_genres_request_params
):
    mock_spotify_data_service.get_top_genres.side_effect = SpotifyDataServiceException("Test")

    res = client.post(url=GENRES_URL, params=top_genres_request_params, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Failed to retrieve the user's top genres"}


# 3. Test /data/me/top/genres returns 500 error if general exception occurs.
def test_get_top_genres_returns_500_error_if_general_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_genres_request_params
):
    mock_spotify_data_service.get_top_genres.side_effect = Exception("Test")

    res = client.post(url=GENRES_URL, params=top_genres_request_params, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 4. Test /data/me/top/genres returns 422 error if request sends no POST body.
def test_get_top_genres_returns_422_error_if_request_sends_no_post_body(client, top_genres_request_params):
    res = client.post(url=GENRES_URL, params=top_genres_request_params)

    assert res.status_code == 422
    

# 5. Test /data/me/top/genres returns 422 error if request missing access token.
def test_get_top_genres_returns_422_error_if_request_missing_access_token(client, top_genres_request_params):
    res = client.post(url=GENRES_URL, params=top_genres_request_params, json={"refresh_token": "refresh"})

    assert res.status_code == 422
    

# 6. Test /data/me/top/genres returns 422 error if request missing time range.
def test_get_top_genres_returns_422_error_if_request_missing_time_range(
        client,
        mock_access_token_request,
        top_genres_request_params
):
    top_genres_request_params.pop("time_range")

    res = client.post(url=GENRES_URL, params=top_genres_request_params, json=mock_access_token_request)

    assert res.status_code == 422
    

# 7. Test /data/me/top/genres returns 422 error if request time range invalid.
def test_get_top_genres_returns_422_error_if_request_time_range_invalid(
        client,
        mock_access_token_request,
        top_genres_request_params
):
    top_genres_request_params["time_range"] = "short"

    res = client.post(url=GENRES_URL, params=top_genres_request_params, json=mock_access_token_request)

    assert res.status_code == 422
    

# 8. Test /data/me/top/genres returns 500 error if response data type invalid.
def test_get_top_genres_returns_500_error_if_response_data_type_invalid(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_genres_request_params
):
    mock_spotify_data_service.get_top_genres.return_value = {}

    res = client.post(url=GENRES_URL, params=top_genres_request_params, json=mock_access_token_request)

    assert res.status_code == 500
    

# 9. Test /data/me/top/genres calls get_top_genres with expected params.
@pytest.mark.parametrize("time_range", ["short_term", "medium_term", "long_term"])
def test_get_top_genres_calls_get_top_genres_with_expected_params(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        top_genres_request_params,
        time_range
):
    mock_get_top_genres = AsyncMock()
    mock_spotify_data_service.get_top_genres = mock_get_top_genres
    top_genres_request_params["time_range"] = time_range

    client.post(url=GENRES_URL, params=top_genres_request_params, json=mock_access_token_request)

    mock_spotify_data_service.get_top_genres.assert_called_once_with(access_token="access", time_range=time_range)


@pytest.fixture
def mock_top_genre_factory():
    def _create(name: str, count: float) -> TopGenre:
        return TopGenre(name=name, count=count)

    return _create
    

# 10. Test /data/me/top/genres returns expected response.
def test_get_top_genres_returns_expected_response(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        mock_top_genre_factory,
        top_genres_request_params
):
    mock_spotify_data_service.get_top_genres.return_value = [
        mock_top_genre_factory(name="genre1", count=6),
        mock_top_genre_factory(name="genre2", count=5),
        mock_top_genre_factory(name="genre3", count=3),
        mock_top_genre_factory(name="genre4", count=2),
        mock_top_genre_factory(name="genre5", count=1)
    ]

    res = client.post(url=GENRES_URL, params=top_genres_request_params, json=mock_access_token_request)

    expected_json = [
        {"name": "genre1", "count": 6},
        {"name": "genre2", "count": 5},
        {"name": "genre3", "count": 3},
        {"name": "genre4", "count": 2},
        {"name": "genre5", "count": 1}
    ]
    assert res.status_code == 200 and res.json() == expected_json


# -------------------- GET TOP EMOTIONS -------------------- #
EMOTIONS_URL = f"{BASE_URL}/top/emotions"


@pytest.fixture
def top_emotions_request_params() -> dict[str, str | int]:
    return {"time_range": "short_term"}


# 1. Test /data/me/top/emotions returns 500 error if InsightsServiceException occurs.
def test_get_top_emotions_returns_500_error_if_spotify_data_service_exception_occurs(
        client,
        mock_insights_service,
        mock_access_token_request,
        top_emotions_request_params
):
    mock_insights_service.get_top_emotions.side_effect = InsightsServiceException("Test")

    res = client.post(url=EMOTIONS_URL, params=top_emotions_request_params, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Failed to retrieve the user's top emotions"}


# 2. Test /data/me/top/emotions returns 500 error if general exception occurs.
def test_get_top_emotions_returns_500_error_if_general_exception_occurs(
        client,
        mock_insights_service,
        mock_access_token_request,
        top_emotions_request_params
):
    mock_insights_service.get_top_emotions.side_effect = Exception("Test")

    res = client.post(url=EMOTIONS_URL, params=top_emotions_request_params, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 3. Test /data/me/top/emotions returns 422 error if request sends no POST body.
def test_get_top_emotions_returns_422_error_if_request_sends_no_post_body(client, top_emotions_request_params):
    res = client.post(url=EMOTIONS_URL, params=top_emotions_request_params)

    assert res.status_code == 422
    
    
# 4. Test /data/me/top/emotions returns 422 error if request missing access token.
def test_get_top_emotions_returns_422_error_if_request_missing_access_token(client, top_emotions_request_params):
    res = client.post(url=EMOTIONS_URL, params=top_emotions_request_params, json={"refresh_token": "refresh"})

    assert res.status_code == 422


# 5. Test /data/me/top/emotions returns 422 error if request missing time range.
def test_get_top_emotions_returns_422_error_if_request_missing_time_range(
        client,
        mock_access_token_request,
        top_emotions_request_params
):
    top_emotions_request_params.pop("time_range")

    res = client.post(url=EMOTIONS_URL, params=top_emotions_request_params, json=mock_access_token_request)

    assert res.status_code == 422


# 6. Test /data/me/top/emotions returns 422 error if request invalid time range.
def test_get_top_emotions_returns_422_error_if_request_time_range_invalid(
        client,
        mock_access_token_request,
        top_emotions_request_params
):
    top_emotions_request_params["time_range"] = "short"

    res = client.post(url=EMOTIONS_URL, params=top_emotions_request_params, json=mock_access_token_request)

    assert res.status_code == 422


# 9. Test /data/me/top/emotions returns 500 error if response data type invalid.
@pytest.mark.parametrize("time_range", ["short_term", "medium_term", "long_term"])
def test_get_top_emotions_calls_get_top_emotions_with_expected_params(
        client,
        mock_insights_service,
        mock_access_token_request,
        top_emotions_request_params,
        time_range
):
    mock_get_top_emotions = AsyncMock()
    mock_insights_service.get_top_emotions = mock_get_top_emotions
    top_emotions_request_params["time_range"] = time_range

    client.post(url=EMOTIONS_URL, params=top_emotions_request_params, json=mock_access_token_request)

    mock_insights_service.get_top_emotions.assert_called_once_with(access_token="access", time_range=time_range)


@pytest.fixture
def mock_top_emotion_factory():
    def _create(name: str, percentage: EmotionPercentage, track_id: str) -> TopEmotion:
        return TopEmotion(name=name, percentage=percentage, track_id=track_id)

    return _create


# 10. Test /data/me/top/emotions returns expected response.
def test_get_top_emotions_returns_expected_response(
        client,
        mock_insights_service,
        mock_access_token_request,
        mock_top_emotion_factory,
        top_emotions_request_params
):
    mock_insights_service.get_top_emotions.return_value = [
        mock_top_emotion_factory(name="emotion1", percentage=0.42, track_id="1"),
        mock_top_emotion_factory(name="emotion2", percentage=0.3, track_id="2"),
        mock_top_emotion_factory(name="emotion3", percentage=0.16, track_id="3"),
        mock_top_emotion_factory(name="emotion4", percentage=0.08, track_id="4"),
        mock_top_emotion_factory(name="emotion5", percentage=0.04, track_id="5")
    ]

    res = client.post(url=EMOTIONS_URL, params=top_emotions_request_params, json=mock_access_token_request)

    expected_json = [
        {"name": "emotion1", "percentage": 0.42, "track_id": "1"},
        {"name": "emotion2", "percentage": 0.3, "track_id": "2"},
        {"name": "emotion3", "percentage": 0.16, "track_id": "3"},
        {"name": "emotion4", "percentage": 0.08, "track_id": "4"},
        {"name": "emotion5", "percentage": 0.04, "track_id": "5"}
    ]
    assert res.status_code == 200 and res.json() == expected_json
