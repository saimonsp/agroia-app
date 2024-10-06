from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_area():
    response = client.post("/areas/", json={"hectares": 10, "radius": 100, "latitude": 12.34, "longitude": 56.78})
    assert response.status_code == 200
    assert response.json()["hectares"] == 10
