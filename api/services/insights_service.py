from collections import defaultdict

from loguru import logger

from api.models.models import LyricsRequest, TopEmotion, EmotionalProfileResponse, EmotionalProfileRequest, \
    EmotionalTagsRequest, Emotion, EmotionalTagsResponse
from api.services.analysis_service import AnalysisService, AnalysisServiceException
from api.services.lyrics_service import LyricsService, LyricsServiceException
from api.services.spotify.spotify_data_service import SpotifyDataService, SpotifyDataServiceException


class InsightsServiceException(Exception):
    """
    Exception raised when InsightsService fails to process the responses from the services.

    Parameters
    ----------
    message : str
        The error message describing the failure.
    """

    def __init__(self, message):
        super().__init__(message)


class InsightsService:
    """
    A service for analyzing emotional content in a user's top tracks.

    This service orchestrates the retrieval of top tracks from Spotify,
    fetching their lyrics, analyzing the lyrics for emotional content,
    and providing insights into the user's emotional listening patterns.

    Methods
    -------
    get_top_emotions(access_token: str, time_range: str, limit: int) -> list[TopEmotion]
        Retrieves the top emotions detected in a user's top Spotify tracks.
    tag_lyrics_with_emotion(access_token: str, track_id: str, emotion: Emotion) -> EmotionalTagsResponse
        Retrieves emotional tags for a given track's lyrics based on the specified emotion.
    """

    def __init__(
            self,
            spotify_data_service: SpotifyDataService,
            lyrics_service: LyricsService,
            analysis_service: AnalysisService
    ):
        """
        Parameters
        ----------
        spotify_data_service : SpotifyDataService
            An instance of `SpotifyDataService` used to retrieve a user's top tracks.
        lyrics_service : LyricsService
            An instance of `LyricsService` used to fetch lyrics for songs.
        analysis_service : AnalysisService
            An instance of `AnalysisService` used to analyze song lyrics for emotional content.
        """

        self.spotify_data_service = spotify_data_service
        self.lyrics_service = lyrics_service
        self.analysis_service = analysis_service

    @staticmethod
    def _aggregate_emotions(emotional_analyses: list[EmotionalProfileResponse]) -> dict:
        """
        Aggregates emotional analysis results across multiple songs.

        This method sums up emotion percentages and tracks the song with the highest percentage for each emotion.

        Parameters
        ----------
        emotional_analyses : list[EmotionalProfileResponse]
            A list of `EmotionalProfile` objects containing emotional analysis results.

        Returns
        -------
        dict
            A dictionary where keys are emotion names, and values contain total emotion percentages and the track with
            the highest percentage for that emotion.
        """

        total_emotions = defaultdict(lambda: {"total": 0, "max_track": {"track_id": None, "percentage": 0}})

        for analysis in emotional_analyses:
            track_id = analysis.track_id
            emotional_profile = analysis.emotional_profile

            for emotion, percentage in emotional_profile.model_dump().items():
                total_emotions[emotion]["total"] += percentage

                if percentage > total_emotions[emotion]["max_track"]["percentage"]:
                    total_emotions[emotion]["max_track"] = {"track_id": track_id, "percentage": percentage}

        return total_emotions

    @staticmethod
    def _get_average_emotions(total_emotions: dict, result_count: int) -> list[TopEmotion]:
        """
        Computes the average percentage for each emotion across all analyzed tracks.

        Parameters
        ----------
        total_emotions : dict
            A dictionary containing total emotion percentages and the highest contributing track.
        result_count : int
            The total number of tracks analyzed.

        Returns
        -------
        list[TopEmotion]
            A list of `TopEmotion` objects representing the averaged emotional profile.

        Raises
        ------
        KeyError
            If total_emotions dict does not contain the required keys.
        ZeroDivisionError
            If results_count == 0.
        pydantic.ValidationError
            If creating TopEmotion objects fails.
        """

        average_emotions = []

        for emotion, info in total_emotions.items():
            avg_percentage = round(info["total"] / result_count, 2)
            track_id = None if avg_percentage == 0 else info["max_track"]["track_id"]
            average_emotions.append(TopEmotion(name=emotion, percentage=avg_percentage, track_id=track_id))

        return average_emotions

    def _process_emotions(self, emotional_profiles: list[EmotionalProfileResponse]) -> list[TopEmotion]:
        """
        Processes the emotional profiles of the tracks and returns the top emotions.

        Parameters
        ----------
        emotional_profiles : list of EmotionalProfileResponse
            A list of `EmotionalProfileResponse` objects representing the emotional profiles of the tracks.

        Returns
        -------
        list
            A list of `TopEmotion` objects representing the top emotions detected in the tracks, sorted by their
            average percentage.
        """

        total_emotions = self._aggregate_emotions(emotional_profiles)
        average_emotions = self._get_average_emotions(
            total_emotions=total_emotions,
            result_count=len(emotional_profiles)
        )
        top_emotions = sorted(average_emotions, key=lambda emotion: emotion.percentage, reverse=True)
        return top_emotions

    async def get_top_emotions(self, access_token: str, time_range: str) -> list[TopEmotion]:
        """
        Retrieves the top emotions detected in a user's top Spotify tracks.

        This method fetches a user's top tracks from Spotify, retrieves lyrics for each track,
        performs emotional analysis, and returns the most prominent emotions.

        Parameters
        ----------
        access_token : str
            The token string used to retrieve the user's Spotify data from the SpotifyDataService.
        time_range : str
            The time range to retrieve the user's top emotions for.

        Returns
        -------
        list[TopEmotion]
            The list of the user's top emotions identified in their Spotify listening history.

        Raises
        ------
        InsightsServiceException
            If any of the dependency services fail.
        """

        try:
            # get top tracks and refreshed tokens (if expired)
            top_tracks = await self.spotify_data_service.get_top_tracks(
                access_token=access_token,
                time_range=time_range,
                limit=30
            )
            if not top_tracks:
                logger.info("No top tracks found. Cannot proceed further with analysis.")
                return []

            # get lyrics for each track
            lyrics_requests = [
                LyricsRequest(
                    track_id=entry.id,
                    artist_name=entry.artist.name,
                    track_title=entry.name
                )
                for entry
                in top_tracks
            ]
            lyrics_list = await self.lyrics_service.get_lyrics_list(lyrics_requests)
            if not lyrics_list:
                logger.info("No lyrics found. Cannot proceed further with analysis.")
                return []

            # get emotional profiles for each set of lyrics
            emotional_profile_requests = [
                EmotionalProfileRequest(
                    track_id=entry.track_id,
                    lyrics=entry.lyrics
                )
                for entry
                in lyrics_list
            ]
            emotional_profiles = await self.analysis_service.get_emotional_profiles(emotional_profile_requests)
            if not emotional_profiles:
                logger.info("No emotional profiles found. Cannot proceed further with analysis.")
                return []

            # get top emotions from all emotional profiles
            top_emotions = self._process_emotions(emotional_profiles=emotional_profiles)

            return top_emotions
        except (SpotifyDataServiceException, LyricsServiceException, AnalysisServiceException) as e:
            error_message = f"Service failure - {e}"
            logger.error(error_message)
            raise InsightsServiceException(error_message)

    async def tag_lyrics_with_emotion(
            self,
            access_token: str,
            track_id: str,
            emotion: Emotion
    ) -> EmotionalTagsResponse:
        """
        Retrieves emotional tags for a given track's lyrics based on the specified emotion.

        Parameters
        ----------
        access_token : str
            The token string used to retrieve the user's Spotify data from the SpotifyDataService.
        track_id : str
            The ID of the track being analyzed.
        emotion : Emotion
            The emotion for which tagged lyrics are requested.

        Returns
        -------
        EmotionalTagsResponse
            A response object containing the track's lyrics with emotional tags.

        Raises
        ------
        InsightsServiceException
            If any of the dependency services fail.
        """

        try:
            track = await self.spotify_data_service.get_track_by_id(
                access_token=access_token,
                track_id=track_id
            )

            lyrics_request = LyricsRequest(track_id=track.id, artist_name=track.artist.name, track_title=track.name)
            lyrics_response = await self.lyrics_service.get_lyrics(lyrics_request)

            emotional_tags_request = EmotionalTagsRequest(
                track_id=track_id,
                emotion=emotion,
                lyrics=lyrics_response.lyrics
            )
            emotional_tags_response = await self.analysis_service.get_emotional_tags(emotional_tags_request)

            return emotional_tags_response
        except (SpotifyDataServiceException, LyricsServiceException, AnalysisServiceException) as e:
            error_message = f"Service failure - {e}"
            logger.error(error_message)
            raise InsightsServiceException(error_message)
