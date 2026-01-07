from routers.generator.checks.features import check_features_created_types
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_peewee_chain(monkeypatch):
    """
    Mock realistico della catena Peewee:

    Parameter
      .select()
      .join(FunctionParameter)
      .where(FunctionParameter.function << function_ids)
      .dicts()

    Ritorna righe compatibili con la tabella Parameter.
    """

    # Dummy rows coerenti con la tabella reale
    dummy_rows = [
        {
            "id": 1,
            "name": "learning_rate",
            "value": "0.1",
            "parameter_type": "float32",
        },
        {
            "id": 2,
            "name": "n_estimators",
            "value": "100",
            "parameter_type": "int32",
        },
    ]

    # Ultimo oggetto della chain (query)
    mock_query = MagicMock()
    mock_query.dicts.return_value = dummy_rows

    # Costruiamo la chain al contrario
    mock_where = MagicMock(return_value=mock_query)
    mock_join = MagicMock(return_value=MagicMock(where=mock_where))
    mock_select = MagicMock(return_value=MagicMock(join=mock_join))

    monkeypatch.setattr(
        "database.schema.Parameter.select",
        mock_select,
    )

    return mock_query


def test_check_features_created_types_success_single_feature(
    mock_peewee_chain,
):
    """
    Given one feature and one compatible function parameter
    Then the function should return (True, None)
    """

    mock_peewee_chain.dicts.return_value = [{"parameter_type": "float32"}]

    features = [{"type": "float32"}]
    function_ids = [1]

    result, error = check_features_created_types(features, function_ids)

    assert result is True
    assert error is None


def test_check_features_created_types_success_multiple_features(
    mock_peewee_chain,
):
    """
    Given multiple features all compatible
    Then the function should return success
    """

    mock_peewee_chain.dicts.return_value = [
        {"parameter_type": "float32"},
        {"parameter_type": "int32"},
    ]

    features = [
        {"type": "float32"},
        {"type": "int32"},
    ]
    function_ids = [1, 2]

    result, error = check_features_created_types(features, function_ids)

    assert result is True
    assert error is None


def test_check_features_created_types_failure_first_incompatible(
    mock_peewee_chain,
):
    """
    Given a feature with incompatible type
    Then the function should fail immediately
    """

    mock_peewee_chain.dicts.return_value = [
        {
            "id": 1,
            "name": "learning_rate",
            "value": "0.1",
            "parameter_type": "float32",
        }
    ]

    features = [
        {"type": "string"},
        {"type": "float32"},  # should not be evaluated
    ]
    function_ids = [1]

    result, error = check_features_created_types(features, function_ids)

    assert result is False
    assert error == "string"


def test_check_features_created_types_empty_features(
    mock_peewee_chain,
):
    """
    Given no features created
    Then the function should always succeed
    """

    mock_peewee_chain.dicts.return_value = [
        {"parameter_type": "float32"},
    ]

    features = []
    function_ids = [1]

    result, error = check_features_created_types(features, function_ids)

    assert result is True
    assert error is None


def test_check_features_created_types_no_supported_params(
    mock_peewee_chain,
):
    """
    Given no parameters returned from DB
    Then any feature should be incompatible
    """

    mock_peewee_chain.dicts.return_value = []

    features = [{"type": "float32"}]
    function_ids = [1]

    result, error = check_features_created_types(features, function_ids)

    assert result is False
    assert error == "float32"
