from unittest.mock import AsyncMock

import pytest

from api.models.models import SpotifyArtist, TopGenre
from api.services.spotify.spotify_data_service import SpotifyDataServiceException


# 1. Test get_top_genres raises SpotifyDataServiceException if get_top_artists returns empty list.
# 2. Test get_top_genres raises SpotifyDataServiceException if limit less than 1.
# 3. Test get_top_genres returns empty list if no all genres empty in top artists.
# 4. Test get_top_genres returns expected genres.


# 1. Test get_top_genres raises SpotifyDataServiceException if get_top_artists returns empty list.
@pytest.mark.asyncio
async def test_get_top_genres_raises_spotify_data_service_exception_if_get_top_artists_returns_empty_list(
        spotify_data_service
):
    mock_get_top_artists = AsyncMock()
    mock_get_top_artists.return_value = []
    spotify_data_service.get_top_artists = mock_get_top_artists

    with pytest.raises(SpotifyDataServiceException) as e:
        await spotify_data_service.get_top_genres(access_token="", time_range="", limit=1)

    assert "No top artists found. Cannot proceed with analysis." in str(e.value)


# 2. Test get_top_genres raises SpotifyDataServiceException if limit less than 1.
@pytest.mark.asyncio
@pytest.mark.parametrize("limit", [0, -1, -10])
async def test_get_top_genres_raises_spotify_data_service_exception_if_limit_less_than_1(spotify_data_service, limit):
    with pytest.raises(SpotifyDataServiceException) as e:
        await spotify_data_service.get_top_genres(access_token="", time_range="", limit=limit)

    assert "Limit must be at least 1." in str(e.value)


# 3. Test get_top_genres returns empty list if no all genres empty in top artists.
@pytest.mark.asyncio
async def test_get_top_genres_returns_empty_list_if_no_genres_in_top_artists(spotify_data_service):
    mock_get_top_artists = AsyncMock()
    artist1 = SpotifyArtist(
        id="1",
        name="",
        images=[],
        spotify_url="",
        genres=[],
        followers=0,
        popularity=50
    )
    artist2 = SpotifyArtist(
        id="2",
        name="",
        images=[],
        spotify_url="",
        genres=[],
        followers=0,
        popularity=50
    )
    mock_get_top_artists.return_value = [artist1, artist2]
    spotify_data_service.get_top_artists = mock_get_top_artists

    top_genres = await spotify_data_service.get_top_genres(access_token="", time_range="", limit=10)

    assert top_genres == []


# 4. Test get_top_genres returns expected genres.
@pytest.mark.asyncio
@pytest.mark.parametrize("limit", [10, 3, 2, 1])
async def test_get_top_genres_returns_expected_genres(spotify_data_service, limit):
    mock_get_top_artists = AsyncMock()
    artist1 = SpotifyArtist(
        id="1",
        name="artist1",
        images=[],
        spotify_url="",
        genres=["rock", "metal", "emo", "pop-punk"],
        followers=0,
        popularity=50
    )
    artist2 = SpotifyArtist(
        id="2",
        name="artist2",
        images=[],
        spotify_url="",
        genres=["rock", "metal", "pop-punk"],
        followers=0,
        popularity=50
    )
    artist3 = SpotifyArtist(
        id="3",
        name="artist3",
        images=[],
        spotify_url="",
        genres=[],
        followers=0,
        popularity=50
    )
    artist4 = SpotifyArtist(
        id="4",
        name="artist4",
        images=[],
        spotify_url="",
        genres=["pop-punk"],
        followers=0,
        popularity=50
    )
    artist5 = SpotifyArtist(
        id="5",
        name="artist5",
        images=[],
        spotify_url="",
        genres=["metal"],
        followers=0,
        popularity=50
    )
    artist6 = SpotifyArtist(
        id="6",
        name="artist6",
        images=[],
        spotify_url="",
        genres=["metal"],
        followers=0,
        popularity=50
    )
    mock_get_top_artists.return_value = [artist1, artist2, artist3, artist4, artist5, artist6]
    spotify_data_service.get_top_artists = mock_get_top_artists

    top_genres = await spotify_data_service.get_top_genres(access_token="", time_range="", limit=limit)

    expected_top_genres = [
        TopGenre(name="metal", percentage=40),
        TopGenre(name="pop-punk", percentage=30),
        TopGenre(name="rock", percentage=20),
        TopGenre(name="emo", percentage=10),
    ]
    assert len(top_genres) <= limit and top_genres == expected_top_genres[:limit]
