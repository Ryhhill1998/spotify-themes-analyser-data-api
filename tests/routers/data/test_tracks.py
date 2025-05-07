import pytest

from api.models.models import EmotionalTagsResponse, Emotion
from api.services.insights_service import InsightsServiceException
from api.services.spotify.spotify_data_service import SpotifyDataServiceNotFoundException, SpotifyDataServiceException, \
    SpotifyDataServiceUnauthorisedException

BASE_URL = "/data/tracks"


# -------------------- GET TRACK BY ID -------------------- #
# 1. Test /data/tracks/{track_id} returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/tracks/{track_id} returns 404 error if SpotifyDataServiceNotFoundException occurs.
# 3. Test /data/tracks/{track_id} returns 500 error if SpotifyDataServiceException occurs.
# 4. Test /data/tracks/{track_id} returns 500 error if general exception occurs.
# 5. Test /data/tracks/{track_id} returns 422 error if request sends no POST body.
# 6. Test /data/tracks/{track_id} returns 422 error if request missing access token.
# 7. Test /data/tracks/{track_id} returns 500 error if response data type invalid.
# 8. Test /data/tracks/{track_id} returns expected response.

# -------------------- GET SEVERAL TRACKS BY IDS -------------------- #
# 1. Test /data/tracks returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/tracks returns 404 error if SpotifyDataServiceNotFoundException occurs.
# 3. Test /data/tracks returns 500 error if SpotifyDataServiceException occurs.
# 4. Test /data/tracks returns 500 error if general exception occurs.
# 5. Test /data/tracks returns 422 error if request sends no POST body.
# 6. Test /data/tracks returns 422 error if request missing access token.
# 7. Test /data/tracks returns 500 error if response data type invalid.
# 8. Test /data/tracks returns expected response.

# -------------------- GET LYRICS TAGGED WITH EMOTION -------------------- #
# 1. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns 500 error if InsightsServiceException occurs.
# 2. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns 500 error if general exception occurs.
# 3. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns 422 error if request sends no POST body.
# 4. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns 422 error if request missing access token.
# 5. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns 500 error if response data type invalid.
# 6. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns expected response.


@pytest.fixture
def mock_access_token_request() -> dict[str, str]:
    return {"access_token": "access"}


# -------------------- GET TRACK BY ID -------------------- #
# 1. Test /data/tracks/{track_id} returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
def test_get_track_by_id_returns_401_error_if_spotify_data_service_unauthorised_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_track_by_id.side_effect = SpotifyDataServiceUnauthorisedException("Test")

    res = client.post(url=f"{BASE_URL}/1", json=mock_access_token_request)

    assert res.status_code == 401 and res.json() == {"detail": "Invalid access token"}


# 2. Test /data/tracks/{track_id} returns 404 error if SpotifyDataServiceNotFoundException occurs.
def test_get_track_by_id_returns_404_error_if_spotify_data_service_not_found_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_track_by_id.side_effect = SpotifyDataServiceNotFoundException("Test")

    res = client.post(url=f"{BASE_URL}/1", json=mock_access_token_request)

    assert res.status_code == 404 and res.json() == {"detail": "Could not find the requested track"}


# 3. Test /data/tracks/{track_id} returns 500 error if SpotifyDataServiceException occurs.
def test_get_track_by_id_returns_500_error_if_spotify_data_service_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_track_by_id.side_effect = SpotifyDataServiceException("Test")

    res = client.post(url=f"{BASE_URL}/1", json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Failed to retrieve the requested track"}


# 4. Test /data/tracks/{track_id} returns 500 error if general exception occurs.
def test_get_track_by_id_returns_500_error_if_general_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_track_by_id.side_effect = Exception("Test")

    res = client.post(url=f"{BASE_URL}/1", json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 5. Test /data/tracks/{track_id} returns 422 error if request sends no POST body.
def test_get_track_by_id_returns_422_error_if_request_sends_no_post_body(client):
    res = client.post(url=f"{BASE_URL}/1")

    assert res.status_code == 422


# 6. Test /data/tracks/{track_id} returns 422 error if request missing access token.
def test_get_track_by_id_returns_422_error_if_request_missing_access_token(client):
    res = client.post(url=f"{BASE_URL}/1", json={"refresh_token": "refresh"})

    assert res.status_code == 422


# 7. Test /data/tracks/{track_id} returns 500 error if response data type invalid.
def test_get_track_by_id_returns_500_error_if_response_data_type_invalid(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_track_by_id.return_value = {}

    res = client.post(url=f"{BASE_URL}/1", json=mock_access_token_request)

    assert res.status_code == 500


# 8. Test /data/tracks/{track_id} returns expected response.
def test_get_track_by_id_returns_expected_response(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        mock_spotify_track_factory
):
    mock_spotify_data_service.get_track_by_id.return_value = mock_spotify_track_factory()

    res = client.post(url=f"{BASE_URL}/1", json=mock_access_token_request)

    expected_json = {
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
    }
    assert res.status_code == 200 and res.json() == expected_json


# -------------------- GET SEVERAL TRACKS BY IDS -------------------- #
# 1. Test /data/tracks returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
def test_get_several_tracks_by_ids_returns_401_error_if_spotify_data_service_unauthorised_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_tracks_by_ids.side_effect = SpotifyDataServiceUnauthorisedException("Test")
    request_body = {"requested_tracks": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 401 and res.json() == {"detail": "Invalid access token"}


# 2. Test /data/tracks returns 404 error if SpotifyDataServiceNotFoundException occurs.
def test_get_several_tracks_by_ids_returns_404_error_if_spotify_data_service_not_found_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_tracks_by_ids.side_effect = SpotifyDataServiceNotFoundException("Test")
    request_body = {"requested_tracks": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 404 and res.json() == {"detail": "Could not find the requested tracks"}


# 3. Test /data/tracks returns 500 error if SpotifyDataServiceException occurs.
def test_get_several_tracks_by_ids_returns_500_error_if_spotify_data_service_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_tracks_by_ids.side_effect = SpotifyDataServiceException("Test")
    request_body = {"requested_tracks": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 500 and res.json() == {"detail": "Failed to retrieve the requested tracks"}


# 4. Test /data/tracks returns 500 error if general exception occurs.
def test_get_several_tracks_by_ids_returns_500_error_if_general_exception_occurs(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_tracks_by_ids.side_effect = Exception("Test")
    request_body = {"requested_tracks": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 5. Test /data/tracks returns 422 error if request sends no POST body.
def test_get_several_tracks_by_ids_returns_422_error_if_request_sends_no_post_body(client):
    res = client.post(url=BASE_URL)

    assert res.status_code == 422


# 6. Test /data/tracks returns 422 error if request missing access token.
def test_get_several_tracks_by_ids_returns_422_error_if_request_missing_access_token(client):
    request_body = {"requested_tracks": {"ids": []}}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 422


# 7. Test /data/tracks returns 500 error if response data type invalid.
def test_get_several_tracks_by_ids_returns_500_error_if_response_data_type_invalid(
        client,
        mock_spotify_data_service,
        mock_access_token_request
):
    mock_spotify_data_service.get_tracks_by_ids.return_value = [{}]
    request_body = {"requested_tracks": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

    assert res.status_code == 500


# 8. Test /data/tracks returns expected response.
def test_get_several_tracks_by_ids_returns_expected_response(
        client,
        mock_spotify_data_service,
        mock_access_token_request,
        mock_spotify_tracks
):
    mock_spotify_data_service.get_tracks_by_ids.return_value = mock_spotify_tracks
    request_body = {"requested_tracks": {"ids": []}, "access_token": mock_access_token_request}

    res = client.post(url=BASE_URL, json=request_body)

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


# -------------------- GET LYRICS TAGGED WITH EMOTION -------------------- #
# 1. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns 500 error if InsightsServiceException occurs.
def test_get_lyrics_tagged_with_emotion_returns_500_error_if_insights_service_exception_occurs(
        client,
        mock_insights_service,
        mock_access_token_request
):
    mock_insights_service.tag_lyrics_with_emotion.side_effect = InsightsServiceException("Test")

    res = client.post(url=f"{BASE_URL}/1/lyrics/emotional-tags/sadness", json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Failed to tag lyrics with requested emotion: sadness"}
    

# 2. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns 500 error if general exception occurs.
def test_get_lyrics_tagged_with_emotion_returns_500_error_if_general_exception_occurs(
        client,
        mock_insights_service,
        mock_access_token_request
):
    mock_insights_service.tag_lyrics_with_emotion.side_effect = Exception("Test")

    res = client.post(url=f"{BASE_URL}/1/lyrics/emotional-tags/sadness", json=mock_access_token_request)

    assert res.status_code == 500 and res.json() == {"detail": "Something went wrong. Please try again later."}


# 3. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns 422 error if request sends no POST body.
def test_get_lyrics_tagged_with_emotion_returns_422_error_if_request_sends_no_post_body(client):
    res = client.post(url=f"{BASE_URL}/1/lyrics/emotional-tags/sadness")

    assert res.status_code == 422


# 4. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns 422 error if request missing access token.
def test_get_lyrics_tagged_with_emotion_returns_422_error_if_request_missing_access_token(client):
    res = client.post(url=f"{BASE_URL}/1/lyrics/emotional-tags/sadness", json={"refresh_token": "refresh"})

    assert res.status_code == 422


# 5. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns 500 error if response data type invalid.
def test_get_lyrics_tagged_with_emotion_returns_422_error_if_response_data_type_invalid(
        client,
        mock_insights_service,
        mock_access_token_request
):
    mock_insights_service.tag_lyrics_with_emotion.return_value = {}

    res = client.post(url=f"{BASE_URL}/1/lyrics/emotional-tags/sadness", json=mock_access_token_request)

    assert res.status_code == 500


# 6. Test /tracks/{track_id}/lyrics/emotions/{emotion} returns expected response.
def test_get_lyrics_tagged_with_emotion_returns_expected_response(
        client,
        mock_insights_service,
        mock_access_token_request
):
    mock_insights_service.tag_lyrics_with_emotion.return_value = EmotionalTagsResponse(
        track_id="1",
        lyrics="lyrics",
        emotion=Emotion.SADNESS
    )

    res = client.post(url=f"{BASE_URL}/1/lyrics/emotional-tags/sadness", json=mock_access_token_request)

    expected_json = {"track_id": "1", "lyrics": "lyrics", "emotion": "sadness"}
    assert res.status_code == 200 and res.json() == expected_json
