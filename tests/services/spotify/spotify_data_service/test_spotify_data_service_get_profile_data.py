from copy import deepcopy

import pytest

from api.models.models import SpotifyProfile, SpotifyImage
from api.services.endpoint_requester import EndpointRequesterUnauthorisedException, EndpointRequesterException
from api.services.spotify.spotify_data_service import SpotifyDataServiceException, \
    SpotifyDataServiceUnauthorisedException


# 1. Test get_profile_data raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
# 2. Test get_profile_data raises SpotifyDataServiceException if EndpointRequesterException occurs.
# 3. Test get_profile_data raises SpotifyDataServiceException if API data is invalid.
# 4. Test get_profile_data does not raise exception if email is missing.
# 5. Test get_profile_data does not raise exception if email is None.
# 6. Test get_profile_data calls endpoint_requester.get with expected params.
# 7. Test get_profile_data returns expected SpotifyProfile.


# 1. Test get_profile_data raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
@pytest.mark.asyncio
async def test_get_profile_data_raises_spotify_data_service_unauthorised_exception_if_endpoint_requester_unauthorised_exception_occurs(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterUnauthorisedException()

    with pytest.raises(SpotifyDataServiceUnauthorisedException) as e:
        await spotify_data_service.get_profile_data("")

    assert "Invalid Spotify API access token" in str(e.value)

# 2. Test get_profile_data raises SpotifyDataServiceException if EndpointRequesterException occurs.
@pytest.mark.asyncio
async def test_get_profile_data_raises_spotify_data_service_exception_if_endpoint_requester_exception_occurs(
        spotify_data_service,
        mock_endpoint_requester
):
    mock_endpoint_requester.get.side_effect = EndpointRequesterException()

    with pytest.raises(SpotifyDataServiceException) as e:
        await spotify_data_service.get_profile_data("")

    assert "Failed to make request to Spotify API" in str(e.value)


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


@pytest.fixture
def mock_profile_data() -> dict:
    return {
        "id": "1",
        "display_name": "display_name",
        "email": "email",
        "href": "href",
        "images": [{"height": 100, "width": 100, "url": "image_url"}],
        "followers": {
            "total": 0
        },
    }


# 3. Test get_profile_data raises SpotifyDataServiceException if API data is invalid.
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "missing_field",
    [
        "id",
        "display_name",
        "href",
        "images",
        "images.[].height",
        "images.[].width",
        "images.[].url",
        "followers",
        "followers.total"
    ]
)
async def test_get_profile_data_raises_spotify_data_service_exception_if_api_data_invalid(
        spotify_data_service,
        mock_endpoint_requester,
        mock_profile_data,
        missing_field
):
    data, deleted_field = delete_field(data=mock_profile_data, field=missing_field)
    mock_endpoint_requester.get.return_value = data

    with pytest.raises(SpotifyDataServiceException) as e:
        await spotify_data_service.get_profile_data("")

    assert "Spotify API data validation failed" in str(e.value) and deleted_field in str(e.value)


# 4. Test get_profile_data does not raise exception if email is missing.
@pytest.mark.asyncio
async def test_get_profile_data_does_not_raise_exception_if_email_is_missing(
        spotify_data_service,
        mock_endpoint_requester,
        mock_profile_data
):
    data, deleted_field = delete_field(data=mock_profile_data, field="email")
    mock_endpoint_requester.get.return_value = data

    await spotify_data_service.get_profile_data("")


# 5. Test get_profile_data does not raise exception if email is None.
@pytest.mark.asyncio
async def test_get_profile_data_does_not_raise_exception_if_email_is_none(
        spotify_data_service,
        mock_endpoint_requester,
        mock_profile_data
):
    mock_profile_data["email"] = None
    mock_endpoint_requester.get.return_value = mock_profile_data

    await spotify_data_service.get_profile_data("")


# 6. Test get_profile_data calls endpoint_requester.get with expected params.
@pytest.mark.asyncio
async def test_get_profile_data_calls_endpoint_requester_get_with_expected_params(
        spotify_data_service,
        mock_endpoint_requester,
        mock_profile_data
):
    mock_endpoint_requester.get.return_value = mock_profile_data

    await spotify_data_service.get_profile_data("access")

    mock_endpoint_requester.get.assert_called_once_with(
        url="http://test-url.com/me",
        headers = {"Authorization": "Bearer access"}
    )


# 7. Test get_profile_data returns expected SpotifyProfile.
@pytest.mark.asyncio
async def test_get_profile_data_returns_expected_spotify_profile(
        spotify_data_service,
        mock_endpoint_requester,
        mock_profile_data
):
    mock_endpoint_requester.get.return_value = mock_profile_data

    profile = await spotify_data_service.get_profile_data("access")

    expected_profile = SpotifyProfile(
        id="1",
        display_name="display_name",
        email="email",
        href="href",
        images=[SpotifyImage(height=100, width=100, url="image_url")],
        followers=0
    )
    assert profile == expected_profile
