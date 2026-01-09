def test_get_all_algorithms(client):
    response = client.get("/algorithms/")

    assert response.status_code == 200
    body = response.json()
    assert "algorithms" in body
    assert isinstance(body["algorithms"], list)

    if body["algorithms"]:
        algo = body["algorithms"][0]
        assert "id" in algo
        assert "name" in algo
        assert "description" in algo
        assert "default_loss_function" in algo


def test_get_algorithm_by_id_success(client):
    # first retrieve a valid ID
    list_response = client.get("/algorithms/")
    algorithms = list_response.json()["algorithms"]
    assert len(algorithms) > 0

    algorithm_id = algorithms[0]["id"]

    response = client.get(f"/algorithms/{algorithm_id}")

    assert response.status_code == 200
    body = response.json()

    assert "algorithm" in body
    assert "datatypes" in body

    algorithm = body["algorithm"]
    assert algorithm["id"] == algorithm_id
    assert "name" in algorithm
    assert "description" in algorithm

    datatypes = body["datatypes"]
    assert isinstance(datatypes, list)


def test_get_algorithm_by_id_not_found(client):
    response = client.get("/algorithms/999999")

    assert response.status_code == 404
    assert response.json() == "Algorithm not found"
