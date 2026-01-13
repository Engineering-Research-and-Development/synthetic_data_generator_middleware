from .common import (
    _get_existing_parameter_type,
    _get_existing_function_ids,
)
from routers.generator.checks.features import handle_features_creation
from routers.generator.validation_schema import GeneratorDataOutput, ModelOutput


def test_handle_features_creation_success():
    function_ids = _get_existing_function_ids()
    valid_type = _get_existing_parameter_type()

    data = {
        "data": {
            "input_type": "features_created",
            "features_created": [
                {"name": "f1", "type": valid_type},
            ],
        },
        "functions": function_ids,
        "additional_rows": 100,
    }

    function_data = []  # allowed
    model = ModelOutput(algorithm_name="dummy_model", model_name="dummy_name")

    output, error = handle_features_creation(
        data["data"]["features_created"], function_data, model, data["additional_rows"]
    )

    assert error == ""
    assert isinstance(output, GeneratorDataOutput)
    assert output.model == model
    assert output.n_rows == 100
    assert output.functions == function_data


def test_handle_features_creation_incompatible_types():
    function_ids = _get_existing_function_ids()

    data = {
        "data": {
            "input_type": "features_created",
            "features_created": [
                {"name": "f1", "type": "invalid_type"},
            ],
        },
        "functions": function_ids,
    }
    model = ModelOutput(algorithm_name="dummy_model", model_name="dummy_name")
    function_data = []  # allowed
    output, error = handle_features_creation(
        data["data"]["features_created"], function_data, model, 100
    )

    assert output is None
    assert "not compatible" in error
    assert "invalid_type" in error


def test_handle_features_creation_none_function_data():
    function_ids = _get_existing_function_ids()
    valid_type = _get_existing_parameter_type()

    data = {
        "data": {
            "input_type": "features_created",
            "features_created": [
                {"name": "f1", "type": valid_type},
            ],
        },
        "functions": function_ids,
        "additional_rows": 100,
    }
    model = ModelOutput(algorithm_name="dummy_model", model_name="dummy_name")
    output, error = handle_features_creation(
        data["data"]["features_created"], None, model, data["additional_rows"]
    )

    assert error == ""
    assert isinstance(output, GeneratorDataOutput)
    assert output.functions is None
