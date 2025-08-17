from unittest.mock import MagicMock
import pytest
from pytest_mock import MockerFixture

from service.pricing_service import PricingService
from shared.view.request_view import PricePredictionRequest, PricePredictionBatchRequest
from shared.dto.price_prediction import PricePrediction


@pytest.fixture
def mock_model_provider(mocker: MockerFixture) -> MagicMock:
    mock = mocker.MagicMock()
    mock.predict.return_value = MagicMock(predictions=[123456.78, 234567.89])
    return mock


def test_predict_price_success(mock_model_provider: MagicMock) -> None:
    """Test the predict_price method of the PricingService class."""
    # GIVEN
    service = PricingService(mock_model_provider)
    req = PricePredictionRequest(
        id=1,
        ms_sub_class=20,
        ms_zoning='RL',
        lot_area=8450,
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
        year_built=2003,
        year_remod_add=2003,
        roof_style='Gable',
        roof_matl='CompShg',
        exterior_1st='VinylSd',
        exterior_2nd='VinylSd',
        exter_qual='Gd',
        exter_cond='TA',
        foundation='PConc',
        bsmt_fin_sf_1=706,
        bsmt_fin_sf_2=0,
        bsmt_unf_sf=150,
        total_bsmt_sf=856,
        heating='GasA',
        heating_qc='Ex',
        central_air='Y',
        first_flr_sf=856,
        second_flr_sf=854,
        low_qual_fin_sf=0,
        gr_liv_area=1710,
        bsmt_full_bath=1,
        bsmt_half_bath=0,
        full_bath=2,
        half_bath=1,
        bedroom_abv_gr=3,
        kitchen_abv_gr=1,
        kitchen_qual='Gd',
        tot_rms_abv_grd=8,
        functional='Typ',
        fireplaces=0,
        garage_cars=2,
        garage_area=548,
        paved_drive='Y',
        wood_deck_sf=0,
        open_porch_sf=61,
        enclosed_porch=0,
        three_ssn_porch=0,
        screen_porch=0,
        pool_area=0,
        misc_val=0,
        mo_sold=2,
        yr_sold=2008,
        sale_type='WD',
        sale_condition='Normal',
    )

    # WHEN
    result = service.predict_price(req)

    # THEN
    assert isinstance(result, PricePrediction)
    assert result.id == 1
    assert result.predicted_price == 123456.78
    mock_model_provider.predict.assert_called_once()


def test_predict_price_no_prediction(mock_model_provider: MagicMock) -> None:
    """Test the predict_price method when no predictions are returned."""
    # GIVEN
    service = PricingService(mock_model_provider)
    mock_model_provider.predict.return_value = MagicMock(predictions=[])
    req = PricePredictionRequest(
        id=1,
        ms_sub_class=20,
        ms_zoning='RL',
        lot_area=8450,
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
        year_built=2003,
        year_remod_add=2003,
        roof_style='Gable',
        roof_matl='CompShg',
        exterior_1st='VinylSd',
        exterior_2nd='VinylSd',
        exter_qual='Gd',
        exter_cond='TA',
        foundation='PConc',
        bsmt_fin_sf_1=706,
        bsmt_fin_sf_2=0,
        bsmt_unf_sf=150,
        total_bsmt_sf=856,
        heating='GasA',
        heating_qc='Ex',
        central_air='Y',
        first_flr_sf=856,
        second_flr_sf=854,
        low_qual_fin_sf=0,
        gr_liv_area=1710,
        bsmt_full_bath=1,
        bsmt_half_bath=0,
        full_bath=2,
        half_bath=1,
        bedroom_abv_gr=3,
        kitchen_abv_gr=1,
        kitchen_qual='Gd',
        tot_rms_abv_grd=8,
        functional='Typ',
        fireplaces=0,
        garage_cars=2,
        garage_area=548,
        paved_drive='Y',
        wood_deck_sf=0,
        open_porch_sf=61,
        enclosed_porch=0,
        three_ssn_porch=0,
        screen_porch=0,
        pool_area=0,
        misc_val=0,
        mo_sold=2,
        yr_sold=2008,
        sale_type='WD',
        sale_condition='Normal',
    )

    # WHEN / THEN
    with pytest.raises(ValueError, match='No predictions returned from the model.'):
        service.predict_price(req)
    mock_model_provider.predict.assert_called_once()


def test_predict_price_batch_success(mock_model_provider: MagicMock) -> None:
    """Test the predict_price_batch method of the PricingService class."""
    # GIVEN
    service = PricingService(mock_model_provider)
    req1 = PricePredictionRequest(
        id=1,
        ms_sub_class=20,
        ms_zoning='RL',
        lot_area=8450,
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
        year_built=2003,
        year_remod_add=2003,
        roof_style='Gable',
        roof_matl='CompShg',
        exterior_1st='VinylSd',
        exterior_2nd='VinylSd',
        exter_qual='Gd',
        exter_cond='TA',
        foundation='PConc',
        bsmt_fin_sf_1=706,
        bsmt_fin_sf_2=0,
        bsmt_unf_sf=150,
        total_bsmt_sf=856,
        heating='GasA',
        heating_qc='Ex',
        central_air='Y',
        first_flr_sf=856,
        second_flr_sf=854,
        low_qual_fin_sf=0,
        gr_liv_area=1710,
        bsmt_full_bath=1,
        bsmt_half_bath=0,
        full_bath=2,
        half_bath=1,
        bedroom_abv_gr=3,
        kitchen_abv_gr=1,
        kitchen_qual='Gd',
        tot_rms_abv_grd=8,
        functional='Typ',
        fireplaces=0,
        garage_cars=2,
        garage_area=548,
        paved_drive='Y',
        wood_deck_sf=0,
        open_porch_sf=61,
        enclosed_porch=0,
        three_ssn_porch=0,
        screen_porch=0,
        pool_area=0,
        misc_val=0,
        mo_sold=2,
        yr_sold=2008,
        sale_type='WD',
        sale_condition='Normal',
    )
    req2 = PricePredictionRequest(
        id=2,
        ms_sub_class=60,
        ms_zoning='RL',
        lot_area=9600,
        street='Pave',
        lot_shape='Reg',
        land_contour='Lvl',
        utilities='AllPub',
        lot_config='Corner',
        land_slope='Gtl',
        neighborhood='CollgCr',
        condition_1='Norm',
        condition_2='Norm',
        bldg_type='1Fam',
        house_style='2Story',
        overall_qual=8,
        overall_cond=5,
        year_built=2005,
        year_remod_add=2006,
        roof_style='Gable',
        roof_matl='CompShg',
        exterior_1st='VinylSd',
        exterior_2nd='VinylSd',
        exter_qual='Gd',
        exter_cond='TA',
        foundation='PConc',
        bsmt_fin_sf_1=800,
        bsmt_fin_sf_2=0,
        bsmt_unf_sf=100,
        total_bsmt_sf=900,
        heating='GasA',
        heating_qc='Ex',
        central_air='Y',
        first_flr_sf=900,
        second_flr_sf=900,
        low_qual_fin_sf=0,
        gr_liv_area=1800,
        bsmt_full_bath=1,
        bsmt_half_bath=0,
        full_bath=2,
        half_bath=1,
        bedroom_abv_gr=4,
        kitchen_abv_gr=1,
        kitchen_qual='Gd',
        tot_rms_abv_grd=9,
        functional='Typ',
        fireplaces=1,
        garage_cars=2,
        garage_area=600,
        paved_drive='Y',
        wood_deck_sf=100,
        open_porch_sf=50,
        enclosed_porch=0,
        three_ssn_porch=0,
        screen_porch=0,
        pool_area=0,
        misc_val=0,
        mo_sold=5,
        yr_sold=2009,
        sale_type='WD',
        sale_condition='Normal',
    )
    batch_req = PricePredictionBatchRequest(data=[req1, req2])

    # WHEN
    result = service.predict_price_batch(batch_req)

    # THEN
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].predicted_price == 123456.78
    assert result[1].id == 2
    assert result[1].predicted_price == 234567.89
    mock_model_provider.predict.assert_called_once()


def test_predict_price_batch_no_predictions(mock_model_provider: MagicMock) -> None:
    """Test the predict_price_batch method when no predictions are returned."""
    # GIVEN
    service = PricingService(mock_model_provider)
    mock_model_provider.predict.return_value = MagicMock(predictions=[])
    req1 = PricePredictionRequest(
        id=1,
        ms_sub_class=20,
        ms_zoning='RL',
        lot_area=8450,
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
        year_built=2003,
        year_remod_add=2003,
        roof_style='Gable',
        roof_matl='CompShg',
        exterior_1st='VinylSd',
        exterior_2nd='VinylSd',
        exter_qual='Gd',
        exter_cond='TA',
        foundation='PConc',
        bsmt_fin_sf_1=706,
        bsmt_fin_sf_2=0,
        bsmt_unf_sf=150,
        total_bsmt_sf=856,
        heating='GasA',
        heating_qc='Ex',
        central_air='Y',
        first_flr_sf=856,
        second_flr_sf=854,
        low_qual_fin_sf=0,
        gr_liv_area=1710,
        bsmt_full_bath=1,
        bsmt_half_bath=0,
        full_bath=2,
        half_bath=1,
        bedroom_abv_gr=3,
        kitchen_abv_gr=1,
        kitchen_qual='Gd',
        tot_rms_abv_grd=8,
        functional='Typ',
        fireplaces=0,
        garage_cars=2,
        garage_area=548,
        paved_drive='Y',
        wood_deck_sf=0,
        open_porch_sf=61,
        enclosed_porch=0,
        three_ssn_porch=0,
        screen_porch=0,
        pool_area=0,
        misc_val=0,
        mo_sold=2,
        yr_sold=2008,
        sale_type='WD',
        sale_condition='Normal',
    )
    batch_req = PricePredictionBatchRequest(data=[req1])

    # WHEN / THEN
    with pytest.raises(ValueError, match='No predictions returned from the model.'):
        service.predict_price_batch(batch_req)
    mock_model_provider.predict.assert_called_once()
