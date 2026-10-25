import httpx

from models.prediction_models import (
    PricePredictionRequest,
    PricePredictionBatchRequest,
    PricePredictionResponse,
    PricePredictionBatchResponse,
)


class OrchestratorClient:
    """Asynchronous HTTP client for communicating with the housing price orchestrator."""

    def __init__(self, base_url: str = 'http://localhost:8000'):
        self._client = httpx.AsyncClient(base_url=base_url, timeout=30.0)

    async def __aenter__(self) -> 'OrchestratorClient':
        """Support use as an async context manager."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Close the underlying HTTP client when exiting the context."""
        await self.aclose()

    async def predict(self, request: PricePredictionRequest) -> PricePredictionResponse:
        """Send a single prediction request to the orchestrator."""
        response = await self._client.post(
            '/api/v1/price/predict',
            json=request.model_dump(),
        )
        if response.status_code != 200:
            raise Exception(f'Prediction failed with status {response.status_code}: {response.text}')
        return PricePredictionResponse.model_validate(response.json())

    async def predict_batch(self, batch_request: PricePredictionBatchRequest) -> PricePredictionBatchResponse:
        """Send a batch prediction request to the orchestrator."""
        response = await self._client.post(
            '/api/v1/price/predict/batch',
            json=batch_request.model_dump(),
        )
        if response.status_code != 200:
            raise Exception(f'Batch prediction failed with status {response.status_code}: {response.text}')
        return PricePredictionBatchResponse.model_validate(response.json())

    async def aclose(self):
        """Close the underlying HTTP client."""
        await self._client.aclose()
