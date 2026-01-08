def test_create_new_algorithm_success(client):
    payload = {
        "algorithm": {
            "_id": 1,
            "name": "RandomForest",
            "description": "Tree ensemble algorithm",
            "default_loss_function": "gini",
        },
        "datatypes": [{"_id": 1, "type": "float", "is_categorical": False}],
    }

    response = client.post("/algorithms/", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert isinstance(body["id"], int)
    assert body["id"] > 0


def test_create_algorithm_already_existing(client):
    payload = {
        "algorithm": {
            "_id": 1,
            "name": "RandomForest",  # already created above
            "description": "Tree ensemble algorithm",
            "default_loss_function": "gini",
        },
        "datatypes": [{"_id": 1, "type": "float", "is_categorical": False}],
    }

    response = client.post("/algorithms/", json=payload)

    # get_or_create → still returns existing id
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
