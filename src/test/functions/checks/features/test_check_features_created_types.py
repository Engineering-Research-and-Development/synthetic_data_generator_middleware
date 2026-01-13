from .common import (
    _get_existing_function_ids,
    _get_existing_parameter_type,
)
from routers.generator.checks.features import (
    check_features_created_types,
)


def test_check_features_created_types_success():
    function_ids = _get_existing_function_ids()
    valid_type = _get_existing_parameter_type()

    features = [
        {"name": "f1", "type": valid_type},
        {"name": "f2", "type": valid_type},
    ]

    result, error = check_features_created_types(features, function_ids)

    assert result is True
    assert error is None


def test_check_features_created_types_invalid_feature_type():
    function_ids = _get_existing_function_ids()
    valid_type = _get_existing_parameter_type()

    features = [
        {"name": "f1", "type": valid_type},
        {"name": "f2", "type": "non_existing_type"},
    ]

    result, error = check_features_created_types(features, function_ids)

    assert result is False
    assert error == "non_existing_type"


def test_check_features_created_types_empty_features():
    function_ids = _get_existing_function_ids()

    result, error = check_features_created_types([], function_ids)

    assert result is True
    assert error is None


def test_check_features_created_types_no_functions_selected():
    valid_type = _get_existing_parameter_type()

    features = [{"name": "f1", "type": valid_type}]

    result, error = check_features_created_types(features, [])

    assert result is True
