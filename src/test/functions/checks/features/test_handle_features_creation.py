from .common import (
    _get_existing_parameter_type,
    _get_existing_function_ids,
)
from routers.generator.checks.functions import handle_data_function_mapping
from routers.generator.validation_schema.shared import (
    SupportedDatatypesCategory,
)
from routers.generator.validation_schema.output import ParametersOut, FunctionDataOut


def test_handle_features_creation_success():
    function_ids = _get_existing_function_ids()
    valid_type = _get_existing_parameter_type()

    data = [
        {
            "name": "f1",
            "type": valid_type,
            "category": SupportedDatatypesCategory.categorical,
            "associated_functions": [
                {
                    "function_id": function_ids[0],
                    "parameters": [{"param_id": 1, "value": "test_value"}],
                }
            ],
        },
        {
            "name": "f2",
            "type": valid_type,
            "category": SupportedDatatypesCategory.categorical,
            "associated_functions": [
                {
                    "function_id": function_ids[0],
                    "parameters": [{"param_id": 1, "value": "test_value"}],
                }
            ],
        },
    ]

    function_data = [
        {
            "feature_name": "f1",
            "associated_functions": [
                {
                    "function_id": function_ids[0],
                    "parameters": [{"param_id": 1, "value": "test_value"}],
                }
            ],
        }
    ]

    output, error = handle_data_function_mapping(data, function_data)

    assert error == ""
    assert isinstance(output, list)
    assert len(output) == 1
    assert isinstance(output[0], FunctionDataOut)
    assert output[0].feature == "f1"
    assert output[0].function_reference is not None
    assert len(output[0].parameters) == 1
    assert isinstance(output[0].parameters[0], ParametersOut)
    assert output[0].parameters[0].value == "test_value"


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
    function_data = [
        {
            "feature_name": "f1",
            "associated_functions": [
                {
                    "function_id": function_ids[0],
                    "parameters": [{"param_id": 1, "value": "test_value"}],
                }
            ],
        }
    ]

    output, error = handle_data_function_mapping(
        data["data"]["features_created"], function_data
    )

    assert output is None
    assert "not compatible" in error
    assert "invalid_type" in error


def test_handle_features_creation_empty_function_data():
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

    function_data = []

    output, error = handle_data_function_mapping(
        data["data"]["features_created"], function_data
    )

    assert error == ""
    assert isinstance(output, list)
    assert len(output) == 0


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

    function_data = None

    output, error = handle_data_function_mapping(
        data["data"]["features_created"], function_data
    )

    assert error == ""
    assert isinstance(output, list)
    assert len(output) == 0
