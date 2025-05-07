from unittest.mock import MagicMock

import pytest

from api.services.insights_service import InsightsServiceException
from api.services.spotify.spotify_data_service import SpotifyDataServiceException

# -------------------- GET PROFILE -------------------- #
# 1. Test /data/me/profile returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/profile returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/profile returns 500 error if general exception occurs.
# 4. Test /data/me/profile returns 422 error if request sends no POST body.
# 5. Test /data/me/profile returns 422 error if request missing access token.
# 6. Test /data/me/profile returns 500 error if response data type invalid.
# 7. Test /data/me/profile returns expected response.

# -------------------- GET TOP ARTISTS -------------------- #
# 1. Test /data/me/top/artists returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/artists returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/artists returns 500 error if general exception occurs.
# 4. Test /data/me/top/artists returns 422 error if request sends no POST body.
# 5. Test /data/me/top/artists returns 422 error if request missing access token.
# 6. Test /data/me/top/artists returns 422 error if request missing time range.
# 7. Test /data/me/top/artists returns 422 error if request invalid time range.
# 8. Test /data/me/top/artists returns 422 error if request missing limit.
# 9. Test /data/me/top/artists returns 422 error if request invalid limit.
# 10. Test /data/me/top/artists returns 500 error if response data type invalid.
# 11. Test /data/me/top/artists returns expected response.

# -------------------- GET TOP TRACKS -------------------- #
# 1. Test /data/me/top/tracks returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/tracks returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/tracks returns 500 error if general exception occurs.
# 4. Test /data/me/top/tracks returns 422 error if request sends no POST body.
# 5. Test /data/me/top/tracks returns 422 error if request missing access token.
# 6. Test /data/me/top/tracks returns 422 error if request missing time range.
# 7. Test /data/me/top/tracks returns 422 error if request invalid time range.
# 8. Test /data/me/top/tracks returns 422 error if request missing limit.
# 9. Test /data/me/top/tracks returns 422 error if request invalid limit.
# 10. Test /data/me/top/tracks returns 500 error if response data type invalid.
# 11. Test /data/me/top/tracks returns expected response.

# -------------------- GET TOP GENRES -------------------- #
# 1. Test /data/me/top/genres returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/genres returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/genres returns 500 error if general exception occurs.
# 4. Test /data/me/top/genres returns 422 error if request sends no POST body.
# 5. Test /data/me/top/genres returns 422 error if request missing access token.
# 6. Test /data/me/top/genres returns 422 error if request missing time range.
# 7. Test /data/me/top/genres returns 422 error if request invalid time range.
# 8. Test /data/me/top/genres returns 422 error if request missing limit.
# 9. Test /data/me/top/genres returns 422 error if request invalid limit.
# 10. Test /data/me/top/genres returns 500 error if response data type invalid.
# 11. Test /data/me/top/genres returns expected response.

# -------------------- GET TOP EMOTIONS -------------------- #
# 1. Test /data/me/top/emotions returns 500 error if SpotifyDataServiceException occurs.
# 2. Test /data/me/top/emotions returns 500 error if general exception occurs.
# 3. Test /data/me/top/emotions returns 422 error if request sends no POST body.
# 4. Test /data/me/top/emotions returns 422 error if request missing access token.
# 5. Test /data/me/top/emotions returns 422 error if request missing time range.
# 6. Test /data/me/top/emotions returns 422 error if request invalid time range.
# 7. Test /data/me/top/emotions returns 422 error if request missing limit.
# 8. Test /data/me/top/emotions returns 422 error if request invalid limit.
# 9. Test /data/me/top/emotions returns 500 error if response data type invalid.
# 10. Test /data/me/top/emotions returns expected response.

BASE_URL = "/data/me/top"

# -------------------- GET PROFILE -------------------- #
# 1. Test /data/me/profile returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/profile returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/profile returns 500 error if general exception occurs.
# 4. Test /data/me/profile returns 422 error if request sends no POST body.
# 5. Test /data/me/profile returns 422 error if request missing access token.
# 6. Test /data/me/profile returns 500 error if response data type invalid.
# 7. Test /data/me/profile returns expected response.

# -------------------- GET TOP ARTISTS -------------------- #
# 1. Test /data/me/top/artists returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/artists returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/artists returns 500 error if general exception occurs.
# 4. Test /data/me/top/artists returns 422 error if request sends no POST body.
# 5. Test /data/me/top/artists returns 422 error if request missing access token.
# 6. Test /data/me/top/artists returns 422 error if request missing time range.
# 7. Test /data/me/top/artists returns 422 error if request invalid time range.
# 8. Test /data/me/top/artists returns 422 error if request missing limit.
# 9. Test /data/me/top/artists returns 422 error if request invalid limit.
# 10. Test /data/me/top/artists returns 500 error if response data type invalid.
# 11. Test /data/me/top/artists returns expected response.

# -------------------- GET TOP TRACKS -------------------- #
# 1. Test /data/me/top/tracks returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/tracks returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/tracks returns 500 error if general exception occurs.
# 4. Test /data/me/top/tracks returns 422 error if request sends no POST body.
# 5. Test /data/me/top/tracks returns 422 error if request missing access token.
# 6. Test /data/me/top/tracks returns 422 error if request missing time range.
# 7. Test /data/me/top/tracks returns 422 error if request invalid time range.
# 8. Test /data/me/top/tracks returns 422 error if request missing limit.
# 9. Test /data/me/top/tracks returns 422 error if request invalid limit.
# 10. Test /data/me/top/tracks returns 500 error if response data type invalid.
# 11. Test /data/me/top/tracks returns expected response.

# -------------------- GET TOP GENRES -------------------- #
# 1. Test /data/me/top/genres returns 401 error if SpotifyDataServiceUnauthorisedException occurs.
# 2. Test /data/me/top/genres returns 500 error if SpotifyDataServiceException occurs.
# 3. Test /data/me/top/genres returns 500 error if general exception occurs.
# 4. Test /data/me/top/genres returns 422 error if request sends no POST body.
# 5. Test /data/me/top/genres returns 422 error if request missing access token.
# 6. Test /data/me/top/genres returns 422 error if request missing time range.
# 7. Test /data/me/top/genres returns 422 error if request invalid time range.
# 8. Test /data/me/top/genres returns 422 error if request missing limit.
# 9. Test /data/me/top/genres returns 422 error if request invalid limit.
# 10. Test /data/me/top/genres returns 500 error if response data type invalid.
# 11. Test /data/me/top/genres returns expected response.

# -------------------- GET TOP EMOTIONS -------------------- #
# 1. Test /data/me/top/emotions returns 500 error if SpotifyDataServiceException occurs.
# 2. Test /data/me/top/emotions returns 500 error if general exception occurs.
# 3. Test /data/me/top/emotions returns 422 error if request sends no POST body.
# 4. Test /data/me/top/emotions returns 422 error if request missing access token.
# 5. Test /data/me/top/emotions returns 422 error if request missing time range.
# 6. Test /data/me/top/emotions returns 422 error if request invalid time range.
# 7. Test /data/me/top/emotions returns 422 error if request missing limit.
# 8. Test /data/me/top/emotions returns 422 error if request invalid limit.
# 9. Test /data/me/top/emotions returns 500 error if response data type invalid.
# 10. Test /data/me/top/emotions returns expected response.