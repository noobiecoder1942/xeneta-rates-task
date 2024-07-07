import pytest
import json
from werkzeug.exceptions import BadRequest

def test_index_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Hello!"

def test_healthcheck_endpoint(client):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Service is up and running!"

def test_rates_endpoint_happy_path(client, wellformed_rates_query):
    response = client.get(wellformed_rates_query)
    assert response.status_code == 200
    assert json.loads(response.data.decode("utf-8")) == [
        {"day": "2016-01-01", "average_price": 1112},
        {"day": "2016-01-02", "average_price": 1112},
        {"day": "2016-01-03", "average_price": None},
        {"day": "2016-01-04", "average_price": None},
    ]

def test_rates_endpoint_sad_path(client):
    malformed_rates_query = "/rates?date_to=2016-13-10&origin=china_main&destination=scandinavia"
    response = client.get(malformed_rates_query)
    assert response.status_code == 400
    response_data = response.data.decode("utf-8")
    assert "Bad Request" in response_data
    assert "Invalid date_from argument" in response_data

    malformed_rates_query = "/rates?date_from=2016-01-10&origin=china_main&destination=scandinavia"
    response = client.get(malformed_rates_query)
    assert response.status_code == 400
    response_data = response.data.decode("utf-8")
    assert "Bad Request" in response_data
    assert "Invalid date_to argument" in response_data

    malformed_rates_query = "/rates?date_from=2016-01-01&date_to=2016-01-10&destination=scandinavia"
    response = client.get(malformed_rates_query)
    assert response.status_code == 400
    response_data = response.data.decode("utf-8")
    assert "Bad Request" in response_data
    assert "Invalid origin argument" in response_data

    malformed_rates_query = "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=china_main"
    response = client.get(malformed_rates_query)
    assert response.status_code == 400
    response_data = response.data.decode("utf-8")
    assert "Bad Request" in response_data
    assert "Invalid destination argument" in response_data

    malformed_rates_query = "/rates?date_from=2016-01-02&date_to=2016-01-01&origin=china_main"
    response = client.get(malformed_rates_query)
    assert response.status_code == 400
    response_data = response.data.decode("utf-8")
    assert "Bad Request" in response_data
    assert "Invalid date range: date_to must be later than date_from" in response_data