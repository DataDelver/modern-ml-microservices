from shared.data_model_base import DTOBase


class SearchResult(DTOBase):
    object_id: int
    title: str
    primary_image: str
    additional_images: list[str]
    total_results: int
