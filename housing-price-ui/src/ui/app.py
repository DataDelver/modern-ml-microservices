"""Streamlit UI for housing price prediction using sample properties."""

import json
from pathlib import Path

import streamlit as st

from config.settings import UIConfigSettings
from client.orchestrator_client import OrchestratorClient
from models.prediction_models import PricePredictionRequest

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

_SAMPLES_PATH = Path(__file__).parent.parent.parent / 'samples' / 'samples.json'


def load_samples() -> list[dict]:
    """Load sample properties from the bundled JSON file."""
    with open(_SAMPLES_PATH) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------


def format_price(price: float) -> str:
    """Format a price as a dollar string with commas."""
    return f'${price:,.2f}'


def validate_prediction_request(data: dict) -> list[str] | None:
    """Validate form data and return list of errors, or None if valid."""
    try:
        PricePredictionRequest.model_validate({**data, 'id': 1})
        return None
    except Exception as e:
        return [str(e)]


def build_prediction_request(data: dict, request_id: int) -> PricePredictionRequest:
    """Build a PricePredictionRequest from sample data with the given id."""
    return PricePredictionRequest.model_validate({**data, 'id': request_id})


# Human-readable labels for key display fields
DISPLAY_FIELDS = [
    ('neighborhood', 'Neighborhood'),
    ('house_style', 'Style'),
    ('overall_qual', 'Quality'),
    ('overall_cond', 'Condition'),
    ('year_built', 'Year Built'),
    ('gr_liv_area', 'Living Area'),
    ('first_flr_sf', '1st Floor'),
    ('second_flr_sf', '2nd Floor'),
    ('total_bsmt_sf', 'Basement'),
    ('bedroom_abv_gr', 'Bedrooms'),
    ('full_bath', 'Full Baths'),
    ('half_bath', 'Half Baths'),
    ('kitchen_abv_gr', 'Kitchens'),
    ('tot_rms_abv_grd', 'Total Rooms'),
    ('garage_cars', 'Garage Cars'),
    ('garage_area', 'Garage Area'),
    ('fireplaces', 'Fireplaces'),
    ('lot_area', 'Lot Size'),
    ('wood_deck_sf', 'Deck'),
    ('open_porch_sf', 'Porch'),
]

# Fields with special formatting
_SUFFIX_SF = {
    'gr_liv_area',
    'first_flr_sf',
    'second_flr_sf',
    'total_bsmt_sf',
    'garage_area',
    'lot_area',
    'wood_deck_sf',
    'open_porch_sf',
}


def format_value(key: str, value) -> str:
    """Format a field value for display."""
    if value is None:
        return 'N/A'
    if key in _SUFFIX_SF:
        return f'{value:,} sqft'
    if key in ('overall_qual', 'overall_cond'):
        return f'{value}/10'
    return str(value)


def render_sample_summary(sample_data: dict):
    """Render a compact summary of the selected property."""
    cols = st.columns(len(DISPLAY_FIELDS))
    for (key, label), col in zip(DISPLAY_FIELDS, cols):
        with col:
            st.markdown(f'**{label}**')
            st.markdown(format_value(key, sample_data.get(key)))


def render_full_details(sample_data: dict):
    """Render all fields in an expandable table."""
    rows = []
    for key, value in sample_data.items():
        display_key = key.replace('_', ' ').title()
        display_value = format_value(key, value) if value is not None else 'N/A'
        rows.append([display_key, display_value])
    st.dataframe(rows, column_config={'0': 'Field', '1': 'Value'}, width='stretch')


# ---------------------------------------------------------------------------
# Streamlit App
# ---------------------------------------------------------------------------


def main():
    st.set_page_config(page_title='Housing Price Predictor', layout='wide')
    st.title('Housing Price Prediction')

    # Lazily create the orchestrator client once per session
    if 'client' not in st.session_state:
        settings = UIConfigSettings()
        st.session_state.client = OrchestratorClient(base_url=settings.orchestrator_url)
    client = st.session_state.client

    # Load samples
    samples = load_samples()
    sample_labels = [s['label'] for s in samples]

    # Sidebar selector
    st.sidebar.header('Select a Property')
    st.sidebar.markdown('Choose a sample property from the test set to predict its price.')
    selected_label = st.sidebar.selectbox('Property', sample_labels, index=2)
    selected_sample = next(s for s in samples if s['label'] == selected_label)
    sample_data = selected_sample['data']

    # Property header
    st.subheader(f'Property #{sample_data["id"]}')
    st.caption(selected_sample['label'])

    # Summary cards
    st.markdown('---')
    st.markdown('### Property Overview')
    render_sample_summary(sample_data)

    # Full details (collapsible)
    with st.expander('View All Fields'):
        render_full_details(sample_data)

    # Predict button
    st.markdown('---')
    predict_col, _ = st.columns([1, 4])
    with predict_col:
        submitted = st.button('Predict Price', type='primary', width='stretch')

    if submitted:
        # Build the request using the sample's actual id
        request_id = sample_data['id']
        errors = validate_prediction_request(sample_data)
        if errors:
            st.error('Validation errors:')
            for err in errors:
                st.text(err)
            return

        request = build_prediction_request(sample_data, request_id=request_id)

        with st.spinner('Predicting price...'):
            result = client.predict(request)

        st.success(f'**Predicted Price:** {format_price(result.predicted_price)}')


if __name__ == '__main__':
    main()
