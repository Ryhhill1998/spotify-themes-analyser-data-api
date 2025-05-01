from copy import deepcopy

# 1. Test _create_track raises SpotifyDataServiceException if input data is not a dict.
# 2. Test _create_track raises SpotifyDataServiceException if fields missing from input data.
# 3. Test _create_track returns expected track.
# 4. Test _create_artist raises SpotifyDataServiceException if input data is not a dict.
# 5. Test _create_artist raises SpotifyDataServiceException if fields missing from input data.
# 6. Test _create_artist returns expected track.

import pytest

from api.services.spotify.spotify_data_service import SpotifyDataServiceException


@pytest.fixture
def track_data() -> dict:
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
def artist_data() -> dict:
    return {
        "id": "1",
        "name": "artist_name",
        "images": [{"height": 100, "width": 100, "url": "album_image_url"}],
        "external_urls": {"spotify": "spotify_url"},
        "followers": {"total": 100},
        "genres": ["genre1", "genre2", "genre3"],
        "popularity": 50
    }


def delete_field(data: dict, field: str):
    data_copy = deepcopy(data)
    keys = field.split(".")
    current = data_copy

    for key in keys[:-1]:
        if key == "[]":
            current = current[0]
        else:
            current = current[key]

    del current[keys[-1]]
    return data_copy, keys[-1]


# 1. Test _create_track raises SpotifyDataServiceException if input data is not a dict.
def test__create_track_raises_spotify_data_service_exception_if_data_not_a_dict(spotify_data_service):
    with pytest.raises(SpotifyDataServiceException) as e:
        spotify_data_service._create_track("")

    assert "Spotify data not of type dict. Actual type: <class 'str'>" in str(e.value)


# 2. Test _create_track raises SpotifyDataServiceException if fields missing from input data.
@pytest.mark.parametrize(
    "missing_field",
    [
        "id",
        "name",
        "album",
        "album.name",
        "album.images",
        "album.images.[].height",
        "album.images.[].width",
        "album.images.[].url",
        "album.release_date",
        "artists",
        "artists.[].id",
        "artists.[].name",
        "external_urls",
        "external_urls.spotify",
        "explicit",
        "duration_ms",
        "popularity"
    ]
)
def test__create_track_raises_spotify_data_service_exception_if_data_missing_fields(
        spotify_data_service,
        track_data,
        missing_field
):
    data, deleted_field = delete_field(data=track_data, field=missing_field)

    with pytest.raises(SpotifyDataServiceException) as e:
        spotify_data_service._create_track(data)

    assert "Failed to create SpotifyTrack from Spotify API data" in str(e.value) and deleted_field in str(e.value)


# 3. Test _create_track returns expected track.
def test__create_track_returns_expected_track():
    pass


# 4. Test _create_artist raises SpotifyDataServiceException if input data is not a dict.
def test__create_artist_raises_spotify_data_service_exception_if_data_not_a_dict(spotify_data_service):
    with pytest.raises(SpotifyDataServiceException) as e:
        spotify_data_service._create_track("")

    assert "Spotify data not of type dict. Actual type: <class 'str'>" in str(e.value)


# 5. Test _create_artist raises SpotifyDataServiceException if fields missing from input data.
@pytest.mark.parametrize(
    "missing_field",
    [
        "id",
        "name",
        "images",
        "images.[].height",
        "images.[].width",
        "images.[].url",
        "external_urls",
        "external_urls.spotify",
        "followers",
        "followers.total",
        "genres",
        "popularity"
    ]
)
def test__create_artist_raises_spotify_data_service_exception_if_data_missing_fields(
        spotify_data_service,
        artist_data,
        missing_field
):
    data, deleted_field = delete_field(data=artist_data, field=missing_field)

    with pytest.raises(SpotifyDataServiceException) as e:
        spotify_data_service._create_artist(data)

    assert "Failed to create SpotifyArtist from Spotify API data" in str(e.value) and deleted_field in str(e.value)



# 6. Test _create_artist returns expected track.
def test__create_artist_returns_expected_track():
    pass
