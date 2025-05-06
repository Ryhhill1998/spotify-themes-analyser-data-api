from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

from api.dependencies import get_spotify_data_service, get_insights_service
from api.main import app
from api.services.insights_service import InsightsService


@pytest.fixture
def mock_insights_service() -> MagicMock:
    return MagicMock(spec=InsightsService)


@pytest.fixture
def client(mock_spotify_data_service, mock_insights_service):
    app.dependency_overrides[get_spotify_data_service] = lambda: mock_spotify_data_service
    app.dependency_overrides[get_insights_service] = lambda: mock_insights_service

    yield TestClient(app, follow_redirects=False, raise_server_exceptions=False)

    app.dependency_overrides = {}
