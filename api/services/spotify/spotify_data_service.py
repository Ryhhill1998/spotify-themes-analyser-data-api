import urllib.parse
from collections import defaultdict
from enum import Enum

from loguru import logger
import pydantic

from api.models.models import SpotifyItem, SpotifyTrack, SpotifyArtist, SpotifyTrackArtist, SpotifyTrackData, \
    SpotifyArtistData, SpotifyProfile, SpotifyProfileData, TopGenre
from api.services.endpoint_requester import EndpointRequester, EndpointRequesterUnauthorisedException, \
    EndpointRequesterException, EndpointRequesterNotFoundException
from api.services.spotify.spotify_service import SpotifyService


class SpotifyItemType(str, Enum):
    ARTIST = "artist"
    TRACK = "track"


class SpotifyDataServiceException(Exception):
    """
    Exception raised when the SpotifyDataService fails to make the API request or process the response data.

    Parameters
    ----------
    message : str
        The error message describing the failure.
    """

    def __init__(self, message):
        super().__init__(message)


class SpotifyDataServiceUnauthorisedException(SpotifyDataServiceException):
    """
    Exception raised when SpotifyDataService fails to authenticate the request with the provided access_token.

    Parameters
    ----------
    message : str
        The error message describing the resource that was not found.
    """

    def __init__(self, message):
        super().__init__(message)


class SpotifyDataServiceNotFoundException(SpotifyDataServiceException):
    """
    Exception raised when SpotifyDataService fails to return results for the request.

    Parameters
    ----------
    message : str
        The error message describing the resource that was not found.
    """

    def __init__(self, message):
        super().__init__(message)


class SpotifyDataService(SpotifyService):
    """
    Service responsible for interacting with Spotify's API to fetch user-related spotify data.

    This class provides methods to retrieve a user's top tracks and artists, as well as fetching
    specific tracks and artists by their Spotify ID.

    Inherits from
    -------------
    MusicService, which provides core attributes such as client_id, client_secret, base_url and endpoint_requester.

    Methods
    -------
    get_top_items(tokens, item_type, time_range=TimeRange.MEDIUM, limit=20) -> SpotifyItemsResponse
        Retrieves the top tracks or artists for a user.

    get_item_by_id(item_id, tokens, item_type) -> SpotifyItemResponse
        Retrieves a specific track or artist by its unique identifier, handling authentication and errors.
    """

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            base_url: str,
            endpoint_requester: EndpointRequester
    ):
        """
        Parameters
        ----------
        client_id : str
            The Spotify API client ID.
        client_secret : str
            The Spotify API client secret.
        base_url : str
            The base URL of the Spotify Web API.
        endpoint_requester : EndpointRequester
            The service responsible for making API requests.
        """

        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
            endpoint_requester=endpoint_requester
        )

    @staticmethod
    def _get_bearer_auth_headers(access_token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {access_token}"}

    async def get_profile_data(self, access_token: str) -> SpotifyProfile:
        """
        Fetches a user's profile from Spotify.

        Returns
        -------
        SpotifyProfile
            The user's Spotify profile data.

        Raises
        -------
        SpotifyDataServiceUnauthorisedException
            If the Spotify API request returns a 401 Unauthorised response code.
        SpotifyDataServiceException
            If the Spotify API request fails for any other reason or API data validation fails.
        """

        try:
            url = f"{self.base_url}/me"

            data = await self.endpoint_requester.get(url=url, headers=self._get_bearer_auth_headers(access_token))

            profile_data = SpotifyProfileData(**data)

            return SpotifyProfile(
                id=profile_data.id,
                display_name=profile_data.display_name,
                email=profile_data.email,
                href=profile_data.href,
                images=profile_data.images,
                followers=profile_data.followers.total
            )
        except EndpointRequesterUnauthorisedException as e:
            error_message = "Invalid Spotify API access token"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceUnauthorisedException(error_message)
        except EndpointRequesterException as e:
            error_message = "Failed to make request to Spotify API"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceException(error_message)
        except pydantic.ValidationError as e:
            error_message = "Spotify API data validation failed"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceException(error_message)

    @staticmethod
    def _create_track(data: dict) -> SpotifyTrack:
        """
        Creates a TopTrack object from Spotify API data.

        Parameters
        ----------
        data : dict
            The track data received from Spotify's API.

        Returns
        -------
        SpotifyTrack
            A validated TopTrack object.

        Raises
        -------
        TypeError
            If data is not a dict.
        pydantic.ValidationError
            If data validation fails.
        """
        
        try:
            track_data = SpotifyTrackData(**data)
    
            artist = track_data.artists[0]
            track_artist = SpotifyTrackArtist(id=artist.id, name=artist.name)
            album = track_data.album
    
            top_track = SpotifyTrack(
                id=track_data.id,
                name=track_data.name,
                images=album.images,
                album_name=album.name,
                spotify_url=track_data.external_urls.spotify,
                artist=track_artist,
                release_date=album.release_date,
                explicit=track_data.explicit,
                duration_ms=track_data.duration_ms,
                popularity=track_data.popularity
            )
    
            return top_track
        except TypeError as e:
            error_message = f"Spotify data not of type dict. Actual type: {type(data)} - {e}"
            logger.error(error_message)
            raise SpotifyDataServiceException(error_message)
        except pydantic.ValidationError as e:
            error_message = f"Failed to create SpotifyTrack from Spotify API data: {data} - {e}"
            logger.error(error_message)
            raise SpotifyDataServiceException(error_message)

    @staticmethod
    def _create_artist(data: dict) -> SpotifyArtist:
        """
        Creates a TopArtist object from Spotify API data.

        Parameters
        ----------
        data : dict
            The artist data received from Spotify's API.

        Returns
        -------
        SpotifyArtist
            A validated TopArtist object.

        Raises
        -------
        TypeError
            If data is not a dict.
        pydantic.ValidationError
            If data validation fails.
        """

        try:
            artist_data = SpotifyArtistData(**data)
    
            top_artist = SpotifyArtist(
                id=artist_data.id,
                name=artist_data.name,
                images=artist_data.images,
                spotify_url=artist_data.external_urls.spotify,
                genres=artist_data.genres,
                followers=artist_data.followers.total,
                popularity=artist_data.popularity
            )
    
            return top_artist
        except TypeError as e:
            error_message = f"Spotify data not of type dict. Actual type: {type(data)} - {e}"
            logger.error(error_message)
            raise SpotifyDataServiceException(error_message)
        except pydantic.ValidationError as e:
            error_message = f"Failed to create SpotifyArtist from Spotify API data: {data} - {e}"
            logger.error(error_message)
            raise SpotifyDataServiceException(error_message)

    async def _get_top_items_data(
            self,
            access_token: str,
            item_type: SpotifyItemType,
            time_range: str,
            limit: int
    ) -> list[dict]:
        """
        Fetches a user's top items from Spotify.

        Parameters
        ----------
        item_type : SpotifyItemType
            The type of items to retrieve (TRACKS or ARTISTS).
        time_range : str
            The time range for retrieving top items.
        limit : int
            The number of top items to retrieve.

        Returns
        -------
        list[SpotifyItem]
            A list of the user's top items.

        Raises
        -------
        SpotifyDataServiceUnauthorisedException
            If the Spotify API request returns a 401 Unauthorised response code.
        SpotifyDataServiceException
                If the Spotify API request fails for any other reason or API data validation fails.
        """

        try:
            params = {"time_range": time_range, "limit": limit}
            url = f"{self.base_url}/me/top/{item_type.value}s?" + urllib.parse.urlencode(params)

            data = await self.endpoint_requester.get(url=url, headers=self._get_bearer_auth_headers(access_token))

            top_items = data["items"]

            return top_items
        except EndpointRequesterUnauthorisedException as e:
            error_message = "Invalid Spotify API access token"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceUnauthorisedException(error_message)
        except EndpointRequesterException as e:
            error_message = "Failed to make request to Spotify API"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceException(error_message)
        except KeyError:
            error_message = "No items key present in API data"
            logger.error(error_message)
            raise SpotifyDataServiceException(error_message)
        
    async def get_top_artists(self, access_token: str, time_range: str, limit: int) -> list[SpotifyArtist]:
        top_items_data = await self._get_top_items_data(
            access_token=access_token, 
            item_type=SpotifyItemType.ARTIST, 
            time_range=time_range, 
            limit=limit
        )
        top_artists = [self._create_artist(entry) for entry in top_items_data]
        return top_artists
    
    async def get_top_tracks(self, access_token: str, time_range: str, limit: int) -> list[SpotifyTrack]:
        top_items_data = await self._get_top_items_data(
            access_token=access_token, 
            item_type=SpotifyItemType.TRACK, 
            time_range=time_range, 
            limit=limit
        )
        top_tracks = [self._create_track(entry) for entry in top_items_data]
        return top_tracks

    async def get_top_genres(self, access_token: str, time_range: str, limit: int) -> list[TopGenre]:
        top_artists = await self.get_top_artists(access_token=access_token, time_range=time_range, limit=50)

        if not top_artists:
            raise SpotifyDataServiceException("No top artists found. Cannot proceed with analysis.")

        all_genres = [
            genre
            for artist in top_artists
            for genre in artist.genres
        ]
        total_genres = len(all_genres)

        genres_map = defaultdict(int)

        for genre in all_genres:
            genres_map[genre] += 1

        top_genres = []

        for genre, freq in genres_map.items():
            percentage = round(100 * freq / total_genres)
            top_genre = TopGenre(name=genre, percentage=percentage)
            top_genres.append(top_genre)

        top_genres.sort(key=lambda genre: genre.percentage, reverse=True)
        sampled_top_genres = top_genres[:limit]

        return sampled_top_genres

    async def _get_item_data_by_id(self, access_token: str, item_id: str, item_type: SpotifyItemType) -> dict:
        """
        Fetches a specific item (track or artist) from the Spotify API using its unique identifier.

        Parameters
        ----------
        item_id : str
            The unique identifier of the item (track or artist) to retrieve.
        item_type : SpotifyItemType
            The type of the item being requested (e.g., TRACKS or ARTISTS).

        Returns
        -------
        SpotifyItem
            An object representing the retrieved track or artist.

        Raises
        ------
        SpotifyDataServiceException
            If creating the top item object or the API request fails.
        SpotifyDataServiceUnauthorisedException
            If the Spotify API request returns a 401 Unauthorised response code.
        SpotifyDataServiceNotFoundException
            If the Spotify API request returns a 404 Not Found response code.
        """

        try:
            url = f"{self.base_url}/{item_type.value}s/{item_id}"

            data = await self.endpoint_requester.get(url=url, headers=self._get_bearer_auth_headers(access_token))

            return data
        except EndpointRequesterUnauthorisedException as e:
            error_message = "Invalid Spotify API access token"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceUnauthorisedException(error_message)
        except EndpointRequesterNotFoundException as e:
            error_message = f"Requested Spotify item not found. Item ID: {item_id}, item type: {item_type.value}"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceNotFoundException(error_message)
        except EndpointRequesterException as e:
            error_message = "Failed to make request to Spotify API"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceException(error_message)
        
    async def get_artist_by_id(self, access_token: str, item_id: str) -> SpotifyArtist:
        item = await self._get_item_data_by_id(access_token=access_token, item_id=item_id, item_type=SpotifyItemType.ARTIST)
        artist = self._create_artist(item)
        return artist
    
    async def get_track_by_id(self, access_token: str, item_id: str) -> SpotifyTrack:
        item = await self._get_item_data_by_id(access_token=access_token, item_id=item_id, item_type=SpotifyItemType.TRACK)
        track = self._create_track(item)
        return track

    async def _get_items_data_by_ids(
            self,
            access_token: str,
            item_ids: list[str],
            item_type: SpotifyItemType
    ) -> list[dict]:
        try:
            url = f"{self.base_url}/{item_type.value}s"
            params = {"ids": ",".join(item_ids)}

            data = await self.endpoint_requester.get(
                url=url,
                headers=self._get_bearer_auth_headers(access_token),
                params=params
            )

            items = data[f"{item_type.value}s"]

            return items
        except EndpointRequesterUnauthorisedException as e:
            error_message = "Invalid Spotify API access token"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceUnauthorisedException(error_message)
        except EndpointRequesterException as e:
            error_message = "Failed to make request to Spotify API"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceException(error_message)
        except KeyError as e:
            error_message = f"Invalid response data. Missing field: {item_type.value}s"
            logger.error(f"{error_message} - {e}")
            raise SpotifyDataServiceException(error_message)
        
    async def get_artists_by_ids(self, access_token: str, artist_ids: list[str]) -> list[SpotifyArtist]:
        items_data = await self._get_items_data_by_ids(
            access_token=access_token, 
            item_ids=artist_ids, 
            item_type=SpotifyItemType.ARTIST
        )
        artists = [self._create_artist(entry) for entry in items_data]
        return artists
    
    async def get_tracks_by_ids(self, access_token: str, track_ids: list[str]) -> list[SpotifyTrack]:
        items_data = await self._get_items_data_by_ids(
            access_token=access_token, 
            item_ids=track_ids, 
            item_type=SpotifyItemType.TRACK
        )
        tracks = [self._create_track(entry) for entry in items_data]
        return tracks
