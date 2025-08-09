from pydantic import Field
from shared.data_model_base import DTOBase


class PricePrediction(DTOBase):
    """Data Transfer Object for price prediction requests."""

    id: int = Field(ge=1)
    """Unique identifier for the housing unit."""

    predicted_price: float = Field(gt=0)
    """Predicted price of the housing unit."""
