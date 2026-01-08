def test_delete_function(client):
    payload = {
        "function": {
            "_id": 999,
            "name": "TempFunction",
            "description": "Temporary function",
            "function_reference": "temp.ref",
        },
        "parameters": [
            {"_id": 999, "name": "temp_param", "value": "1", "parameter_type": "int"}
        ],
    }

    create_response = client.post("/functions/", json=payload)
    function_id = create_response.json()["function"]["id"]

    delete_response = client.delete(f"/functions/{function_id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == "ok"


def test_delete_function_not_existing(client):
    response = client.delete("/functions/999999")

    assert response.status_code == 200
    assert response.json() == "ok"
