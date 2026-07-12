import pytest
import httpx
from unittest.mock import MagicMock, patch

from client.orchestrator_client import OrchestratorClient
from models.prediction_models import (
    PricePredictionRequest,
    PricePredictionBatchRequest,
    PricePredictionResponse,
)


@pytest.fixture
def client():
    return OrchestratorClient(base_url='http://test:8000')


@pytest.fixture
def valid_request():
    return PricePredictionRequest(
        id=1,
        ms_sub_class=20,
        ms_zoning='RL',
        lot_area=8000,
        street='Pave',
        lot_shape='Reg',
        land_contour='Lvl',
        utilities='AllPub',
        lot_config='Inside',
        land_slope='Gtl',
        neighborhood='CollgCr',
        condition_1='Norm',
        condition_2='Norm',
        bldg_type='1Fam',
        house_style='2Story',
        overall_qual=7,
        overall_cond=5,
        year_built=2000,
        year_remod_add=2000,
        roof_style='Gable',
        roof_matl='CompShg',
        exterior_1st='AsphShn',
        exterior_2nd='AsphShn',
        exter_qual='Gd',
        exter_cond='TA',
        foundation='PConc',
        bsmt_fin_sf_1=700,
        bsmt_fin_sf_2=0,
        bsmt_unf_sf=500,
        total_bsmt_sf=1200,
        heating='GasA',
        heating_qc='Gd',
        central_air='Y',
        first_flr_sf=1200,
        second_flr_sf=1200,
        low_qual_fin_sf=0,
        gr_liv_area=2400,
        bsmt_full_bath=1,
        bsmt_half_bath=0,
        full_bath=2,
        half_bath=0,
        bedroom_abv_gr=3,
        kitchen_abv_gr=1,
        kitchen_qual='Gd',
        tot_rms_abv_grd=10,
        functional='Typ',
        fireplaces=1,
        garage_cars=2,
        garage_area=400,
        paved_drive='Y',
        wood_deck_sf=300,
        open_porch_sf=100,
        enclosed_porch=0,
        three_ssn_porch=0,
        screen_porch=0,
        pool_area=0,
        misc_val=0,
        mo_sold=5,
        yr_sold=2023,
        sale_type='WD',
        sale_condition='Normal',
    )


class TestOrchestratorClientPredict:
    def test_predict_returns_response(self, client, valid_request):
        expected_response = PricePredictionResponse(id=1, predicted_price=250000.0)
        mock_response_data = expected_response.model_dump()

        mock_response = httpx.Response(
            200,
            json=mock_response_data,
            request=httpx.Request('POST', 'http://test:8000/api/v1/price/predict'),
        )

        with patch.object(client._client, 'post', return_value=mock_response) as mock_post:
            result = client.predict(valid_request)

            assert result.id == 1
            assert result.predicted_price == 250000.0
            mock_post.assert_called_once()

    def test_predict_raises_on_non_200(self, client, valid_request):
        mock_response = httpx.Response(
            500,
            json={'detail': 'Internal server error'},
            request=httpx.Request('POST', 'http://test:8000/api/v1/price/predict'),
        )

        with patch.object(client._client, 'post', return_value=mock_response):
            with pytest.raises(Exception) as exc_info:
                client.predict(valid_request)
            assert '500' in str(exc_info.value)


class TestOrchestratorClientPredictBatch:
    def test_predict_batch_returns_responses(self, client, valid_request):
        expected_responses = [
            PricePredictionResponse(id=1, predicted_price=250000.0),
            PricePredictionResponse(id=2, predicted_price=300000.0),
        ]
        mock_response_data = {'predictions': [r.model_dump() for r in expected_responses]}

        mock_response = httpx.Response(
            200,
            json=mock_response_data,
            request=httpx.Request('POST', 'http://test:8000/api/v1/price/predict/batch'),
        )

        batch_request = PricePredictionBatchRequest(data=[valid_request, valid_request])

        with patch.object(client._client, 'post', return_value=mock_response) as mock_post:
            result = client.predict_batch(batch_request)

            assert len(result.predictions) == 2
            assert result.predictions[0].predicted_price == 250000.0
            assert result.predictions[1].predicted_price == 300000.0
            mock_post.assert_called_once()


class TestOrchestratorClientClose:
    def test_close_calls_close(self, client):
        client._client.close = MagicMock()
        client.close()
        client._client.close.assert_called_once()
