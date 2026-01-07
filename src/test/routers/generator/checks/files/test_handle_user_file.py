from unittest.mock import MagicMock

from routers.generator.checks.files import handle_user_file
from routers.generator.validation_schema import (
    DatasetOutput,
    GeneratorDataOutput,
    SupportedDatatypesCategory,
    SupportedDatatypes,
    ModelOutput,
)


def test_handle_user_file_parsing_error(monkeypatch):
    """
    Given check_user_file returns an empty list
    When handle_user_file is called
    Then it should return (None, error message)
    """

    monkeypatch.setattr(
        "routers.generator.checks.files.check_user_file",
        lambda _: [],
    )

    data = {
        "user_file": [{"a": "1"}],
        "additional_rows": 10,
    }

    result, error = handle_user_file(
        data=data,
        function_data=None,
        model=MagicMock(),
    )

    assert result is None
    assert error == "Error parsing input dataset"


def test_handle_user_file_success(monkeypatch):
    """
    Given check_user_file returns a valid dataset
    When handle_user_file is called
    Then it should return GeneratorDataOutput and empty error
    """

    dummy_dataset = [
        DatasetOutput(
            column_name="a",
            column_data=[1, 2, 3],
            column_type=SupportedDatatypesCategory.continuous,
            column_datatype=SupportedDatatypes.int,
        )
    ]

    monkeypatch.setattr(
        "routers.generator.checks.files.check_user_file",
        lambda _: dummy_dataset,
    )

    model = ModelOutput(model_name="model", algorithm_name="algorithm")

    data = {
        "user_file": [{"a": "1"}, {"a": "2"}],
        "additional_rows": 42,
    }

    result, error = handle_user_file(
        data=data,
        function_data=None,
        model=model,
    )

    assert error == ""
    assert isinstance(result, GeneratorDataOutput)

    assert result.dataset == dummy_dataset
    assert result.n_rows == 42
    assert result.model == model
