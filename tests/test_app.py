import pytest
import json

def test_index_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Hello!"

def test_healthcheck_endpoint(client):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Service is up and running!"

def test_rates_endpoint(client):
    response = client.get("/rates?date_from=2016-01-01&date_to=2016-01-04&origin=CNSGH&destination=north_europe_main")
    assert response.status_code == 200
    assert json.loads(response.data.decode("utf-8")) == [
        {"day": "2016-01-01", "average_price": 1112},
        {"day": "2016-01-02", "average_price": 1112},
        {"day": "2016-01-03", "average_price": None},
        {"day": "2016-01-04", "average_price": None},
    ]