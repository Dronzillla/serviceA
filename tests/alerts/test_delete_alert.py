import json


def test_delete_alert_correct_attributes(client, init_database):
    response = client.delete("/api/alerts/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"

    # Verify that the alert is actually deleted
    response = client.get("/api/alerts/1")
    assert response.status_code == 404


def test_delete_nonexistent_alert(client):
    response = client.delete("/api/alerts/999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["status"] == "fail"
