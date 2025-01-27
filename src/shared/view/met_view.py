from typing import Optional

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
