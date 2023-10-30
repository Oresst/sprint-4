import pytest
from fastapi.testclient import TestClient

from main import app


endpoints = [
    '/api/v1/films/',
    '/api/v1/films/6fddb231-8127-42f0-81e5-f53a806c2ae8',
    '/api/v1/films/6fddb231-8127-42f0-81e5-f53a806c2ae8/alike',
    '/api/v1/genres/',
    '/api/v1/genres/3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
    '/api/v1/genres/action/popular',
    '/api/v1/persons/',
    '/api/v1/persons/466c8350-fda7-44b4-a08f-afceaa16bc31',
    '/api/v1/persons/466c8350-fda7-44b4-a08f-afceaa16bc31/film',
]

client = TestClient(app)


@pytest.mark.parametrize('endpoint', endpoints)
def test_status(endpoint: str):
    response = client.get(endpoint)
    assert response.status_code == 200
