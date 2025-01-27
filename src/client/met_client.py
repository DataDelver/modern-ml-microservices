from datetime import datetime
from typing import Optional
import httpx

from pydantic import Field

from shared.model import ModelBase


class SearchResponse(ModelBase):
    total: int
    object_ids: Optional[list[int]] = Field(alias='objectIDs')


class Department(ModelBase):
    department_id: int
    display_name: str


class DepartmentResponse(ModelBase):
    departments: list[Department]


class ObjectResponse(ModelBase):
    object_id: int = Field(alias='objectID')
    title: str
    primary_image: str
    additional_images: list[str]


class ObjectsResponse(ModelBase):
    total: int
    object_ids: list[int] = Field(alias='objectIDs')


class MetClient:
    """A client for the Metropolitan Museum of Art API.

    Args:
        base_url: The base URL of the API.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_objects(
        self, metadata_date: Optional[datetime] = None, department_ids: Optional[list[int]] = None
    ) -> ObjectsResponse:
        """Retrieves objects from the Metropolitan Museum of Art API.

        Args:
            metadata_date: Returns any objects with updated data after this date.
            department_ids: Returns any objects in a specific department.

        Returns:
            A list of objects.
        """

        query_params = {}

        if metadata_date:
            query_params['metadataDate'] = metadata_date.strftime('%Y-%m-%d')
        if department_ids:
            query_params['departmentIds'] = '|'.join(map(str, department_ids))

        r = httpx.get(
            f'{self.base_url}/public/collection/v1/objects',
            params=query_params,
        )

        return ObjectsResponse.model_validate(r.json())

    def get_object(self, object_id: int) -> ObjectResponse:
        """Retrieves an object from the Metropolitan Museum of Art API.

        Args:
            object_id: The ID of the object to retrieve.

        Returns:
            The object.
        """

        r = httpx.get(f'{self.base_url}/public/collection/v1/objects/{object_id}')
        return ObjectResponse.model_validate(r.json())

    def get_departments(self) -> DepartmentResponse:
        """Retrieves departments from the Metropolitan Museum of Art API.

        Returns:
            A list of departments.
        """

        r = httpx.get(f'{self.base_url}/public/collection/v1/departments')
        return DepartmentResponse.model_validate(r.json())

    def search(self, q: str, title: Optional[bool] = None, has_images: Optional[bool] = None) -> SearchResponse:
        """Executes a search against the Metropolitan Museum of Art API.

        Args:
            q: The query string.
            title: Whether to search the title field.
            has_images: Whether to search for objects with images.

        Returns:
            The search results.
        """

        query_params = {'q': q}

        if title is not None:
            query_params['title'] = str(title)

        if has_images is not None:
            query_params['hasImages'] = str(has_images)

        r = httpx.get(
            f'{self.base_url}/public/collection/v1/search',
            params=query_params,
        )

        return SearchResponse.model_validate(r.json())