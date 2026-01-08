from routers.generator.checks.files import handle_user_file
from routers.generator.validation_schema import GeneratorDataOutput, ModelOutput


def test_handle_user_file_success():
    data = {
        "user_file": [
            {"a": "1"},
            {"a": "2"},
        ],
        "additional_rows": 10,
    }
    model = ModelOutput(algorithm_name="dummy_model", model_name="model-x")
    output, error = handle_user_file(data, function_data=None, model=model)

    assert error == ""
    assert isinstance(output, GeneratorDataOutput)
    assert output.model.model_name == "model-x"
    assert output.n_rows == 10
    assert len(output.dataset) == 1


def test_handle_user_file_error_on_empty_dataset():
    data = {"user_file": []}

    output, error = handle_user_file(data, function_data=None, model="model-x")

    assert output is None
    assert error == "Error parsing input dataset"
