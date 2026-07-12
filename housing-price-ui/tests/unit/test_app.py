from ui.app import (
    format_price,
    validate_prediction_request,
    build_prediction_request,
    load_samples,
    format_value,
)


class TestFormatPrice:
    def test_format_price_returns_dollar_string(self):
        assert format_price(250000.0) == '$250,000.00'

    def test_format_price_handles_zero(self):
        assert format_price(0.0) == '$0.00'

    def test_format_price_handles_large_value(self):
        assert format_price(1250000.50) == '$1,250,000.50'


class TestLoadSamples:
    def test_load_samples_returns_list(self):
        samples = load_samples()
        assert isinstance(samples, list)

    def test_load_samples_has_five_entries(self):
        samples = load_samples()
        assert len(samples) == 5

    def test_load_samples_has_required_keys(self):
        samples = load_samples()
        for sample in samples:
            assert 'label' in sample
            assert 'id' in sample
            assert 'data' in sample

    def test_load_samples_data_has_required_fields(self):
        samples = load_samples()
        required = {
            'ms_sub_class',
            'ms_zoning',
            'lot_area',
            'neighborhood',
            'overall_qual',
            'gr_liv_area',
            'bedroom_abv_gr',
        }
        for sample in samples:
            data = sample['data']
            for field in required:
                assert field in data, f'Missing field {field} in sample {sample["label"]}'

    def test_load_samples_have_unique_ids(self):
        samples = load_samples()
        ids = [s['id'] for s in samples]
        assert len(ids) == len(set(ids))


class TestFormatValue:
    def test_format_value_sqft_field(self):
        assert format_value('gr_liv_area', 2400) == '2,400 sqft'

    def test_format_value_quality_field(self):
        assert format_value('overall_qual', 7) == '7/10'

    def test_format_value_none(self):
        assert format_value('lot_frontage', None) == 'N/A'

    def test_format_value_string(self):
        assert format_value('neighborhood', 'CollgCr') == 'CollgCr'


class TestValidatePredictionRequest:
    def test_valid_sample_data_returns_none_error(self):
        """Sample data from samples.json should validate without errors."""
        samples = load_samples()
        for sample in samples:
            errors = validate_prediction_request(sample['data'])
            assert errors is None, f'Sample {sample["label"]} failed validation: {errors}'

    def test_missing_required_field_returns_error(self):
        data = {'ms_sub_class': 20}  # missing all other fields
        error = validate_prediction_request(data)
        assert error is not None
        assert isinstance(error, list) and len(error) > 0


class TestBuildPredictionRequest:
    def test_build_request_from_sample_data(self):
        samples = load_samples()
        sample = samples[0]
        request = build_prediction_request(sample['data'], request_id=sample['id'])
        assert request.id == sample['id']
        assert request.ms_sub_class == sample['data']['ms_sub_class']
        assert request.overall_qual == sample['data']['overall_qual']
        assert request.gr_liv_area == sample['data']['gr_liv_area']
