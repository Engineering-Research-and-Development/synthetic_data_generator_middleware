def test_get_all_trained_models(client):
    response = client.get("/trained_models/")

    assert response.status_code == 200
    body = response.json()

    assert "models" in body
    assert isinstance(body["models"], list)

    if body["models"]:
        item = body["models"][0]

        assert "model" in item
        assert "versions" in item

        model = item["model"]
        assert "id" in model
        assert "name" in model
        assert "dataset_name" in model
        assert "algorithm" in model

        versions = item["versions"]
        assert isinstance(versions, list)


def test_get_trained_model_by_id_success(client):
    models = client.get("/trained_models/").json()["models"]
    assert len(models) > 0

    model_id = models[0]["model"]["id"]

    response = client.get(f"/trained_models/{model_id}")

    assert response.status_code == 200
    body = response.json()

    assert "model" in body
    assert "versions" in body
    assert "datatypes" in body

    assert body["model"]["id"] == model_id

    assert isinstance(body["versions"], list)
    assert isinstance(body["datatypes"], list)

    if body["datatypes"]:
        dtype = body["datatypes"][0]
        assert "type" in dtype
        assert "is_categorical" in dtype
        assert "feature_name" in dtype
        assert "feature_position" in dtype


def test_get_trained_model_by_id_not_found(client):
    response = client.get("/trained_models/999999")

    assert response.status_code == 404
    assert response.json()["message"] == "Model not found"
