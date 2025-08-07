from provider.mlflow_model_provider import MLFlowModelProvider
from shared.view.request_view import PricePredictionRequest
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

        return PricePrediction(predicted_price=predicted_price)
