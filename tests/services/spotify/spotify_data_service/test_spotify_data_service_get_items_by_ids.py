from unittest.mock import AsyncMock, Mock

import pytest

from api.services.endpoint_requester import EndpointRequesterUnauthorisedException, EndpointRequesterException
from api.services.spotify.spotify_data_service import SpotifyDataServiceUnauthorisedException, SpotifyItemType, \
    SpotifyDataServiceException


# 1. Test _get_items_data_by_ids raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
# 2. Test _get_items_data_by_ids raises SpotifyDataServiceException if EndpointRequesterException occurs.
# 3. Test _get_items_data_by_ids raises SpotifyDataServiceException if API data missing expected key.
# 4. Test _get_items_data_by_ids calls endpoint_requester.get with expected params.
# 5. Test _get_items_data_by_ids returns expected data.
# 6. Test get_artists_by_ids calls expected methods.
# 7. Test get_tracks_by_ids calls expected methods.


# 1. Test _get_items_data_by_ids raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
@pytest.mark.asyncio
async def test__get_items_data_by_ids_raises_spotify_data_service_unauthorised_exception_if_endpoint_requester_unauthorised_exception_occurs(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterUnauthorisedException()

    with pytest.raises(SpotifyDataServiceUnauthorisedException, match="Invalid Spotify API access token"):
        await spotify_data_service._get_items_data_by_ids(
            access_token="",
            item_ids=["1"],
            item_type=SpotifyItemType.TRACK
        )


# 2. Test _get_items_data_by_ids raises SpotifyDataServiceException if EndpointRequesterException occurs.
@pytest.mark.asyncio
async def test__get_items_data_by_ids_raises_spotify_data_service_exception_if_endpoint_requester_exception(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterException()

    with pytest.raises(SpotifyDataServiceException, match="Failed to make request to Spotify API"):
        await spotify_data_service._get_items_data_by_ids(
            access_token="",
            item_ids=["1"],
            item_type=SpotifyItemType.TRACK
        )


# 3. Test _get_items_data_by_ids raises SpotifyDataServiceException if API data missing expected key.


# 4. Test _get_items_data_by_ids calls endpoint_requester.get with expected params.
@pytest.mark.asyncio
async def test__get_items_data_by_ids_calls_endpoint_requester_get_method_with_expected_params(
        spotify_data_service,
        mock_endpoint_requester
):
    await spotify_data_service._get_items_data_by_ids(
        access_token="access",
        item_ids=["1", "2", "3"],
        item_type=SpotifyItemType.TRACK
    )

    mock_endpoint_requester.get.assert_called_once_with(
        url="http://test-url.com/tracks",
        headers={"Authorization": f"Bearer access"},
        params={"ids": "1,2,3"}
    )


# 5. Test _get_items_data_by_ids returns expected data.
@pytest.mark.asyncio
async def test__get_item_data_by_id_returns_expected_data(spotify_data_service, mock_endpoint_requester):
    mock_data = {"tracks": "test_value"}
    mock_endpoint_requester.get.return_value = mock_data

    data = await spotify_data_service._get_items_data_by_ids(
        access_token="",
        item_ids=["1"],
        item_type=SpotifyItemType.TRACK
    )

    assert data == "test_value"


# 6. Test get_artists_by_ids calls expected methods.
@pytest.mark.asyncio
async def test_get_artist_by_id_calls_expected_methods(spotify_data_service):
    mock__get_items_data_by_ids = AsyncMock()
    mock__get_items_data_by_ids.return_value = ["1", "2", "3"]
    mock__create_artist = Mock()
    spotify_data_service._get_items_data_by_ids = mock__get_items_data_by_ids
    spotify_data_service._create_artist = mock__create_artist

    await spotify_data_service.get_artists_by_ids(access_token="access", artist_ids=["1", "2", "3"])

    mock__get_items_data_by_ids.assert_called_once_with(
        access_token="access",
        item_ids=["1", "2", "3"],
        item_type=SpotifyItemType.ARTIST
    )
    assert mock__create_artist.call_count == 3


# 7. Test get_tracks_by_ids calls expected methods.
@pytest.mark.asyncio
async def test_get_tracks_by_ids_calls_expected_methods(spotify_data_service):
    mock__get_items_data_by_ids = AsyncMock()
    mock__get_items_data_by_ids.return_value = ["1", "2", "3"]
    mock__create_track = Mock()
    spotify_data_service._get_items_data_by_ids = mock__get_items_data_by_ids
    spotify_data_service._create_track = mock__create_track

    await spotify_data_service.get_tracks_by_ids(access_token="access", track_ids=["1", "2", "3"])

    mock__get_items_data_by_ids.assert_called_once_with(
        access_token="access",
        item_ids=["1", "2", "3"],
        item_type=SpotifyItemType.TRACK
    )
    assert mock__create_track.call_count == 3
