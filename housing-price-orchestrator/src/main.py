import os
from fastapi import FastAPI, HTTPException
from service.pricing_service import PricingService
from provider.mlflow_model_provider import MLFlowModelProvider
from shared.config.config_loader import load_config_settings
from shared.view.request_view import PricePredictionBatchRequest, PricePredictionRequest
from shared.view.response_view import PricePredictionBatchResponseView, PricePredictionResponseView

app = FastAPI()
app_settings = load_config_settings(os.getenv('ENV', 'dev'))
pricing_service = PricingService(MLFlowModelProvider(app_settings.pricing_model_url))


@app.post('/api/v1/price/predict')
def predict(price_prediction_request: PricePredictionRequest) -> PricePredictionResponseView:
    """Endpoint to predict the price of a housing unit.

    Args:
        price_prediction_request: The request containing the input data for the prediction.

    Returns:
        A PricePredictionResponseView containing the predicted price.
    """

    try:
        price_prediction = pricing_service.predict_price(price_prediction_request)
        return PricePredictionResponseView(id=price_prediction.id, predicted_price=price_prediction.predicted_price)
    except ValueError:
        raise HTTPException(status_code=404, detail='No results found.')


@app.post('/api/v1/price/predict/batch')
def batch_predict(price_prediction_requests: PricePredictionBatchRequest) -> PricePredictionBatchResponseView:
    """Endpoint to predict the price of multiple housing units.

    Args:
        price_prediction_requests: A list of requests containing the input data for the predictions.

    Returns:
        A list of PricePredictionResponseView containing the predicted prices.
    """

    try:
        price_predictions = pricing_service.predict_price_batch(price_prediction_requests)
        return PricePredictionBatchResponseView(
            predictions=[
                PricePredictionResponseView(id=pred.id, predicted_price=pred.predicted_price)
                for pred in price_predictions
            ]
        )
    except ValueError:
        raise HTTPException(status_code=404, detail='No results found.')
