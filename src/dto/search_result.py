from shared.model import ModelBase


class SearchResult(ModelBase):
    object_id: int
    title: str
    primary_image: str
    additional_images: list[str]
    total_results: int
