from typing import Optional
import httpx
import pandas as pd
from shared.view.mlflow_view import MLFlowPredictionsView
import json


class MLFlowModelProvider:
    """Provider for interacting with MLFlow models.

    Args:
        model_uri: The URI of the MLFlow model.
        client: An optional httpx client for making requests. If not provided, a new client will be created.
    """

    def __init__(self, base_url: str, client: Optional[httpx.Client] = None):
        self.base_url = base_url
        self.client = client or httpx.Client()

    def health(self) -> bool:
        """Checks the health of the MLFlow model provider.

        Returns:
            A string indicating the health status of the model provider.
        """
        try:
            response = httpx.get(f'{self.base_url}/ping')
            return response.status_code == 200
        except httpx.RequestError:
            return False

    def predict(self, data: pd.DataFrame) -> MLFlowPredictionsView:
        """Makes a prediction using the MLFlow model.

        Args:
            data: The input data for the prediction.

        Returns:
            A ModelPredictionsView containing the predictions.

        Raises:
            HTTPStatusError: If the prediction request fails.
        """

        payload = {'dataframe_split': json.loads(data.to_json(orient='split'))}

        response = self.client.post(f'{self.base_url}/invocations', json=payload)
        response.raise_for_status()

        predictions = response.json()
        return MLFlowPredictionsView.model_validate(predictions)
