from provider.met_provider import MetProvider


def test_get_objects(mocked_provider: MetProvider) -> None:
    """Test the get_objects method of the MetProvider class."""

    # GIVEN
    provider = mocked_provider

    # WHEN
    response = provider.get_objects()

    # THEN
    assert response.total == 1
    assert response.object_ids == [1]


def test_get_object(mocked_provider: MetProvider):
    """Test the get_object method of the MetProvider class."""

    # GIVEN
    provider = mocked_provider

    # WHEN
    response = provider.get_object(1)

    # THEN
    assert response.object_id == 1
    assert response.title == 'Test Object'


def test_get_departments(mocked_provider: MetProvider):
    """Test the get_departments method of the MetProvider class."""

    # GIVEN
    provider = mocked_provider

    # WHEN
    response = provider.get_departments()

    # THEN
    assert len(response.departments) == 1
    assert response.departments[0].department_id == 1


def test_search(mocked_provider: MetProvider):
    """Test the search method of the MetProvider class."""

    # GIVEN
    provider = mocked_provider

    # WHEN
    response = provider.search('Test Title')

    # THEN
    assert response.total == 1
    assert response.object_ids == [1]
