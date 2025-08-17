import pandas as pd
import httpx
import pytest
from unittest.mock import MagicMock

from provider.mlflow_model_provider import MLFlowModelProvider
from shared.view.mlflow_view import MLFlowPredictionsView


def test_health_success(mocker):
    """Test the health method returns True when /ping returns 200."""
    # GIVEN
    mocker.patch('httpx.get', return_value=MagicMock(status_code=200))
    provider = MLFlowModelProvider(base_url='http://fake-url')

    # WHEN
    result = provider.health()

    # THEN
    assert result is True


def test_health_failure(mocker):
    """Test the health method returns False when /ping raises an error."""
    # GIVEN
    mocker.patch('httpx.get', side_effect=httpx.RequestError('fail'))
    provider = MLFlowModelProvider(base_url='http://fake-url')

    # WHEN
    result = provider.health()

    # THEN
    assert result is False


def test_predict_success(mocker):
    """Test the predict method returns MLFlowPredictionsView on success."""
    # GIVEN
    mock_client = MagicMock()
    provider = MLFlowModelProvider(base_url='http://fake-url', client=mock_client)
    df = pd.DataFrame([{'a': 1, 'b': 2}])
    expected_payload = {'dataframe_split': df.to_dict(orient='split')}
    mock_response = MagicMock()
    mock_response.json.return_value = {'predictions': [123.45]}
    mock_client.post.return_value = mock_response
    mock_response.raise_for_status.return_value = None
    mocker.patch.object(
        MLFlowPredictionsView, 'model_validate', return_value=MLFlowPredictionsView(predictions=[123.45])
    )

    # WHEN
    result = provider.predict(df)

    # THEN
    mock_client.post.assert_called_once()
    assert isinstance(result, MLFlowPredictionsView)
    assert result.predictions == [123.45]


def test_predict_http_error(mocker):
    """Test the predict method raises if HTTP error occurs."""
    # GIVEN
    mock_client = MagicMock()
    provider = MLFlowModelProvider(base_url='http://fake-url', client=mock_client)
    df = pd.DataFrame([{'a': 1, 'b': 2}])
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        'fail', request=MagicMock(), response=MagicMock()
    )
    mock_client.post.return_value = mock_response

    # WHEN / THEN
    with pytest.raises(httpx.HTTPStatusError):
        provider.predict(df)
