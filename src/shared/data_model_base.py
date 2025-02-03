from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class ViewBase(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class DTOBase(BaseModel):
    class Config:
        populate_by_name = True
