def test_create_trained_model_success(client):
    payload = {
        "model": {
            "_id": 1,
            "name": "ImageClassifier",
            "dataset_name": "ImageNet",
            "size": "100GB",
            "input_shape": "(3,224,224)",
            "algorithm": 1,
        },
        "version": {
            "_id": 1,
            "version_name": "v1",
            "image_path": "/models/v1",
            "loss_function": "cross_entropy",
            "train_loss": 0.2,
            "val_loss": 0.25,
            "train_samples": 10000,
            "val_samples": 2000,
            "_trained_model": 1,
        },
        "datatypes": [
            {
                "_id": 1,
                "type": "float",
                "is_categorical": False,
                "feature_name": "pixel",
                "feature_position": 0,
                "feature_type": "numeric",
                "feature_size": "1",
            }
        ],
    }

    response = client.post("/trained_models/", json=payload)

    assert response.status_code == 201
    body = response.json()

    assert "trained_model_id" in body
    assert "model_version_id" in body


def test_create_trained_model_algorithm_not_found(client):
    payload = {
        "model": {
            "_id": 999,
            "name": "BrokenModel",
            "dataset_name": "X",
            "size": "1GB",
            "input_shape": "(1,)",
            "algorithm": 999999,
        },
        "version": {
            "_id": 1,
            "version_name": "v1",
            "image_path": "/broken",
            "loss_function": "mse",
            "train_loss": 1.0,
            "val_loss": 1.1,
            "train_samples": 10,
            "val_samples": 5,
            "_trained_model": 999,
        },
        "datatypes": [],
    }

    response = client.post("/trained_models/", json=payload)

    assert response.status_code == 404
    assert response.json() == "Algorithm not found"


def test_create_new_version_existing_model(client):
    payload = {
        "model": {
            "_id": 1,
            "name": "ImageClassifier",  # already exists
            "dataset_name": "ImageNet",
            "size": "100GB",
            "input_shape": "(3,224,224)",
            "algorithm": 1,
        },
        "version": {
            "_id": 2,
            "version_name": "v2",
            "image_path": "/models/v2",
            "loss_function": "cross_entropy",
            "train_loss": 0.15,
            "val_loss": 0.2,
            "train_samples": 12000,
            "val_samples": 3000,
            "_trained_model": 1,
        },
        "datatypes": [],  # ignored if model exists
    }

    response = client.post("/trained_models/", json=payload)

    assert response.status_code == 201
    body = response.json()

    assert "trained_model_id" in body
    assert "model_version_id" in body
