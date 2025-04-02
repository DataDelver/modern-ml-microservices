import pytest

from provider.met_provider import MetProvider
from shared.config.config_loader import Settings


@pytest.fixture(autouse=True)
def mock_app_settings(mocker):
    """Mock the app settings for all tests."""

    mock_settings = mocker.MagicMock(Settings)
    mock_settings.met_api_url = 'https://collectionapi-dummy.metmuseum.org'
    mocker.patch('main.app_settings', mock_settings)


@pytest.fixture
def mocked_provider(httpx_mock) -> MetProvider:
    """Mock responses for the Metropolitan Museum of Art API."""

    dummy_url = 'https://collectionapi-dummy.metmuseum.org'

    # Mock the response for the get_objects method
    httpx_mock.add_response(
        url=f'{dummy_url}/public/collection/v1/objects',
        json={
            'total': 1,
            'objectIDs': [1],
        },
        is_optional=True,
    )

    # Mock the response for the get_object method
    httpx_mock.add_response(
        url=f'{dummy_url}/public/collection/v1/objects/1',
        json={
            'objectID': 1,
            'title': 'Test Object',
            'primaryImage': 'https://example.com/image.jpg',
            'additionalImages': [
                'https://example.com/image1.jpg',
                'https://example.com/image2.jpg',
            ],
        },
        is_optional=True,
    )

    # Mock the response for the get_departments method
    httpx_mock.add_response(
        url=f'{dummy_url}/public/collection/v1/departments',
        json={
            'departments': [
                {
                    'departmentId': 1,
                    'displayName': 'Test Department',
                },
            ],
        },
        is_optional=True,
    )

    # Mock the response for the search method
    httpx_mock.add_response(
        url=f'{dummy_url}/public/collection/v1/search?q=Test Title',
        json={
            'total': 1,
            'objectIDs': [1],
        },
        is_optional=True,
    )

    return MetProvider(dummy_url)
