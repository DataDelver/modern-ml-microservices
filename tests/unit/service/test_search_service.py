from unittest.mock import MagicMock
import pytest
from pytest_mock import MockerFixture

from provider.met_provider import MetProvider
from service.search_service import SearchService
from shared.view.met_view import DepartmentResponse, ObjectResponse, ObjectsResponse, SearchResponse


@pytest.fixture
def mock_provider(mocker: MockerFixture) -> MagicMock:
    mock = mocker.MagicMock(MetProvider)
    mock.get_objects.return_value = ObjectsResponse.model_validate(
        {
            'total': 1,
            'objectIDs': [1],
        }
    )
    mock.get_object.return_value = ObjectResponse.model_validate(
        {
            'objectID': 1,
            'title': 'Test Object',
            'primaryImage': 'https://example.com/image.jpg',
            'additionalImages': ['https://example.com/image1.jpg', 'https://example.com/image2.jpg'],
        }
    )
    mock.get_departments.return_value = DepartmentResponse.model_validate(
        {
            'departments': [
                {
                    'departmentId': 1,
                    'displayName': 'Test Department',
                },
            ],
        }
    )
    mock.search.return_value = SearchResponse.model_validate(
        {
            'total': 1,
            'objectIDs': [1],
        }
    )
    return mock


def test_search_by_title(mock_provider: MagicMock) -> None:
    """Test the search_by_title method of the SearchService class."""

    # GIVEN
    service = SearchService(mock_provider)
    title = 'Test Title'

    # WHEN
    result = service.search_by_title(title)

    # THEN
    assert result.object_id == 1
    assert result.title == 'Test Object'
    assert result.primary_image == 'https://example.com/image.jpg'
    assert result.additional_images == ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']
    assert result.total_results == 1
    mock_provider.search.assert_called_once_with(q=title)


def test_search_by_title_no_results(mock_provider: MagicMock) -> None:
    """Test the search_by_title method of the SearchService class when no results are found."""

    # GIVEN
    service = SearchService(mock_provider)
    title = 'Nonexistent Title'
    mock_provider.search.return_value = SearchResponse.model_validate(
        {
            'total': 0,
            'objectIDs': [],
        }
    )

    # WHEN / THEN
    with pytest.raises(ValueError, match='No results found.'):
        service.search_by_title(title)
    mock_provider.search.assert_called_once_with(q=title)
