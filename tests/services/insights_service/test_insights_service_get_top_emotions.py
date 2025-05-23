from unittest.mock import Mock

import pytest

from api.models.models import LyricsResponse, EmotionalProfileResponse, EmotionalProfile, TopEmotion, LyricsRequest, \
    EmotionalProfileRequest
from api.services.analysis_service import AnalysisServiceException
from api.services.insights_service import InsightsServiceException
from api.services.lyrics_service import LyricsServiceException
from api.services.spotify.spotify_data_service import SpotifyDataServiceException

# 1. Test get_top_emotions raises InsightsServiceException if SpotifyDataServiceException occurs.
# 2. Test get_top_emotions raises InsightsServiceException if LyricsServiceException occurs.
# 3. Test get_top_emotions raises InsightsServiceException if AnalysisServiceException occurs.
# 4. Test get_top_emotions raises InsightsServiceException if top_tracks is empty.
# 5. Test get_top_emotions raises InsightsServiceException if lyrics_list is empty.
# 6. Test get_top_emotions raises InsightsServiceException if emotional_profiles is empty.
# 7. Test get_top_emotions returns expected top emotions.


@pytest.fixture
def mock_lyrics_list(mock_lyrics_response_factory) -> list[LyricsResponse]:
    return [mock_lyrics_response_factory(str(i)) for i in range(1, 6)]


@pytest.fixture
def mock_emotional_profile_factory():
    def _create(
            track_id: str,
            joy: float,
            sadness: float,
            anger: float,
            fear: float,
            love: float,
            hope: float,
            nostalgia: float,
            loneliness: float,
            confidence: float,
            despair: float,
            excitement: float,
            mystery: float,
            defiance: float,
            gratitude: float,
            spirituality: float
    ) -> EmotionalProfileResponse:
        return EmotionalProfileResponse(
            track_id=track_id,
            lyrics="lyrics",
            emotional_profile=EmotionalProfile(
                joy=joy,
                sadness=sadness,
                anger=anger,
                fear=fear,
                love=love,
                hope=hope,
                nostalgia=nostalgia,
                loneliness=loneliness,
                confidence=confidence,
                despair=despair,
                excitement=excitement,
                mystery=mystery,
                defiance=defiance,
                gratitude=gratitude,
                spirituality=spirituality
            )
        )

    return _create


@pytest.fixture
def mock_emotional_profiles(mock_emotional_profile_factory) -> list[EmotionalProfileResponse]:
    return [
        mock_emotional_profile_factory(
            track_id="1",
            joy=0.2,
            sadness=0.1,
            anger=0.05,
            fear=0,
            love=0,
            hope=0.05,
            nostalgia=0.04,
            loneliness=0.02,
            confidence=0.02,
            despair=0,
            excitement=0.01,
            mystery=0.01,
            defiance=0.2,
            gratitude=0.15,
            spirituality=0.15
        ),
        mock_emotional_profile_factory(
            track_id="2",
            joy=0,
            sadness=0.15,
            anger=0.05,
            fear=0,
            love=0,
            hope=0.05,
            nostalgia=0.24,
            loneliness=0.02,
            confidence=0.02,
            despair=0,
            excitement=0.01,
            mystery=0.06,
            defiance=0.3,
            gratitude=0,
            spirituality=0.1
        )
    ]


# 1. Test that get_top_emotions raises InsightsServiceException if SpotifyDataServiceException occurs.
@pytest.mark.asyncio
async def test_get_top_emotions_raises_insights_service_exception_if_spotify_data_service_exception_occurs(
        insights_service,
        mock_spotify_data_service
):
    exception_message = "Test SpotifyDataService failure"
    mock_spotify_data_service.get_top_tracks.side_effect = SpotifyDataServiceException(exception_message)

    with pytest.raises(InsightsServiceException, match="Service failure") as e:
        await insights_service.get_top_emotions(access_token="", time_range="short_term")

    assert exception_message in str(e.value)


# 2. Test that get_top_emotions raises InsightsServiceException if LyricsServiceException occurs.
@pytest.mark.asyncio
async def test_get_top_emotions_raises_insights_service_exception_if_lyrics_service_exception_occurs(
        insights_service,
        mock_spotify_data_service,
        mock_lyrics_service
):
    mock_spotify_data_service.get_top_tracks.return_value = []
    insights_service._check_data_not_empty = Mock()
    exception_message = "Test LyricsService failure"
    mock_lyrics_service.get_lyrics_list.side_effect = LyricsServiceException(exception_message)

    with pytest.raises(InsightsServiceException, match="Service failure") as e:
        await insights_service.get_top_emotions(access_token="", time_range="short_term")

    assert exception_message in str(e)


# 3. Test that get_top_emotions raises InsightsServiceException if AnalysisServiceException occurs.
@pytest.mark.asyncio
async def test_get_top_emotions_raises_insights_service_exception_if_analysis_service_exception_occurs(
        insights_service,
        mock_spotify_data_service,
        mock_lyrics_service,
        mock_analysis_service
):
    mock_spotify_data_service.get_top_tracks.return_value = []
    mock_lyrics_service.get_lyrics_list.return_value = []
    insights_service._check_data_not_empty = Mock()
    exception_message = "Test AnalysisService failure"
    mock_analysis_service.get_emotional_profiles.side_effect = AnalysisServiceException(exception_message)

    with pytest.raises(InsightsServiceException, match="Service failure") as e:
        await insights_service.get_top_emotions(access_token="", time_range="short_term")

    assert exception_message in str(e)


# 4. Test that get_top_emotions raises InsightsServiceException if top_tracks is empty.
@pytest.mark.asyncio
async def test_get_top_items_raises_insights_service_exception_if_top_tracks_empty(
        insights_service,
        mock_spotify_data_service
):
    mock_spotify_data_service.get_top_tracks.return_value = []

    with pytest.raises(InsightsServiceException, match="No top tracks found. Cannot proceed further with analysis."):
        await insights_service.get_top_emotions(access_token="", time_range="short_term")


# 5. Test that get_top_emotions raises InsightsServiceException if lyrics_list is empty.
@pytest.mark.asyncio
async def test_get_top_items_raises_insights_service_exception_if_lyrics_list_empty(
        insights_service,
        mock_spotify_data_service,
        mock_spotify_tracks,
        mock_lyrics_service
):
    mock_spotify_data_service.get_top_tracks.return_value = mock_spotify_tracks
    mock_lyrics_service.get_lyrics_list.return_value = []

    with pytest.raises(InsightsServiceException, match="No lyrics found. Cannot proceed further with analysis."):
        await insights_service.get_top_emotions(access_token="", time_range="short_term")


# 6. Test that get_top_emotions raises InsightsServiceException if emotional_profiles is empty.
@pytest.mark.asyncio
async def test_get_top_items_raises_insights_service_exception_if_emotional_profiles_empty(
        insights_service,
        mock_spotify_data_service,
        mock_spotify_tracks,
        mock_lyrics_service,
        mock_lyrics_list,
        mock_analysis_service
):
    mock_spotify_data_service.get_top_tracks.return_value = mock_spotify_tracks
    mock_lyrics_service.get_lyrics_list.return_value = mock_lyrics_list
    mock_analysis_service.get_emotional_profiles.return_value = []

    with pytest.raises(
            InsightsServiceException,
            match="No emotional profiles found. Cannot proceed further with analysis."
    ):
        await insights_service.get_top_emotions(access_token="", time_range="short_term")

# 7. Test get_top_emotions returns expected top emotions.
@pytest.mark.asyncio
async def test_get_top_emotions_returns_expected_top_emotions(
        insights_service,
        mock_spotify_data_service,
        mock_spotify_tracks,
        mock_lyrics_service,
        mock_lyrics_list,
        mock_analysis_service,
        mock_emotional_profiles
):
    access_token = "access"
    time_range = "short_term"
    mock_spotify_data_service.get_top_tracks.return_value = mock_spotify_tracks
    mock_lyrics_service.get_lyrics_list.return_value = mock_lyrics_list
    mock_analysis_service.get_emotional_profiles.return_value = mock_emotional_profiles

    top_emotions = await insights_service.get_top_emotions(
        access_token=access_token,
        time_range=time_range
    )

    expected_top_emotions = [
        TopEmotion(name="defiance", percentage=0.25, track_id="2"),
        TopEmotion(name="nostalgia", percentage=0.14, track_id="2"),
        TopEmotion(name="sadness", percentage=0.12, track_id="2"),
        TopEmotion(name="spirituality", percentage=0.12, track_id="1"),
        TopEmotion(name="joy", percentage=0.1, track_id="1"),
        TopEmotion(name="gratitude", percentage=0.07, track_id="1"),
        TopEmotion(name="anger", percentage=0.05, track_id="1"),
        TopEmotion(name="hope", percentage=0.05, track_id="1"),
        TopEmotion(name="mystery", percentage=0.03, track_id="2"),
        TopEmotion(name="loneliness", percentage=0.02, track_id="1"),
        TopEmotion(name="confidence", percentage=0.02, track_id="1"),
        TopEmotion(name="excitement", percentage=0.01, track_id="1")
    ]
    assert top_emotions == expected_top_emotions
    mock_spotify_data_service.get_top_tracks.assert_called_once_with(
        access_token=access_token,
        time_range=time_range,
        limit=30
    )
    lyrics_requests = [
        LyricsRequest(track_id="1", artist_name="artist_name", track_title="track_name"),
        LyricsRequest(track_id="2", artist_name="artist_name", track_title="track_name"),
        LyricsRequest(track_id="3", artist_name="artist_name", track_title="track_name"),
        LyricsRequest(track_id="4", artist_name="artist_name", track_title="track_name"),
        LyricsRequest(track_id="5", artist_name="artist_name", track_title="track_name")
    ]
    mock_lyrics_service.get_lyrics_list.assert_called_once_with(lyrics_requests)
    emotional_profile_requests = [
        EmotionalProfileRequest(track_id="1", lyrics="lyrics"),
        EmotionalProfileRequest(track_id="2", lyrics="lyrics"),
        EmotionalProfileRequest(track_id="3", lyrics="lyrics"),
        EmotionalProfileRequest(track_id="4", lyrics="lyrics"),
        EmotionalProfileRequest(track_id="5", lyrics="lyrics")
    ]
    mock_analysis_service.get_emotional_profiles.assert_called_once_with(emotional_profile_requests)
