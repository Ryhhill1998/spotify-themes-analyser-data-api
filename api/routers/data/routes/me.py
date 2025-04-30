from enum import Enum
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import Field

from api.dependencies import SpotifyDataServiceDependency, InsightsServiceDependency
from api.models.models import SpotifyProfile, SpotifyArtist, AccessToken
from api.services.insights_service import InsightsServiceException
from api.services.music.spotify_data_service import SpotifyDataServiceException, SpotifyDataServiceUnauthorisedException

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
    try:
        profile_data = await spotify_data_service.get_profile_data(access_token.access_token)
        return profile_data
    except SpotifyDataServiceUnauthorisedException as e:
        error_message = "Invalid access token"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_message)


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
    time_range : TimeRange
        The time range to retrieve the top artists for.
    limit : int
        Limit to specify the number of top artists to retrieve (default is 50, must be at least 10 but no more than 50).

    Returns
    -------
    JSONResponse
        A JSON response containing a list of top artists with updated token cookies.

    Raises
    ------
    HTTPException
        Raised with a 500 Internal Server Error status code if another exception occurs while retrieving the user's top
        artists from Spotify.
    """

    try:
        top_artists = await spotify_data_service.get_top_artists(
            access_token=access_token.access_token,
            time_range=time_range,
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


@router.post("/top/tracks")
async def get_top_tracks(
        access_token: AccessToken,
        spotify_data_service: SpotifyDataServiceDependency,
        time_range: TimeRange,
        limit: Annotated[int, Field(ge=10, le=50)] = 50
) -> JSONResponse:
    """
    Retrieves the user's top tracks from Spotify.

    Parameters
    ----------
    time_range : TimeRange
        The time range to retrieve the top tracks for.
    limit : int
        Limit to specify the number of top tracks to retrieve (default is 50, must be at least 10 but no more than 50).

    Returns
    -------
    JSONResponse
        A JSON response containing a list of top tracks with updated token cookies.

    Raises
    ------
    HTTPException
        Raised with a 500 Internal Server Error status code if another exception occurs while retrieving the user's top
        tracks from Spotify.
    """

    try:
        top_tracks = await spotify_data_service.get_top_tracks(
            access_token=access_token.access_token,
            time_range=time_range,
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


@router.post("/top/genres")
async def get_top_genres(
        access_token: AccessToken,
        spotify_data_service: SpotifyDataServiceDependency,
        time_range: TimeRange,
        limit: Annotated[int, Field(ge=1)] = 5
):
    try:
        top_genres = await spotify_data_service.get_top_genres(
            access_token=access_token.access_token,
            time_range=time_range,
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


@router.post("/top/emotions")
async def get_top_emotions(
        access_token: AccessToken,
        insights_service: InsightsServiceDependency,
        time_range: TimeRange,
        limit: Annotated[int, Field(ge=1, le=15)] = 5
) -> JSONResponse:
    """
    Retrieves the user's top emotional responses based on their music listening history.

    Parameters
    ----------
    insights_service : InsightsServiceDependency
        Dependency for analyzing and retrieving the top emotions in the user's Spotify listening history.

    Returns
    -------
    JSONResponse
        A JSON response containing a list of top emotional responses with updated token cookies.

    Raises
    ------
    HTTPException
        Raised with a 500 Internal Server Error status code if an exception occurs while computing the user's top
        emotions.
    """

    try:
        top_emotions = await insights_service.get_top_emotions(
            access_token=access_token.access_token,
            time_range=time_range,
            limit=limit
        )
        return top_emotions
    except InsightsServiceException as e:
        error_message = "Failed to retrieve the user's top emotions"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
