import pytest

from api.models.models import EmotionalTagsResponse, Emotion, EmotionalTagsRequest, LyricsRequest
from api.services.analysis_service import AnalysisServiceException
from api.services.insights_service import InsightsServiceException
from api.services.lyrics_service import LyricsServiceException
from api.services.spotify.spotify_data_service import SpotifyDataServiceException

# 1. Test tag_lyrics_with_emotion raises InsightsServiceException if SpotifyDataServiceException occurs.
# 2. Test tag_lyrics_with_emotion raises InsightsServiceException if LyricsServiceException occurs.
# 3. Test tag_lyrics_with_emotion raises InsightsServiceException if AnalysisServiceException occurs.
# 4. Test tag_lyrics_with_emotion returns expected emotional tags response.


@pytest.fixture
def mock_analysis_data() -> EmotionalTagsResponse:
    return EmotionalTagsResponse(track_id="1", lyrics="lyrics", emotion=Emotion.SADNESS)


# 1. Test tag_lyrics_with_emotion raises InsightsServiceException if SpotifyDataServiceException occurs.
@pytest.mark.asyncio
async def test_tag_lyrics_raises_insights_service_exception_if_spotify_data_service_exception_occurs(
        insights_service,
        mock_spotify_data_service
):
    exception_message = "Test SpotifyDataService failure"
    mock_spotify_data_service.get_track_by_id.side_effect = SpotifyDataServiceException(exception_message)

    with pytest.raises(InsightsServiceException, match="Service failure") as e:
        await insights_service.tag_lyrics_with_emotion(access_token="", track_id="1", emotion=Emotion.SADNESS)

    assert exception_message in str(e)


# 2. Test tag_lyrics_with_emotion raises InsightsServiceException if LyricsServiceException occurs.
@pytest.mark.asyncio
async def test_tag_lyrics_raises_insights_service_exception_if_lyrics_service_exception_occurs(
        insights_service,
        mock_spotify_data_service,
        mock_spotify_track_factory,
        mock_lyrics_service
):
    track_id = "1"
    mock_spotify_data_service.get_track_by_id.return_value = mock_spotify_track_factory(track_id)
    exception_message = "Test LyricsService failure"
    mock_lyrics_service.get_lyrics.side_effect = LyricsServiceException(exception_message)

    with pytest.raises(InsightsServiceException, match="Service failure") as e:
        await insights_service.tag_lyrics_with_emotion(access_token="", track_id=track_id, emotion=Emotion.SADNESS)

    assert exception_message in str(e)


# 3. Test tag_lyrics_with_emotion raises InsightsServiceException if AnalysisServiceException occurs.
@pytest.mark.asyncio
async def test_tag_lyrics_raises_insights_service_exception_if_analysis_service_exception_occurs(
        insights_service,
        mock_spotify_data_service,
        mock_spotify_track_factory,
        mock_lyrics_service,
        mock_lyrics_response_factory,
        mock_analysis_service
):
    track_id = "1"
    mock_spotify_data_service.get_track_by_id.return_value = mock_spotify_track_factory(track_id)
    mock_lyrics_service.get_lyrics.return_value = mock_lyrics_response_factory(track_id)
    exception_message = "Test AnalysisService failure"
    mock_analysis_service.get_emotional_tags.side_effect = AnalysisServiceException(exception_message)

    with pytest.raises(InsightsServiceException, match="Service failure") as e:
        await insights_service.tag_lyrics_with_emotion(access_token="", track_id=track_id, emotion=Emotion.SADNESS)

    assert exception_message in str(e)


# 4. Test tag_lyrics_with_emotion returns expected emotional tags response.
@pytest.mark.asyncio
async def test_tag_lyrics_with_emotion_returns_expected_response(
        insights_service,
        mock_spotify_data_service,
        mock_spotify_track_factory,
        mock_lyrics_service,
        mock_lyrics_response_factory,
        mock_analysis_service,
        mock_analysis_data
):
    track_id = "1"
    access_token = "access"
    mock_spotify_data_service.get_track_by_id.return_value = mock_spotify_track_factory(track_id)
    mock_lyrics_service.get_lyrics.return_value = mock_lyrics_response_factory(track_id)
    mock_analysis_service.get_emotional_tags.return_value = mock_analysis_data

    res = await insights_service.tag_lyrics_with_emotion(
        access_token=access_token,
        track_id=track_id,
        emotion=Emotion.SADNESS
    )

    expected_response = EmotionalTagsResponse(track_id=track_id, emotion=Emotion.SADNESS, lyrics="lyrics")
    assert res == expected_response
    mock_spotify_data_service.get_track_by_id.assert_called_once_with(access_token=access_token, track_id=track_id)
    lyrics_request = LyricsRequest(track_id=track_id, artist_name="artist_name", track_title="track_name")
    mock_lyrics_service.get_lyrics.assert_called_once_with(lyrics_request)
    emotional_tags_request = EmotionalTagsRequest(track_id=track_id, emotion=Emotion.SADNESS, lyrics="lyrics")
    mock_analysis_service.get_emotional_tags.assert_called_once_with(emotional_tags_request)
