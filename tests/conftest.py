from unittest.mock import MagicMock

import pytest

from api.models.models import TokenData


@pytest.fixture
def mock_request_tokens() -> MagicMock:
    mock = MagicMock(spec=TokenData)
    mock.access_token = "access"
    mock.refresh_token = "refresh"
    return mock
