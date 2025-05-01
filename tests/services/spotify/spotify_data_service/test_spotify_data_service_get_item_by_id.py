import pytest

from api.models.models import SpotifyTrack, SpotifyTrackArtist, SpotifyImage, SpotifyArtist
from api.services.endpoint_requester import EndpointRequesterException, EndpointRequesterUnauthorisedException, \
    EndpointRequesterNotFoundException
from api.services.spotify.spotify_auth_service import SpotifyAuthServiceException
from api.services.spotify.spotify_data_service import SpotifyDataServiceException, SpotifyItemType, \
    SpotifyDataServiceNotFoundException

TEST_URL = "http://test-url.com"

# 1. Test _get_item_by_id raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
# 2. Test _get_item_by_id raises SpotifyDataServiceNotFoundException if EndpointRequesterNotFoundException occurs.
# 3. Test _get_item_by_id raises SpotifyDataServiceException if EndpointRequesterException occurs.
# 4. Test _get_item_by_id calls endpoint_requester.get with expected params.
# 5. Test _get_item_by_id returns expected data.
# 6. Test get_artist_by_id raises


# 1. Test get_item_by_id raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
@pytest.mark.asyncio
async def test_get_item_by_id_unauthorised_request(
        spotify_data_service,
        mock_endpoint_requester,
        mock_spotify_auth_service,
        mock_request_tokens
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterUnauthorisedException()
    mock_spotify_auth_service.refresh_tokens.return_value = mock_request_tokens

    with pytest.raises(SpotifyDataServiceException, match="Request to Spotify API failed"):
        await spotify_data_service._get_item_by_id(item_id="1", tokens=mock_request_tokens, item_type=SpotifyItemType.TRACKS)

    mock_spotify_auth_service.refresh_tokens.assert_called_once_with(mock_request_tokens.refresh_token)


# 2. Test get_item_by_id raises SpotifyDataServiceNotFoundException if EndpointRequesterNotFoundException occurs.
@pytest.mark.parametrize("item_type", [SpotifyItemType.TRACKS, SpotifyItemType.ARTISTS])
@pytest.mark.asyncio
async def test_get_item_by_id_item_not_found(
        spotify_data_service,
        mock_endpoint_requester,
        mock_request_tokens,
        item_type
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterNotFoundException()

    with pytest.raises(SpotifyDataServiceNotFoundException, match="Requested item not found"):
        await spotify_data_service._get_item_by_id(item_id="1", tokens=mock_request_tokens, item_type=item_type)


# 3. Test get_item_by_id raises SpotifyDataServiceException if EndpointRequesterException occurs.
@pytest.mark.asyncio
async def test_get_item_by_id_request_failure(spotify_data_service, mock_endpoint_requester, mock_request_tokens):
    mock_endpoint_requester.get.side_effect = EndpointRequesterException()

    with pytest.raises(SpotifyDataServiceException, match="Request to Spotify API failed"):
        await spotify_data_service._get_item_by_id(item_id="1", tokens=mock_request_tokens, item_type=SpotifyItemType.TRACKS)


# 4. Test get_item_by_id calls endpoint_requester.get with expected params.


# 5. Test get_item_by_id returns expected data.
