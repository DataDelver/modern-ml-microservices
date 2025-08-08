import os
from fastapi import FastAPI, HTTPException
from service.pricing_service import PricingService
from provider.mlflow_model_provider import MLFlowModelProvider
from shared.config.config_loader import load_config_settings
from shared.view.request_view import PricePredictionRequest
from shared.view.response_view import PricePredictionResponseView

app = FastAPI()
app_settings = load_config_settings(os.getenv('ENV', 'dev'))
pricing_service = PricingService(MLFlowModelProvider(app_settings.pricing_model_url))


@app.post('/api/price/predict')
def search(price_prediction_request: PricePredictionRequest) -> PricePredictionResponseView:
    """Endpoint to predict the price of a housing unit.

    Args:
        price_prediction_request: The request containing the input data for the prediction.

    Returns:
        A PricePredictionResponseView containing the predicted price.
    """

    try:
        price_prediction = pricing_service.predict_price(price_prediction_request)
        return PricePredictionResponseView(
            id=price_prediction_request.id, predicted_price=price_prediction.predicted_price
        )
    except ValueError:
        raise HTTPException(status_code=404, detail='No results found.')
