import pytest

from api.models.models import SpotifyTrack, SpotifyTrackArtist, SpotifyImage, SpotifyArtist
from api.services.endpoint_requester import EndpointRequesterException, EndpointRequesterUnauthorisedException, \
    EndpointRequesterNotFoundException
from api.services.spotify.spotify_auth_service import SpotifyAuthServiceException
from api.services.spotify.spotify_data_service import SpotifyDataServiceException, SpotifyItemType, \
    SpotifyDataServiceNotFoundException, SpotifyDataServiceUnauthorisedException

TEST_URL = "http://test-url.com"

# 1. Test _get_item_by_id raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
# 2. Test _get_item_by_id raises SpotifyDataServiceNotFoundException if EndpointRequesterNotFoundException occurs.
# 3. Test _get_item_by_id raises SpotifyDataServiceException if EndpointRequesterException occurs.
# 4. Test _get_item_by_id calls endpoint_requester.get with expected params.
# 5. Test _get_item_by_id returns expected data.
# 6. Test get_artist_by_id raises


# 1. Test get_item_by_id raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
@pytest.mark.asyncio
async def test_get_item_by_id_raises_spotify_data_service_unauthorised_exception_if_endpoint_requester_unauthorised_exception_occurs(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterUnauthorisedException()

    with pytest.raises(SpotifyDataServiceUnauthorisedException, match="Invalid Spotify API access token"):
        await spotify_data_service._get_item_by_id(access_token="", item_id="1", item_type=SpotifyItemType.TRACK)


# 2. Test get_item_by_id raises SpotifyDataServiceNotFoundException if EndpointRequesterNotFoundException occurs.
@pytest.mark.asyncio
async def test_get_item_by_id_item_not_found(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterNotFoundException()

    with pytest.raises(
            SpotifyDataServiceNotFoundException,
            match="Requested Spotify item not found. Item ID: 1, item type: artist"
    ):
        await spotify_data_service._get_item_by_id(access_token="", item_id="1", item_type=SpotifyItemType.ARTIST)


# 3. Test get_item_by_id raises SpotifyDataServiceException if EndpointRequesterException occurs.
@pytest.mark.asyncio
async def test_get_item_by_id_request_failure(spotify_data_service, mock_endpoint_requester, mock_request_tokens):
    mock_endpoint_requester.get.side_effect = EndpointRequesterException()

    with pytest.raises(SpotifyDataServiceException, match="Failed to make request to Spotify API"):
        await spotify_data_service._get_item_by_id(access_token="", item_id="1", item_type=SpotifyItemType.ARTIST)


# 4. Test get_item_by_id calls endpoint_requester.get with expected params.


# 5. Test get_item_by_id returns expected data.
