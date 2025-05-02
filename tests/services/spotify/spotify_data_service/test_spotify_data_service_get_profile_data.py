import pytest

# 1. Test get_profile_data raises SpotifyDataServiceUnauthorisedException if EndpointRequesterUnauthorisedException occurs.
# 2. Test get_profile_data raises SpotifyDataServiceException if EndpointRequesterException occurs.
# 3. Test get_profile_data raises SpotifyDataServiceException if API data is invalid.
# 4. Test get_profile_data calls endpoint_requester.get with expected params.
# 5. Test get_profile_data returns expected SpotifyProfile.
