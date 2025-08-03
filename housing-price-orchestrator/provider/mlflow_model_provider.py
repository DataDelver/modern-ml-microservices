from typing import Optional
import httpx
import pandas as pd
from shared.view.model_predictions_view import ModelPredictionsView
import json


class MLFlowModelProvider:
    def __init__(self, model_uri: str, client: Optional[httpx.Client] = None):
        self.model_uri = model_uri
        self.client = client or httpx.Client()

    def health(self) -> bool:
        """Checks the health of the MLFlow model provider.

        Returns:
            A string indicating the health status of the model provider.
        """
        return self.client.get(f'{self.model_uri}/health').status_code == 200

    def predict(self, data: pd.DataFrame) -> ModelPredictionsView:
        """Makes a prediction using the MLFlow model.

        Args:
            data: The input data for the prediction.

        Returns:
            A ModelPredictionsView containing the predictions.

        Raises:
            HTTPStatusError: If the prediction request fails.
        """

        payload = {'dataframe_split': json.loads(data.to_json(orient='split'))}

        response = self.client.post(f'{self.model_uri}/invocations', json=payload)
        response.raise_for_status()

        predictions = response.json()
        return ModelPredictionsView.model_validate(predictions)
