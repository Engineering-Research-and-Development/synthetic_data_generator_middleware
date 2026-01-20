def test_create_new_function_success(client):
    payload = {
        "function": {
            "_id": 1,
            "name": "Normalize",
            "description": "Normalize values",
            "function_reference": "sklearn.preprocessing.normalize",
            "is_generative": False,
            "priority": 1
        },
        "parameters": [
            {"_id": 1, "name": "norm", "value": "l2", "parameter_type": "string"}
        ],
    }

    response = client.post("/functions/", json=payload)

    assert response.status_code == 201
    body = response.json()

    assert "function" in body
    function = body["function"]

    assert "id" in function
    assert function["name"] == "Normalize"


def test_create_function_already_existing(client):
    payload = {
        "function": {
            "_id": 1,
            "name": "Normalize",  # already created
            "description": "Normalize values",
            "function_reference": "sklearn.preprocessing.normalize",
            "is_generative": False,
            "priority": 1
        },
        "parameters": [
            {"_id": 2, "name": "axis", "value": "1", "parameter_type": "int"}
        ],
    }

    response = client.post("/functions/", json=payload)

    assert response.status_code == 201
    body = response.json()

    assert "function" in body
    assert body["function"]["name"] == "Normalize"
