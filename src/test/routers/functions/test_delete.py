def test_delete_function(client):
    payload = {
        "function": {
            "_id": 999,
            "name": "TempFunction",
            "description": "Temporary function",
            "function_reference": "temp.ref",
            "is_generative": False,
            "priority": 1,
        },
        "parameters": [
            {"_id": 999, "name": "temp_param", "value": "1", "parameter_type": "int"}
        ],
    }

    create_response = client.post("/functions/", json=payload)
    function_id = create_response.json()["function"]["id"]

    delete_response = client.delete(f"/functions/{function_id}")

    assert delete_response.status_code == 204


def test_delete_function_not_existing(client):
    response = client.delete("/functions/999999")

    assert response.status_code == 404


def test_get_function_negative(client):
    response = client.get("/functions/-1")
    assert response.status_code == 422
