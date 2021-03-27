import requests
import json
import pytest


@pytest.mark.integration
def test_update():
    headers = {'Content-Type': 'application/json',}
    user_payload= {"user_id":"1"}
    response = requests.post("http://localhost:8008/update", headers=headers, data=json.dumps(user_payload))
    assert response.status_code == 200
    payload = json.loads(response.text)
    print(payload.keys())
    assert "user_data" in payload
    assert set(["shares", "cash", "bid", "offer"]).issubset(set(payload["user_data"].keys()))

    
    user_payload= {"user_id": "1", "bid":{"price": 1, "quantity": 10}}
    response = requests.post("http://localhost:8008/update", headers=headers, data=json.dumps(user_payload))
    payload = json.loads(response.text)
    assert payload["user_data"]["bid"]["price"] == 1
