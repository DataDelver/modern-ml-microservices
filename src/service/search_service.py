from provider.met_provider import MetProvider
from shared.dto.search_result import SearchResult


class SearchService:
    """A service for searching the Metropolitan Museum of Art API.

    Args:
        met_provider: A client for the Metropolitan Museum of Art API.
    """

    def __init__(self, met_provider: MetProvider):
        self.met_provider = met_provider

    def search_by_title(self, title: str) -> SearchResult:
        """Searches the Metropolitan Museum of Art API by title.

        Args:
            title: The title of the work to search for.

        Returns:
            The search results.

        Raises:
            ValueError: If no results are found.
        """

        # Search for a work in the Met collection by title
        search_response = self.met_provider.search(q=title)
        object_ids = search_response.object_ids

        # If the work exists
        if object_ids:
            # Fetch the details of the work
            object_request = self.met_provider.get_object(object_id=object_ids[0])

            return SearchResult(
                object_id=object_request.object_id,
                title=object_request.title,
                primary_image=object_request.primary_image,
                additional_images=object_request.additional_images,
                total_results=search_response.total,
            )
        else:
            raise ValueError('No results found.')
