from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_deployment_plan():
    response = client.post(
        "/deployment/plan",
        json={"request": "Deploy a Python FastAPI application using Docker"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["request"] == "Deploy a Python FastAPI application using Docker"
    assert "AegisOps AI" in data["plan"]
    assert "Deployment request:" in data["plan"]
