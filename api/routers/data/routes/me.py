from enum import Enum
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from loguru import logger
from pydantic import Field

from api.dependencies import SpotifyDataServiceDependency, InsightsServiceDependency
from api.models.models import SpotifyProfile, SpotifyArtist, AccessToken, SpotifyTrack, TopGenre, TopEmotion
from api.services.insights_service import InsightsServiceException
from api.services.spotify.spotify_data_service import SpotifyDataServiceException, SpotifyDataServiceUnauthorisedException

router = APIRouter(prefix="/me")


class TimeRange(str, Enum):
    SHORT = "short_term"
    MEDIUM = "medium_term"
    LONG = "long_term"


@router.post("/profile", response_model=SpotifyProfile)
async def get_profile(
        access_token: AccessToken,
        spotify_data_service: SpotifyDataServiceDependency
) -> SpotifyProfile:
    """
    Retrieves the user's Spotify profile details (id, display_name, email, href, images, followers).

    Parameters
    ----------
    access_token : AccessToken
        The Spotify API access token of the signed-in user.
    spotify_data_service : SpotifyDataServiceDependency
        The object used to retrieve data from the Spotify API.

    Returns
    -------
    SpotifyProfile
        The Spotify profile data of the signed-in user.

    Raises
    ------
    HTTPException
        Raised with a 401 Unauthorised status code if the access token is invalid or expired.
        Raised with a 500 Internal Server Error status code if another exception occurs while retrieving the user's
        profile from Spotify.
    """

    try:
        profile_data = await spotify_data_service.get_user_profile(access_token.access_token)
        return profile_data
    except SpotifyDataServiceUnauthorisedException as e:
        error_message = "Invalid access token"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_message)
    except SpotifyDataServiceException as e:
        error_message = "Failed to retrieve the user's profile"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("/top/artists", response_model=list[SpotifyArtist])
async def get_top_artists(
        access_token: AccessToken,
        spotify_data_service: SpotifyDataServiceDependency,
        time_range: TimeRange,
        limit: Annotated[int, Field(ge=10, le=50)] = 50
) -> list[SpotifyArtist]:
    """
    Retrieves the user's top artists from Spotify.

    Parameters
    ----------
    access_token : AccessToken
        The Spotify API access token of the signed-in user.
    spotify_data_service : SpotifyDataServiceDependency
        The object used to retrieve data from the Spotify API.
    time_range : TimeRange
        The time range to retrieve the top artists for.
    limit : int
        Limit to specify the number of top artists to retrieve (default is 50, must be at least 10 but no more than 50).

    Returns
    -------
    list[SpotifyArtist]
        A list of the user's top artists.

    Raises
    ------
    HTTPException
        Raised with a 401 Unauthorised status code if the access token is invalid or expired.
        Raised with a 500 Internal Server Error status code if another exception occurs while retrieving the user's top
        artists from Spotify.
    """

    try:
        top_artists = await spotify_data_service.get_top_artists(
            access_token=access_token.access_token,
            time_range=time_range.value,
            limit=limit
        )
        return top_artists
    except SpotifyDataServiceUnauthorisedException as e:
        error_message = "Invalid access token"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_message)
    except SpotifyDataServiceException as e:
        error_message = "Failed to retrieve the user's top artists"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("/top/tracks", response_model=list[SpotifyTrack])
async def get_top_tracks(
        access_token: AccessToken,
        spotify_data_service: SpotifyDataServiceDependency,
        time_range: TimeRange,
        limit: Annotated[int, Field(ge=10, le=50)] = 50
) -> list[SpotifyTrack]:
    """
    Retrieves the user's top tracks from Spotify.

    Parameters
    ----------
    access_token : AccessToken
        The Spotify API access token of the signed-in user.
    spotify_data_service : SpotifyDataServiceDependency
        The object used to retrieve data from the Spotify API.
    time_range : TimeRange
        The time range to retrieve the top tracks for.
    limit : int
        Limit to specify the number of top tracks to retrieve (default is 50, must be at least 10 but no more than 50).

    Returns
    -------
    list[SpotifyTrack]
        A list of the user's top tracks.

    Raises
    ------
    HTTPException
        Raised with a 401 Unauthorised status code if the access token is invalid or expired.
        Raised with a 500 Internal Server Error status code if another exception occurs while retrieving the user's top
        tracks from Spotify.
    """

    try:
        top_tracks = await spotify_data_service.get_top_tracks(
            access_token=access_token.access_token,
            time_range=time_range.value,
            limit=limit
        )
        return top_tracks
    except SpotifyDataServiceUnauthorisedException as e:
        error_message = "Invalid access token"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_message)
    except SpotifyDataServiceException as e:
        error_message = "Failed to retrieve the user's top tracks"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("/top/genres", response_model=list[TopGenre])
async def get_top_genres(
        access_token: AccessToken,
        spotify_data_service: SpotifyDataServiceDependency,
        time_range: TimeRange,
        limit: Annotated[int, Field(ge=1)] = 10
) -> list[TopGenre]:
    """
    Retrieves the user's top genres from Spotify.

    Parameters
    ----------
    access_token : AccessToken
        The Spotify API access token of the signed-in user.
    spotify_data_service : SpotifyDataServiceDependency
        The object used to retrieve data from the Spotify API.
    time_range : TimeRange
        The time range to retrieve the top genres for.
    limit : int
        Limit to specify the number of top genres to retrieve (default is 10, must be at least 1).

    Returns
    -------
    list[TopGenre]
        A list of the user's top genres.

    Raises
    ------
    HTTPException
        Raised with a 401 Unauthorised status code if the access token is invalid or expired.
        Raised with a 500 Internal Server Error status code if another exception occurs while retrieving the user's top
        genres from Spotify.
    """

    try:
        top_genres = await spotify_data_service.get_top_genres(
            access_token=access_token.access_token,
            time_range=time_range.value,
            limit=limit
        )
        return top_genres
    except SpotifyDataServiceUnauthorisedException as e:
        error_message = "Invalid access token"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_message)
    except SpotifyDataServiceException as e:
        error_message = "Failed to retrieve the user's top genres"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("/top/emotions", response_model=list[TopEmotion])
async def get_top_emotions(
        access_token: AccessToken,
        insights_service: InsightsServiceDependency,
        time_range: TimeRange,
        limit: Annotated[int, Field(ge=1, le=15)] = 15
) -> list[TopEmotion]:
    """
    Retrieves the user's top emotions based on their Spotify listening history.

    Parameters
    ----------
    access_token : AccessToken
        The Spotify API access token of the signed-in user.
    insights_service : InsightsServiceDependency
        The object used to extract the top emotions from the user's Spotify listening history.
    time_range : TimeRange
        The time range to retrieve the top tracks for.
    limit : int
        Limit to specify the number of top tracks to retrieve (default is 5, must be at least 1 but no more than 15).

    Returns
    -------
    list[TopEmotion]
        A list of the user's top emotions.

    Raises
    ------
    HTTPException
        Raised with a 500 Internal Server Error status code if an exception occurs while computing the user's top
        emotions.
    """

    try:
        top_emotions = await insights_service.get_top_emotions(
            access_token=access_token.access_token,
            time_range=time_range.value,
            limit=limit
        )
        return top_emotions
    except InsightsServiceException as e:
        error_message = "Failed to retrieve the user's top emotions"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
