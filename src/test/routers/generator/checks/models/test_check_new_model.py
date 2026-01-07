from unittest.mock import MagicMock

import peewee

from routers.generator.checks.models import check_new_model
from routers.generator.validation_schema import ModelOutput


def test_check_new_model_success(monkeypatch):
    """
    Given Algorithm.get returns a valid Algorithm
    When check_new_model is called
    Then it should return a ModelOutput instance
    """

    dummy_algorithm = MagicMock()
    dummy_algorithm.name = "XGBoost"

    def mock_get(*args, **kwargs):
        return dummy_algorithm

    monkeypatch.setattr(
        "database.schema.Algorithm.get",
        mock_get,
    )

    result = check_new_model(
        new_model=1,
        model_name="my-custom-model",
    )

    assert isinstance(result, ModelOutput)
    assert result.algorithm_name == "XGBoost"
    assert result.model_name == "my-custom-model"


def test_check_new_model_not_found(monkeypatch):
    """
    Given Algorithm.get raises DoesNotExist
    When check_new_model is called
    Then it should return an empty dictionary
    """

    def mock_get(*args, **kwargs):
        raise peewee.DoesNotExist()

    monkeypatch.setattr(
        "database.schema.Algorithm.get",
        mock_get,
    )

    result = check_new_model(
        new_model=999,
        model_name="unknown-model",
    )

    assert result == {}
