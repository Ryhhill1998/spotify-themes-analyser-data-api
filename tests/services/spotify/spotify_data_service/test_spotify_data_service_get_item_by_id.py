from unittest.mock import Mock, AsyncMock

import pytest

from api.services.endpoint_requester import EndpointRequesterException, EndpointRequesterUnauthorisedException, \
    EndpointRequesterNotFoundException
from api.services.spotify.spotify_data_service import SpotifyDataServiceException, SpotifyItemType, \
    SpotifyDataServiceNotFoundException, SpotifyDataServiceUnauthorisedException

# 1. Test _get_item_data_by_id raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
# 2. Test _get_item_data_by_id raises SpotifyDataServiceNotFoundException if EndpointRequesterNotFoundException occurs.
# 3. Test _get_item_data_by_id raises SpotifyDataServiceException if EndpointRequesterException occurs.
# 4. Test _get_item_data_by_id calls endpoint_requester.get with expected params.
# 5. Test _get_item_data_by_id returns expected data.
# 6. Test get_artist_by_id calls expected methods.
# 7. Test get_track_by_id calls expected methods.


# 1. Test get_item_by_id raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
@pytest.mark.asyncio
async def test__get_item_data_by_id_raises_spotify_data_service_unauthorised_exception_if_endpoint_requester_unauthorised_exception_occurs(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterUnauthorisedException()

    with pytest.raises(SpotifyDataServiceUnauthorisedException, match="Invalid Spotify API access token"):
        await spotify_data_service._get_item_data_by_id(access_token="", item_id="1", item_type=SpotifyItemType.TRACK)


# 2. Test get_item_by_id raises SpotifyDataServiceNotFoundException if EndpointRequesterNotFoundException occurs.
@pytest.mark.asyncio
async def test__get_item_data_by_id_item_not_found(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterNotFoundException()

    with pytest.raises(
            SpotifyDataServiceNotFoundException,
            match="Requested Spotify item not found. Item ID: 1, item type: artist"
    ):
        await spotify_data_service._get_item_data_by_id(access_token="", item_id="1", item_type=SpotifyItemType.ARTIST)


# 3. Test get_item_by_id raises SpotifyDataServiceException if EndpointRequesterException occurs.
@pytest.mark.asyncio
async def test__get_item_data_by_id_raises_spotify_data_service_exception_if_endpoint_requester_exception(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterException()

    with pytest.raises(SpotifyDataServiceException, match="Failed to make request to Spotify API"):
        await spotify_data_service._get_item_data_by_id(access_token="", item_id="1", item_type=SpotifyItemType.ARTIST)


# 4. Test get_item_by_id calls endpoint_requester.get with expected params.
@pytest.mark.asyncio
async def test__get_item_data_by_id_calls_endpoint_requester_get_method_with_expected_params(
        spotify_data_service,
        mock_endpoint_requester
):
    await spotify_data_service._get_item_data_by_id(access_token="access", item_id="1", item_type=SpotifyItemType.ARTIST)

    mock_endpoint_requester.get.assert_called_once_with(
        url="http://test-url.com/artists/1",
        headers={"Authorization": f"Bearer access"}
    )


# 5. Test get_item_by_id returns expected data.
@pytest.mark.asyncio
async def test__get_item_data_by_id_returns_expected_data(spotify_data_service, mock_endpoint_requester):
    mock_data = {"test_key": "test_value"}
    mock_endpoint_requester.get.return_value = mock_data

    data = await spotify_data_service._get_item_data_by_id(
        access_token="access",
        item_id="1",
        item_type=SpotifyItemType.ARTIST
    )

    assert data == mock_data


# 6. Test get_artist_by_id calls expected methods.
@pytest.mark.asyncio
async def test_get_artist_by_id_calls_expected_methods(spotify_data_service):
    mock__get_item_data_by_id = AsyncMock()
    mock__create_artist = Mock()
    spotify_data_service._get_item_data_by_id = mock__get_item_data_by_id
    spotify_data_service._create_artist = mock__create_artist

    await spotify_data_service.get_artist_by_id(access_token="access", item_id="1")

    mock__get_item_data_by_id.assert_called_once_with(access_token="access", item_id="1", item_type=SpotifyItemType.ARTIST)
    mock__create_artist.assert_called_once()


# 7. Test get_track_by_id calls expected methods.
@pytest.mark.asyncio
async def test_get_track_by_id_calls_expected_methods(spotify_data_service):
    mock__get_item_data_by_id = AsyncMock()
    mock__create_track = Mock()
    spotify_data_service._get_item_data_by_id = mock__get_item_data_by_id
    spotify_data_service._create_track = mock__create_track

    await spotify_data_service.get_track_by_id(access_token="access", item_id="1")

    mock__get_item_data_by_id.assert_called_once_with(access_token="access", item_id="1", item_type=SpotifyItemType.TRACK)
    mock__create_track.assert_called_once()