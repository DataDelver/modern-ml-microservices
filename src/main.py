from typing import Optional
from fastapi import FastAPI
import httpx

app = FastAPI()


@app.get('/api/search')
def search(title: str) -> str:
    """Executes a search against the Metropolitan Museum of Art API and returns the url of the primary image of the first search result.

    Args:
        title: The title of the work you wish to search for.

    Returns:
        The url of the primary image of the first search result or 'No results found.' if no search results are found.
    """
    search_request: httpx.Response = httpx.get(
        'https://collectionapi.metmuseum.org/public/collection/v1/search',
        params={'q': title, 'title': True, 'hasImages': True},
    )

    object_ids: Optional[list[int]] = search_request.json().get('objectIDs')

    if object_ids:
        object_request = httpx.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_ids[0]}')
        primary_image_url = object_request.json().get('primaryImage')
        return primary_image_url
    else:
        return 'No results found.'
