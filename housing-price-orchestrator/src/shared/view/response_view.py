from pydantic import Field
from shared.data_model_base import ViewBase


class PricePredictionResponseView(ViewBase):
    """View model for the response from the housing price orchestrator."""

    id: int = Field(ge=1, alias='Id')
    """Unique identifier for the housing unit."""

    predicted_price: float = Field(gt=0, alias='PredictedPrice')
    """Predicted price of the housing unit."""


class BatchPricePredictionResponseView(ViewBase):
    """View model for the response from the housing price orchestrator for batch predictions."""

    predictions: list[PricePredictionResponseView]
    """List of predicted prices for multiple housing units."""
