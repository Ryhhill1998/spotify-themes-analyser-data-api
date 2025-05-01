from unittest.mock import AsyncMock, Mock

import pytest

from api.models.models import SpotifyArtist, SpotifyTrack
from api.services.endpoint_requester import EndpointRequesterException, EndpointRequesterUnauthorisedException
from api.services.spotify.spotify_data_service import SpotifyDataServiceException, SpotifyItemType

TEST_URL = "http://test-url.com"

# 1. Test _get_top_items_data raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
# 2. Test _get_top_items_data raises SpotifyDataServiceException if EndpointRequesterException occurs.
# 3. Test _get_top_items_data raises KeyError if items key not present in data.
# 4. Test _get_top_items_data returns expected response.
# 5. Test get_top_artists calls expected methods.
# 6. Test get_top_tracks calls expected methods.


# 1. Test _get_top_items_data raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
@pytest.mark.asyncio
async def test_get_top_items_raises_spotify_data_service_unauthorised_exception_if_endpoint_requester_unauthorised_exception_occurs(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterUnauthorisedException()

    with pytest.raises(SpotifyDataServiceException, match="Invalid Spotify API access token"):
        await spotify_data_service._get_top_items_data(
            access_token="access_token",
            item_type=SpotifyItemType.TRACK,
            time_range="medium_term",
            limit=0
        )


# 2. Test _get_top_items_data raises SpotifyDataServiceException if EndpointRequesterException occurs.
@pytest.mark.asyncio
async def test__get_top_items_data_raises_spotify_data_service_exception_if_endpoint_requester_exception_occurs(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterException()

    with pytest.raises(SpotifyDataServiceException, match="Failed to make request to Spotify API"):
        await spotify_data_service._get_top_items_data(
            access_token="",
            item_type=SpotifyItemType.TRACK,
            time_range="",
            limit=0
        )


# 3. Test _get_top_items_data raises KeyError if items key not present in data.
@pytest.mark.asyncio
async def test__get_top_items_data_raises_spotify_data_service_exception_if_items_not_in_data(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.return_value = {"not_items": []}

    with pytest.raises(SpotifyDataServiceException, match="No items key present in API data"):
        await spotify_data_service._get_top_items_data(
            access_token="access_token",
            item_type=SpotifyItemType.TRACK,
            time_range="medium_term",
            limit=0
        )


# 4. Test _get_top_items_data returns expected response.
@pytest.mark.asyncio
async def test__get_top_items_data_returns_expected_response(spotify_data_service, mock_endpoint_requester):
    mock_endpoint_requester.get.return_value = {"items": "response_items"}

    response = await spotify_data_service._get_top_items_data(
        access_token="access_token",
        item_type=SpotifyItemType.TRACK,
        time_range="medium_term",
        limit=0
    )

    assert response == "response_items"


# 5. Test get_top_artists calls expected methods
@pytest.mark.asyncio
async def test_get_top_artists_calls__get_top_items_data_with_expected_params(spotify_data_service, mock_artist_data):
    mock__get_top_items_data = AsyncMock()
    mock__get_top_items_data.return_value = [mock_artist_data]
    mock__create_artist = Mock()
    spotify_data_service._get_top_items_data = mock__get_top_items_data
    spotify_data_service._create_artist = mock__create_artist

    await spotify_data_service.get_top_artists(access_token="access_token", time_range="medium_term", limit=0)

    spotify_data_service._get_top_items_data.assert_called_once_with(
        access_token="access_token",
        item_type=SpotifyItemType.ARTIST,
        time_range="medium_term",
        limit=0
    )
    mock__create_artist.assert_called_once()


# 6. Test get_top_tracks calls expected methods.
@pytest.mark.asyncio
async def test_get_top_tracks_calls__get_top_items_data_with_expected_params(spotify_data_service, mock_track_data):
    mock__get_top_items_data = AsyncMock()
    mock__get_top_items_data.return_value = [mock_track_data]
    mock__create_track = Mock()
    spotify_data_service._get_top_items_data = mock__get_top_items_data
    spotify_data_service._create_track = mock__create_track

    await spotify_data_service.get_top_tracks(access_token="access_token", time_range="medium_term", limit=0)

    spotify_data_service._get_top_items_data.assert_called_once_with(
        access_token="access_token",
        item_type=SpotifyItemType.TRACK,
        time_range="medium_term",
        limit=0
    )
    mock__create_track.assert_called_once()
