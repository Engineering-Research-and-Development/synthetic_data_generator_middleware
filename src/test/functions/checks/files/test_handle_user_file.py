from routers.generator.checks.files import handle_user_file
from routers.generator.validation_schema import GeneratorDataOutput, ModelOutput


def test_handle_user_file_success():
    data = {
        "additional_rows": 10,
        "data": {
            "input_type": "user_file",
            "user_file": [
                {"a": "1"},
                {"a": "2"},
            ],
        },
    }
    model = ModelOutput(algorithm_name="dummy_model", model_name="model-x")
    output, error = handle_user_file(
        data=data["data"]["user_file"],
        function_data=None,
        model=model,
        additional_rows=data["additional_rows"],
    )

    assert error == ""
    assert isinstance(output, GeneratorDataOutput)
    assert output.model.model_name == "model-x"
    assert output.n_rows == 10
    assert len(output.dataset) == 1


def test_handle_user_file_error_on_empty_dataset():
    data = {"user_file": []}

    output, error = handle_user_file(
        data["user_file"], function_data=None, model="model-x", additional_rows=0
    )

    assert output is None
    assert error == "Error parsing input dataset"
