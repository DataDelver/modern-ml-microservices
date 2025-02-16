from fastapi import FastAPI, HTTPException

from provider.met_provider import MetProvider
from service.search_service import SearchService

app = FastAPI()
search_service = SearchService(MetProvider('https://collectionapi.metmuseum.org'))


@app.get('/api/search')
def search(title: str) -> str:
    """Executes a search against the Metropolitan Museum of Art API and returns the url of the primary image of the first search result.

    Args:
        title: The title of the work you wish to search for.

    Returns:
        The url of the primary image of the first search result or 'No results found.' if no search results are found.
    """

    try:
        search_result = search_service.search_by_title(title)
        return search_result.primary_image
    except ValueError:
        raise HTTPException(status_code=404, detail='No results found.')
