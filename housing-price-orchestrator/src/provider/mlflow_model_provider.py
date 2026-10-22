from typing import Optional
import httpx
import pandas as pd
from shared.view.mlflow_view import MLFlowPredictionsView
import json


class MLFlowModelProvider:
    """Provider for interacting with MLFlow models.

    Args:
        base_url: The URI of the MLFlow model.
        client: An optional httpx.AsyncClient for making requests. If not provided, a new client will be created.
    """

    def __init__(self, base_url: str, client: Optional[httpx.AsyncClient] = None):
        self.base_url = base_url
        self.client = client or httpx.AsyncClient()

    async def health(self) -> bool:
        """Checks the health of the MLFlow model provider.

        Returns:
            True if the model provider is healthy, False otherwise.
        """
        try:
            response = await self.client.get(f'{self.base_url}/ping')
            return response.status_code == 200
        except httpx.RequestError:
            return False

    async def predict(self, data: pd.DataFrame) -> MLFlowPredictionsView:
        """Makes a prediction using the MLFlow model.

        Args:
            data: The input data for the prediction.

        Returns:
            A ModelPredictionsView containing the predictions.

        Raises:
            HTTPStatusError: If the prediction request fails.
        """

        payload = {'dataframe_split': json.loads(data.to_json(orient='split'))}

        response = await self.client.post(f'{self.base_url}/invocations', json=payload)
        response.raise_for_status()

        predictions = response.json()
        return MLFlowPredictionsView.model_validate(predictions)

    async def close(self) -> None:
        """Closes the underlying async HTTP client."""
        await self.client.aclose()
