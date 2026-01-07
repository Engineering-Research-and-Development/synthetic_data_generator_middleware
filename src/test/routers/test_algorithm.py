import requests

from ..conftest import port, server

BASE_URL = f"{server}:{port}/algorithms"
algo_id = None


def test_create_new_algorithm():
    global algo_id
    payload = {
        "algorithm": {
            "name": "Test Algorithm",
            "description": "A test algorithm",
            "default_loss_function": "mse",
        },
        "datatypes": [{"type": "float", "is_categorical": False}],
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201
    assert "id" in response.json()
    algo_id = response.json()["id"]


def test_get_algorithm_by_id():
    algorithm_id = algo_id
    response = requests.get(f"{BASE_URL}/{algorithm_id}")
    assert response.status_code == 200
    assert "algorithm" in response.json()
    assert "datatypes" in response.json()


def test_get_all_algorithms():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json().get("algorithms"), list)


def test_delete_algorithm():
    algorithm_id = algo_id
    response = requests.delete(f"{BASE_URL}/{algorithm_id}")
    assert response.status_code == 200


def test_get_algorithm_wrong_id():
    algorithm_id = 999999
    response = requests.get(f"{BASE_URL}/{algorithm_id}")
    assert response.status_code == 404
