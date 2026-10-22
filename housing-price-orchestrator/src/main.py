import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request
import httpx
from service.pricing_service import PricingService
from provider.mlflow_model_provider import MLFlowModelProvider
from shared.config.config_loader import load_config_settings
from shared.view.request_view import PricePredictionBatchRequest, PricePredictionRequest
from shared.view.response_view import PricePredictionBatchResponseView, PricePredictionResponseView

app_settings = load_config_settings(os.getenv('ENV', 'dev'))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create the async HTTP client and inject services onto app.state
    client = httpx.AsyncClient()
    app.state.model_provider = MLFlowModelProvider(app_settings.pricing_model_url, client)
    app.state.pricing_service = PricingService(app.state.model_provider)
    yield
    # Shutdown: close the async HTTP client
    await client.aclose()


app = FastAPI(lifespan=lifespan)


def get_pricing_service(request: Request) -> PricingService:
    """Dependency that provides the PricingService from the application state."""
    return request.app.state.pricing_service


@app.post('/api/v1/price/predict')
async def predict(
    price_prediction_request: PricePredictionRequest,
    pricing_service: PricingService = Depends(get_pricing_service),
) -> PricePredictionResponseView:
    """Endpoint to predict the price of a housing unit.

    Args:
        price_prediction_request: The request containing the input data for the prediction.
        pricing_service: The injected PricingService instance.

    Returns:
        A PricePredictionResponseView containing the predicted price.
    """

    try:
        price_prediction = await pricing_service.predict_price(price_prediction_request)
        return PricePredictionResponseView(id=price_prediction.id, predicted_price=price_prediction.predicted_price)
    except ValueError:
        raise HTTPException(status_code=404, detail='No results found.')


@app.post('/api/v1/price/predict/batch')
async def batch_predict(
    price_prediction_requests: PricePredictionBatchRequest,
    pricing_service: PricingService = Depends(get_pricing_service),
) -> PricePredictionBatchResponseView:
    """Endpoint to predict the price of multiple housing units.

    Args:
        price_prediction_requests: A list of requests containing the input data for the predictions.
        pricing_service: The injected PricingService instance.

    Returns:
        A list of PricePredictionResponseView containing the predicted prices.
    """

    try:
        price_predictions = await pricing_service.predict_price_batch(price_prediction_requests)
        return PricePredictionBatchResponseView(
            predictions=[
                PricePredictionResponseView(id=pred.id, predicted_price=pred.predicted_price)
                for pred in price_predictions
            ]
        )
    except ValueError:
        raise HTTPException(status_code=404, detail='No results found.')
