import requests

from ..conftest import server, port

BASE_URL = f"{server}:{port}/functions"
function_id = None


def test_create_new_function():
    global function_id
    payload = {
        "function": {
            "name": "RandomForestRegressor",
            "description": "A random forest regressor",
            "function_reference": "sklearn.ensemble.RandomForestRegressor",
        },
        "parameters": [
            {"name": "n_estimators", "value": "100", "parameter_type": "float"},
            {"name": "max_depth", "value": "3.0", "parameter_type": "float"},
            {"name": "min_samples_split", "value": "2.0", "parameter_type": "float"},
        ],
    }

    response = requests.post(f"{BASE_URL}/", json=payload)
    assert response.status_code == 201
    response_data = response.json()

    # Validate response structure
    assert "id" in response_data["function"]

    # Store IDs for later tests
    function_id = response_data["function"]["id"]


def test_get_function_by_id():
    response = requests.get(f"{BASE_URL}/{function_id}")
    assert response.status_code == 200
    response_data = response.json()

    # Validate response structure
    assert "function" in response_data
    assert "parameters" in response_data

    # Validate function data
    assert isinstance(response_data["function"]["name"], str)
    assert isinstance(response_data["function"]["description"], str)

    # Validate parameters
    assert len(response_data["parameters"]) == 3
    for param in response_data["parameters"]:
        assert param["parameter_type"] == "float"


def test_get_all_functions():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    functions = response.json()

    assert isinstance(functions, list)
    if function_id:  # Only check if we've created a function
        assert any(func["function"]["id"] == function_id for func in functions)
        our_function = next(
            func for func in functions if func["function"]["id"] == function_id
        )
        assert our_function["function"]["name"] == "RandomForestRegressor"


def test_delete_function():
    # First create a function to delete
    create_payload = {
        "function": {
            "name": "TemporaryFunction",
            "description": "Will be deleted",
            "function_reference": "test.TemporaryFunction",
        },
        "parameters": [
            {"name": "temp_param", "value": "1.0", "parameter_type": "float"}
        ],
    }
    create_response = requests.post(f"{BASE_URL}/", json=create_payload)
    temp_function_id = create_response.json()["function"]["id"]

    # Now delete it
    delete_response = requests.delete(f"{BASE_URL}/{temp_function_id}")
    assert delete_response.status_code == 200

    # Verify deletion
    get_response = requests.get(f"{BASE_URL}/{temp_function_id}")
    assert get_response.status_code == 404


def test_invalid_function_creation():
    # Test missing required fields
    invalid_payloads = [
        {
            "function": {"name": "MissingFields"}
        },  # Missing description and function_reference
        {"function": {"description": "NoName"}},  # Missing name
        {"parameters": [{"name": "OnlyParams"}]},  # Missing function
        {
            "function": {
                "name": "Valid",
                "description": "Valid",
                "function_reference": "valid.ref",
            },
            "parameters": [
                {"name": "invalid_param"}
            ],  # Missing value and parameter_type
        },
    ]

    for payload in invalid_payloads:
        response = requests.post(f"{BASE_URL}/", json=payload)
        assert response.status_code == 422  # Unprocessable Entity
