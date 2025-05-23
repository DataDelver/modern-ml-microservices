from datetime import datetime
from provider.met_provider import MetProvider


def test_get_objects(provider_with_mock_api: MetProvider) -> None:
    """Test the get_objects method of the MetProvider class."""

    # GIVEN
    provider = provider_with_mock_api

    # WHEN
    response = provider.get_objects()

    # THEN
    assert response.total == 1
    assert response.object_ids == [1]


def test_get_objects_with_metadata_date_and_department_ids(provider_with_mock_api: MetProvider, httpx_mock) -> None:
    """Test the get_objects method of the MetProvider class with metadata date."""

    # GIVEN
    provider = provider_with_mock_api
    metadata_date = datetime(day=1, month=1, year=2023)
    department_ids = [1]
    # Mock the response for the get_objects method with metadata date
    httpx_mock.add_response(
        url=f'{provider.base_url}/public/collection/v1/objects?metadataDate=2023-01-01&departmentIds=1',
        json={
            'total': 1,
            'objectIDs': [1],
        },
    )

    # WHEN
    response = provider.get_objects(metadata_date=metadata_date, department_ids=department_ids)

    # THEN
    assert response.total == 1
    assert response.object_ids == [1]


def test_get_object(provider_with_mock_api: MetProvider) -> None:
    """Test the get_object method of the MetProvider class."""

    # GIVEN
    provider = provider_with_mock_api

    # WHEN
    response = provider.get_object(1)

    # THEN
    assert response.object_id == 1
    assert response.title == 'Test Object'


def test_get_departments(provider_with_mock_api: MetProvider) -> None:
    """Test the get_departments method of the MetProvider class."""

    # GIVEN
    provider = provider_with_mock_api

    # WHEN
    response = provider.get_departments()

    # THEN
    assert len(response.departments) == 1
    assert response.departments[0].department_id == 1


def test_search(provider_with_mock_api: MetProvider) -> None:
    """Test the search method of the MetProvider class."""

    # GIVEN
    provider = provider_with_mock_api

    # WHEN
    response = provider.search('Test Title')

    # THEN
    assert response.total == 1
    assert response.object_ids == [1]


def test_search_with_title_and_has_images(provider_with_mock_api: MetProvider, httpx_mock) -> None:
    """Test the search method of the MetProvider class with title and has_images."""

    # GIVEN
    provider = provider_with_mock_api

    # Mock the response for the search method with title and has_images
    httpx_mock.add_response(
        url=f'{provider.base_url}/public/collection/v1/search?q=Test+Title&title=true&hasImages=true',
        json={
            'total': 1,
            'objectIDs': [1],
        },
    )

    # WHEN
    response = provider.search(q='Test Title', title=True, has_images=True)

    # THEN
    assert response.total == 1
    assert response.object_ids == [1]
