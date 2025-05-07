import pytest

from api.models.models import SpotifyArtist, SpotifyImage
from api.services.spotify.spotify_data_service import SpotifyDataServiceNotFoundException, SpotifyDataServiceException, \
    SpotifyDataServiceUnauthorisedException

# -------------------- GET ARTIST BY ID -------------------- #
# 1. Test /data/artists/{artist_id} returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/artists/{artist_id} returns 404 error if SpotifyDataServiceNotFoundException occurs.
# 3. Test /data/artists/{artist_id} returns 500 error if SpotifyDataServiceException occurs.
# 4. Test /data/artists/{artist_id} returns 500 error if general exception occurs.
# 5. Test /data/artists/{artist_id} returns 422 error if request sends no POST body.
# 6. Test /data/artists/{artist_id} returns 422 error if request missing access token.
# 7. Test /data/artists/{artist_id} returns 500 error if response data type invalid.
# 8. Test /data/artists/{artist_id} returns expected response.

# -------------------- GET SEVERAL ARTISTS BY IDS -------------------- #
# 1. Test /data/artists returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/artists returns 404 error if SpotifyDataServiceNotFoundException occurs.
# 3. Test /data/artists returns 500 error if SpotifyDataServiceException occurs.
# 4. Test /data/artists returns 500 error if general exception occurs.
# 5. Test /data/artists returns 422 error if request sends no POST body.
# 6. Test /data/artists returns 422 error if request missing access token.
# 7. Test /data/artists returns 500 error if response data type invalid.
# 8. Test /data/artists returns expected response.

BASE_URL = "/data/artists"

# -------------------- GET ARTIST BY ID -------------------- #
ARTIST_URL = f"{BASE_URL}/1"


# 1. Test /data/artists/{artist_id} returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
def test_get_artist_by_id_returns_401_error_if_spotify_data_service_unauthorised_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_artist_by_id.side_effect = SpotifyDataServiceUnauthorisedException("Test")

    res = client.post(url=ARTIST_URL, json=mock_access_token_request)

    assert res.status_code == 401 and res.json() == {"detail": "Invalid access token"}


# 2. Test /data/artists/{artist_id} returns 404 error if SpotifyDataServiceNotFoundException occurs.
def test_get_artist_by_id_returns_404_error_if_spotify_data_service_not_found_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_artist_by_id.side_effect = SpotifyDataServiceNotFoundException("Test")

    res = client.post(url=ARTIST_URL, json=mock_access_token_request)

    assert res.status_code == 404 and res.json() == {"detail": "Could not find the requested artist"}


# 3. Test /data/artists/{artist_id} returns 500 error if SpotifyDataServiceException occurs.
def test_get_artist_by_id_returns_500_error_if_spotify_data_service_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_artist_by_id.side_effect = SpotifyDataServiceException("Test")

    res = client.post(url=ARTIST_URL, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Failed to retrieve the requested artist"}


# 4. Test /data/artists/{artist_id} returns 500 error if general exception occurs.
def test_get_artist_by_id_returns_500_error_if_general_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_artist_by_id.side_effect = Exception("Test")

    res = client.post(url=ARTIST_URL, json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 5. Test /data/artists/{artist_id} returns 422 error if request sends no POST body.
def test_get_artist_by_id_returns_422_error_if_request_sends_no_post_body(client):
    res = client.post(url=ARTIST_URL)

    assert res.status_code == 422


# 6. Test /data/artists/{artist_id} returns 422 error if request missing access token.
def test_get_artist_by_id_returns_422_error_if_request_missing_access_token(client):
    res = client.post(url=ARTIST_URL, json={"refresh_token": "refresh"})

    assert res.status_code == 422


# 7. Test /data/artists/{artist_id} returns 500 error if response data type invalid.
def test_get_artist_by_id_returns_500_error_if_response_data_type_invalid(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_artist_by_id.return_value = {}

    res = client.post(url=ARTIST_URL, json=mock_access_token_request)

    assert res.status_code == 500


# 8. Test /data/artists/{artist_id} returns expected response.
def test_get_artist_by_id_returns_expected_response(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        mock_spotify_artist_factory
):
    mock_spotify_data_service.get_artist_by_id.return_value = mock_spotify_artist_factory()

    res = client.post(url=ARTIST_URL, json=mock_access_token_request)

    expected_json = {
        "id": "1",
        "name": "artist_name",
        "images": [{"height": 100, "width": 100, "url": "image_url"}],
        "spotify_url": "spotify_url",
        "followers": 100,
        "genres": ["genre1", "genre2", "genre3"],
        "popularity": 50
    }
    assert res.status_code == 200 and res.json() == expected_json


# -------------------- GET SEVERAL ARTISTS BY IDS -------------------- #
# 1. Test /data/artists returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
def test_get_several_artists_by_ids_returns_401_error_if_spotify_data_service_unauthorised_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_artists_by_ids.side_effect = SpotifyDataServiceUnauthorisedException("Test")
    request_body = {"requested_artists": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 401 and res.json() == {"detail": "Invalid access token"}


# 2. Test /data/artists returns 404 error if SpotifyDataServiceNotFoundException occurs.
def test_get_several_artists_by_ids_returns_404_error_if_spotify_data_service_not_found_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_artists_by_ids.side_effect = SpotifyDataServiceNotFoundException("Test")
    request_body = {"requested_artists": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 404 and res.json() == {"detail": "Could not find the requested artists"}


# 3. Test /data/artists returns 500 error if SpotifyDataServiceException occurs.
def test_get_several_artists_by_ids_returns_500_error_if_spotify_data_service_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_artists_by_ids.side_effect = SpotifyDataServiceException("Test")
    request_body = {"requested_artists": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 500 and res.json() == {"detail": "Failed to retrieve the requested artists"}


# 4. Test /data/artists returns 500 error if general exception occurs.
def test_get_several_artists_by_ids_returns_500_error_if_general_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_artists_by_ids.side_effect = Exception("Test")
    request_body = {"requested_artists": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 5. Test /data/artists returns 422 error if request sends no POST body.
def test_get_several_artists_by_ids_returns_422_error_if_request_sends_no_post_body(client):
    res = client.post(url=BASE_URL)

    assert res.status_code == 422


# 6. Test /data/artists returns 422 error if request missing access token.
def test_get_several_artists_by_ids_returns_422_error_if_request_missing_access_token(client):
    request_body = {"requested_artists": {"ids": []}}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 422


# 7. Test /data/artists returns 500 error if response data type invalid.
def test_get_several_artists_by_ids_returns_500_error_if_response_data_type_invalid(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_artists_by_ids.return_value = [{}]
    request_body = {"requested_artists": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 500


# 8. Test /data/artists returns expected response.
def test_get_several_artists_by_ids_returns_expected_response(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        mock_spotify_artists
):
    mock_spotify_data_service.get_artists_by_ids.return_value = mock_spotify_artists
    request_body = {"requested_artists": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

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
