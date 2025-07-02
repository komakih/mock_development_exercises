from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_documents():
    response = client.post("/documents/search", json={
        "query_text": "返品方法を教えてください",
        "n_results": 2
    })
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) <= 2
    for result in data["results"]:
        assert "id" in result
        assert "content" in result
