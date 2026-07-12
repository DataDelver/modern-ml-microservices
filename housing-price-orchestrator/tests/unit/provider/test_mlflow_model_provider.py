import pandas as pd
import httpx
import pytest
from unittest.mock import AsyncMock, MagicMock

from provider.mlflow_model_provider import MLFlowModelProvider
from shared.view.mlflow_view import MLFlowPredictionsView


@pytest.mark.asyncio
async def test_health_success(mocker):
    """Test the health method returns True when /ping returns 200."""
    # GIVEN
    mock_client = AsyncMock()
    mock_client.get.return_value = MagicMock(status_code=200)
    provider = MLFlowModelProvider(base_url='http://fake-url', client=mock_client)

    # WHEN
    result = await provider.health()

    # THEN
    assert result is True
    mock_client.get.assert_awaited_once_with('http://fake-url/ping')


@pytest.mark.asyncio
async def test_health_failure(mocker):
    """Test the health method returns False when /ping raises an error."""
    # GIVEN
    mock_client = AsyncMock()
    mock_client.get.side_effect = httpx.RequestError('fail')
    provider = MLFlowModelProvider(base_url='http://fake-url', client=mock_client)

    # WHEN
    result = await provider.health()

    # THEN
    assert result is False
    mock_client.get.assert_awaited_once_with('http://fake-url/ping')


@pytest.mark.asyncio
async def test_predict_success(mocker):
    """Test the predict method returns MLFlowPredictionsView on success."""
    # GIVEN
    mock_client = AsyncMock()
    provider = MLFlowModelProvider(base_url='http://fake-url', client=mock_client)
    df = pd.DataFrame([{'a': 1, 'b': 2}])
    mock_response = MagicMock()
    mock_response.json.return_value = {'predictions': [123.45]}
    mock_client.post.return_value = mock_response
    mock_response.raise_for_status.return_value = None
    mocker.patch.object(
        MLFlowPredictionsView, 'model_validate', return_value=MLFlowPredictionsView(predictions=[123.45])
    )

    # WHEN
    result = await provider.predict(df)

    # THEN
    mock_client.post.assert_awaited_once()
    assert isinstance(result, MLFlowPredictionsView)
    assert result.predictions == [123.45]


@pytest.mark.asyncio
async def test_predict_http_error(mocker):
    """Test the predict method raises if HTTP error occurs."""
    # GIVEN
    mock_client = AsyncMock()
    provider = MLFlowModelProvider(base_url='http://fake-url', client=mock_client)
    df = pd.DataFrame([{'a': 1, 'b': 2}])
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        'fail', request=MagicMock(), response=MagicMock()
    )
    mock_client.post.return_value = mock_response

    # WHEN / THEN
    with pytest.raises(httpx.HTTPStatusError):
        await provider.predict(df)


@pytest.mark.asyncio
async def test_close(mocker):
    """Test the close method closes the underlying async client."""
    # GIVEN
    mock_client = AsyncMock()
    provider = MLFlowModelProvider(base_url='http://fake-url', client=mock_client)

    # WHEN
    await provider.close()

    # THEN
    mock_client.aclose.assert_awaited_once()
