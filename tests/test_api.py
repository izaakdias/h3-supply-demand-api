from fastapi.testclient import TestClient

from h3_supply_demand.api import app
from h3_supply_demand.service import build_snapshot, classify


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_h3_cell_and_explainable_fields():
    response = client.post(
        "/v1/supply-demand/predict",
        json={"latitude": -22.9068, "longitude": -43.1729, "resolution": 8},
    )
    body = response.json()
    assert response.status_code == 200
    assert len(body["h3_index"]) > 0
    assert 0 <= body["demand_score"] <= 1
    assert body["demand_level"] == classify(body["demand_score"])
    assert body["open_requests"] >= 0
    assert body["active_drivers"] >= 0


def test_same_cell_is_reproducible():
    first = build_snapshot(-22.9068, -43.1729, 8)
    second = build_snapshot(-22.9068, -43.1729, 8)
    assert first == second
