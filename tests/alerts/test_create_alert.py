import json


def test_create_alert_correct_attributes(client):
    new_alert = {"email": "new@example.com", "threshold": 42000}
    response = client.post(
        "/api/alerts", data=json.dumps(new_alert), content_type="application/json"
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert data["data"]["alert"]["email"] == "new@example.com"


def test_create_alert_no_email(client):
    new_alert = {"threshold": 42000}
    response = client.post(
        "/api/alerts", data=json.dumps(new_alert), content_type="application/json"
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["status"] == "fail"


def test_create_alert_invalid_threshold(client):
    new_alert = {"email": "x@example.com", "threshold": "not-a-number"}
    response = client.post(
        "/api/alerts", data=json.dumps(new_alert), content_type="application/json"
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["status"] == "fail"
