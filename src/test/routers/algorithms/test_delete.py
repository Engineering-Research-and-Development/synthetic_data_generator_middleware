def test_delete_algorithm(client):
    # create a new algorithm to delete
    payload = {
        "algorithm": {
            "_id": 999,
            "name": "TempAlgo",
            "description": "Temporary algorithm",
            "default_loss_function": "mse",
        },
        "datatypes": [{"_id": 2, "type": "int", "is_categorical": False}],
    }

    create_response = client.post("/algorithms/", json=payload)
    algorithm_id = create_response.json()["id"]

    delete_response = client.delete(f"/algorithms/{algorithm_id}")

    assert delete_response.status_code == 204


def test_delete_non_existing_algorithm(client):
    response = client.delete("/algorithms/999999")

    assert response.status_code == 204
