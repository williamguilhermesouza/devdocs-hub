from fastapi.testclient import TestClient
from devdocs_hub.api.main import app

client = TestClient(app)

class TestHealth:
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == { "status" : "ok" }

