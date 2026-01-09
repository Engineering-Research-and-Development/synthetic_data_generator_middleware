def test_delete_entire_trained_model(client):
    models = client.get("/trained_models/").json()["models"]
    assert len(models) > 0

    model_id = models[0]["model"]["id"]

    response = client.delete(f"/trained_models/{model_id}")

    assert response.status_code == 200
    assert response.json() == model_id


def test_delete_specific_model_version(client):
    payload = {
        "model": {
            "_id": 888,
            "name": "TempModel",
            "dataset_name": "tmp",
            "size": "1GB",
            "input_shape": "(1,)",
            "algorithm": 1,
        },
        "version": {
            "_id": 1,
            "version_name": "temp_v1",
            "image_path": "/tmp",
            "loss_function": "mse",
            "train_loss": 0.9,
            "val_loss": 1.0,
            "train_samples": 10,
            "val_samples": 5,
            "_trained_model": 888,
        },
        "datatypes": [],
    }

    create = client.post("/trained_models/", json=payload)
    model_id = create.json()["trained_model_id"]

    response = client.delete(
        f"/trained_models/{model_id}",
        params={"version_name": "temp_v1"},
    )

    assert response.status_code == 200
    assert response.json() == "temp_v1"


def test_delete_trained_model_not_found(client):
    response = client.delete("/trained_models/999999")

    assert response.status_code == 404
    assert response.json() == "Trained model not found"
