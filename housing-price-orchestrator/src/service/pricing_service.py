from provider.mlflow_model_provider import MLFlowModelProvider
from shared.view.request_view import PricePredictionRequest, PricePredictionBatchRequest
from shared.dto.price_prediction import PricePrediction
import pandas as pd


class PricingService:
    def __init__(self, pricing_model_provider: MLFlowModelProvider):
        self.pricing_model_provider = pricing_model_provider

    def predict_price(self, price_prediction_request: PricePredictionRequest) -> PricePrediction:
        """Predicts the price using the MLFlow model provider.

        Args:
            data: The input data for the prediction.

        Returns:
            A view containing the predictions.
        """

        input_data = price_prediction_request.model_dump(by_alias=True)

        input_df = pd.DataFrame([input_data])
        predictions = self.pricing_model_provider.predict(input_df)
        predicted_price = predictions.predictions[0] if predictions.predictions else None

        if predicted_price is None:
            raise ValueError('No predictions returned from the model.')

        return PricePrediction(id=price_prediction_request.id, predicted_price=predicted_price)

    def predict_price_batch(self, price_prediction_batch_request: PricePredictionBatchRequest) -> list[PricePrediction]:
        """Predicts the prices for a batch of requests using the MLFlow model provider.

        Args:
            price_prediction_batch_request: The batch request containing multiple price prediction requests.

        Returns:
            A list of views containing the predictions.
        """

        input_data = price_prediction_batch_request.model_dump(by_alias=True)
        input_df = pd.DataFrame(input_data['data'])
        predictions = self.pricing_model_provider.predict(input_df)
        predicted_prices = predictions.predictions if predictions.predictions else []

        if not predicted_prices:
            raise ValueError('No predictions returned from the model.')

        return [
            PricePrediction(id=req.id, predicted_price=price)
            for req, price in zip(price_prediction_batch_request.data, predicted_prices)
        ]
