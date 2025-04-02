from main import app
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest
from pytest_mock import MockerFixture

from service.search_service import SearchService


@pytest.fixture
def mock_search_service(mocker: MockerFixture) -> MagicMock:
    """Mock the SearchService class."""

    mock = MagicMock(SearchService)
    mock.search_by_title.return_value.primary_image = 'https://example.com/image.jpg'
    return mock


def test_search(mock_search_service: MagicMock, mocker: MockerFixture) -> None:
    """Test the search endpoint."""

    # GIVEN
    client = TestClient(app)
    mocker.patch('main.search_service', mock_search_service)
    title = 'Test Title'

    # WHEN
    response = client.get(f'/api/search?title={title}')

    # THEN
    assert response.status_code == 200
    assert response.json() == 'https://example.com/image.jpg'
    mock_search_service.search_by_title.assert_called_once_with(title)


def test_search_no_results(mock_search_service: MagicMock, mocker: MockerFixture) -> None:
    """Test the search endpoint when no results are found."""

    # GIVEN
    client = TestClient(app)
    mocker.patch('main.search_service', mock_search_service)
    mock_search_service.search_by_title.side_effect = ValueError('No results found.')
    title = 'Test Title'

    # WHEN
    response = client.get(f'/api/search?title={title}')

    # THEN
    assert response.status_code == 404
    assert response.json() == {'detail': 'No results found.'}
