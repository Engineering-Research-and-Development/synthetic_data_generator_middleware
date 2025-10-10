import requests
import pytest

from conftest import middleware, load_jsons
from algorithms import get_algorithms_available
from trained_models import (
    check_pushed_models,
    get_trained_models,
    get_versions_by_trained_model_name,
    get_trained_model_id_by_trained_model_name,
)

url = middleware + "/sdg_input/"


@pytest.mark.order1
@pytest.mark.parametrize(
    "filename,payload", load_jsons("../resources/no_functions/sdg_input")
)
def test_train_sdg_input(filename, payload):
    algorithms_available = get_algorithms_available()
    model_id = list(algorithms_available.keys())[
        list(algorithms_available.values()).index(payload["test"])
    ]
    payload.pop("test")
    payload["ai_model"]["selected_model_id"] = model_id
    response = requests.post(url, json=payload)
    assert response.status_code == 200, (
        f"Failed on file: {filename} with status code {response.status_code} and body: {response.text}"
    )

    check_pushed_models()


@pytest.mark.order2
@pytest.mark.parametrize(
    "filename,payload", load_jsons("../resources/no_functions/sdg_input")
)
def test_infer_sdg_input(filename, payload):
    trained_models = get_trained_models()

    payload.pop("test")
    payload["ai_model"]["new_model"] = False
    payload["ai_model"]["model_version"] = get_versions_by_trained_model_name(
        trained_models, payload["ai_model"]["new_model_name"]
    )[-1]
    model_id = get_trained_model_id_by_trained_model_name(
        trained_models, payload["ai_model"]["new_model_name"]
    )[0]
    payload["ai_model"]["selected_model_id"] = model_id
    response = requests.post(url, json=payload)
    assert response.status_code == 200, (
        f"Failed on file: {filename} with status code {response.status_code} and body: {response.text}"
    )
