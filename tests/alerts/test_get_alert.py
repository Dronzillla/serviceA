import json


def test_get_alert_by_id(client, init_database):
    response = client.get("/api/alerts/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert data["data"]["alert"]["id"] == 1


def test_get_nonexistent_alert_by_id(client):
    response = client.get("/api/alerts/999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["status"] == "fail"
    assert data["data"]["alert"] == "Alert does not exist"
