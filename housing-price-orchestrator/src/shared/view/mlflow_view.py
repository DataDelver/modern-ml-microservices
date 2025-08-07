from typing import Any
from shared.data_model_base import ViewBase


class MLFlowPredictionsView(ViewBase):
    """View model for the prediction results of a machine learning model."""

    predictions: list[Any]
    """List of predictions made by the model."""
