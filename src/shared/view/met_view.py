from typing import Optional

from pydantic import Field
from shared.data_model_base import ViewBase


class SearchResponse(ViewBase):
    total: int
    object_ids: Optional[list[int]] = Field(alias='objectIDs')


class Department(ViewBase):
    department_id: int
    display_name: str


class DepartmentResponse(ViewBase):
    departments: list[Department]


class ObjectResponse(ViewBase):
    object_id: int = Field(alias='objectID')
    title: str
    primary_image: str
    additional_images: list[str]


class ObjectsResponse(ViewBase):
    total: int
    object_ids: list[int] = Field(alias='objectIDs')
