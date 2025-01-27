from client.met_client import MetClient
from shared.dto.search_result import SearchResult


class SearchService:
    def __init__(self, met_client: MetClient):
        self.met_client = met_client

    def search_by_title(self, title: str) -> SearchResult:
        search_response = self.met_client.search(q=title, title=True, has_images=True)
        object_ids = search_response.object_ids

        if object_ids:
            object_request = self.met_client.get_object(object_id=object_ids[0])
            primary_image_url = object_request.primary_image
            additional_images = object_request.additional_images

            return SearchResult(
                object_id=object_request.object_id,
                title=object_request.title,
                primary_image=primary_image_url,
                additional_images=additional_images,
                total_results=search_response.total,
            )
        else:
            raise ValueError('No results found.')
