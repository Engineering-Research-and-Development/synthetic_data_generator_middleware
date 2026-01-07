import pytest

from routers.generator.checks.features import handle_features_creation
from routers.generator.validation_schema import (
    ModelOutput,
    FunctionDataOut,
    GeneratorDataOutput,
)


@pytest.fixture
def valid_model():
    return ModelOutput(
        algorithm_name="xgboost",
        model_name="test-model",
    )


@pytest.fixture
def function_data_out():
    return [
        FunctionDataOut(
            feature="feature_1",
            function_reference="fn_ref",
            parameters=[],
        )
    ]


@pytest.fixture
def base_data():
    return {
        "additional_rows": 100,
        "functions": [{"dummy": "value"}],
        "features_created": [{"feature": "f1"}],
    }


def test_handle_feature_creation_success(
    monkeypatch,
    base_data,
    function_data_out,
    valid_model,
):
    """
    Given compatible features and functions
    When handle_feature_creation is called
    Then it should return GeneratorDataOutput and empty error
    """

    def mock_check(features_created, functions):
        assert features_created == base_data["features_created"]
        assert functions == base_data["functions"]
        return True, None

    monkeypatch.setattr(
        "routers.generator.checks.features.check_features_created_types",
        mock_check,
    )

    result, error = handle_features_creation(
        data=base_data,
        function_data=function_data_out,
        model=valid_model,
    )

    assert error == ""
    assert isinstance(result, GeneratorDataOutput)

    assert result.functions == function_data_out
    assert result.n_rows == base_data["additional_rows"]
    assert result.model == valid_model
    assert result.dataset is None


def test_handle_feature_creation_failure(
    monkeypatch,
    base_data,
    function_data_out,
    valid_model,
):
    """
    Given incompatible features and functions
    When handle_feature_creation is called
    Then it should return None and a meaningful error message
    """

    def mock_check(features_created, functions):
        return False, "feature_x"

    monkeypatch.setattr(
        "routers.generator.checks.features.check_features_created_types",
        mock_check,
    )

    result, error = handle_features_creation(
        data=base_data,
        function_data=function_data_out,
        model=valid_model,
    )

    assert result is None
    assert "not compatible" in error
    assert "feature_x" in error


def test_handle_feature_creation_without_features_created(
    monkeypatch,
    base_data,
    function_data_out,
    valid_model,
):
    """
    Given features_created is None
    And check_features_created_types returns success
    Then the function should still succeed
    """

    base_data["features_created"] = None

    def mock_check(features_created, functions):
        assert features_created is None
        return True, None

    monkeypatch.setattr(
        "routers.generator.checks.features.check_features_created_types",
        mock_check,
    )

    result, error = handle_features_creation(
        data=base_data,
        function_data=function_data_out,
        model=valid_model,
    )

    assert error == ""
    assert isinstance(result, GeneratorDataOutput)
