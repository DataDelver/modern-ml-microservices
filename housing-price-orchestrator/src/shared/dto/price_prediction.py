from shared.data_model_base import DTOBase


class PricePrediction(DTOBase):
    """Data Transfer Object for price prediction requests."""

    predicted_price: float
    """The predicted price of the housing unit."""
