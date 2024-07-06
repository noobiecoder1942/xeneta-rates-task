import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def wellformed_rates_query(date_from="2016-01-01", date_to="2016-01-04", origin="CNSGH", destination="north_europe_main"):
    return f"/rates?date_from={date_from}&date_to={date_to}&origin={origin}&destination={destination}"
