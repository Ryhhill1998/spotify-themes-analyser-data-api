from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger

from api.dependencies import SpotifyDataServiceDependency, InsightsServiceDependency
from api.models.models import Emotion, EmotionalTagsResponse, SpotifyTrack, AccessToken, RequestedItems
from api.services.insights_service import InsightsServiceException
from api.services.spotify.spotify_data_service import SpotifyDataServiceNotFoundException, SpotifyDataServiceException

router = APIRouter()


@router.post("/tracks/{track_id}", response_model=SpotifyTrack)
async def get_track_by_id(
        access_token: AccessToken,
        track_id: str,
        spotify_data_service: SpotifyDataServiceDependency
) -> SpotifyTrack:
    """
    Retrieves details about a specific track by its ID.

    Parameters
    ----------
    access_token : AccessToken
        The Spotify API access token of the signed-in user.
    track_id : str
        The Spotify track ID.
    spotify_data_service : SpotifyDataServiceDependency
        The object used to retrieve data from the Spotify API.

    Returns
    -------
    SpotifyTrack
        The requested track.

    Raises
    ------
    HTTPException
        Raised with a 404 Not Found status code if the requested Spotify track was not found.
        Raised with a 500 Internal Server Error status code if another exception occurs while retrieving the requested
        track from Spotify.
    """

    try:
        track = await spotify_data_service.get_track_by_id(access_token=access_token.access_token, track_id=track_id)
        return track
    except SpotifyDataServiceNotFoundException as e:
        error_message = "Could not find the requested track"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)
    except SpotifyDataServiceException as e:
        error_message = "Failed to retrieve the requested track"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
    
    
@router.post("/tracks", response_model=list[SpotifyTrack])
async def get_several_tracks_by_ids(
        access_token: AccessToken,
        requested_tracks: RequestedItems,
        spotify_data_service: SpotifyDataServiceDependency
) -> list[SpotifyTrack]:
    """
    Retrieves details about a specific track by their ID.

    Parameters
    ----------
    access_token : AccessToken
        The Spotify API access token of the signed-in user.
    requested_tracks : RequestedItems
        The requested tracks IDs.
    spotify_data_service : SpotifyDataServiceDependency
        The object used to retrieve data from the Spotify API.

    Returns
    -------
    list[SpotifyTrack]
        The list of requested tracks.

    Raises
    ------
    HTTPException
        Raised with a 404 Not Found status code if the requested Spotify tracks were not found.
        Raised with a 500 Internal Server Error status code if another exception occurs while retrieving the requested
        tracks from Spotify.
    """

    try:
        tracks = await spotify_data_service.get_tracks_by_ids(
            access_token=access_token.access_token,
            track_ids=requested_tracks.ids
        )
        return tracks
    except SpotifyDataServiceNotFoundException as e:
        error_message = "Could not find the requested tracks"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_message)
    except SpotifyDataServiceException as e:
        error_message = "Failed to retrieve the requested tracks"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("/tracks/{track_id}/lyrics/emotional-tags/{emotion}", response_model=EmotionalTagsResponse)
async def get_lyrics_tagged_with_emotion(
        access_token: AccessToken,
        track_id: str,
        emotion: Emotion,
        insights_service: InsightsServiceDependency
) -> EmotionalTagsResponse:
    """
    Retrieves the user's top emotional responses based on their spotify listening history.

    Parameters
    ----------
    access_token : AccessToken
        The Spotify API access token of the signed-in user.
    track_id : str
        The ID of the track being requested.
    emotion : Emotion
        The emotion requested to tag the lyrics with.
    insights_service : InsightsServiceDependency
        The object used to generate lyrics tagged with the requested emotion.

    Returns
    -------
    EmotionalTagsResponse
        The track_id, emotion and lyrics tagged with the requested emotion.

    Raises
    ------
    HTTPException
        Raised with a 500 Internal Server Error status code if an exception occurs while computing the user's top
        emotions.
    """

    try:
        tagged_lyrics_response = await insights_service.tag_lyrics_with_emotion(
            access_token=access_token.access_token,
            track_id=track_id,
            emotion=emotion
        )
        return tagged_lyrics_response
    except InsightsServiceException as e:
        error_message = "Failed to tag lyrics with requested emotion"
        logger.error(f"{error_message} - {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
