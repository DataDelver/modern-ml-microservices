from main import app
from fastapi.testclient import TestClient
import pytest
from pytest_mock import MockerFixture

from provider.met_provider import MetProvider
from service.search_service import SearchService


@pytest.fixture
def search_service(provider_with_mock_api: MetProvider) -> SearchService:
    """Fixture to provide a mocked SearchService instance."""
    return SearchService(provider_with_mock_api)


def test_search(search_service: SearchService, mocker: MockerFixture) -> None:
    """Test the search endpoint."""

    # GIVEN
    client = TestClient(app)
    mocker.patch('main.search_service', search_service)
    title = 'Test Title'

    # WHEN
    response = client.get(f'/api/search?title={title}')

    # THEN
    assert response.status_code == 200
    assert response.json() == 'https://example.com/image.jpg'


def test_search_no_results(search_service: SearchService, mocker: MockerFixture, httpx_mock) -> None:
    """Test the search endpoint when no results are found."""

    # GIVEN
    client = TestClient(app)
    mocker.patch('main.search_service', search_service)
    httpx_mock.add_response(
        url=f'{search_service.met_provider.base_url}/public/collection/v1/search?q=Test No Results Title',
        json={
            'total': 0,
            'objectIDs': [],
        },
    )
    title = 'Test No Results Title'

    # WHEN
    response = client.get(f'/api/search?title={title}')

    # THEN
    assert response.status_code == 404
    assert response.json() == {'detail': 'No results found.'}
