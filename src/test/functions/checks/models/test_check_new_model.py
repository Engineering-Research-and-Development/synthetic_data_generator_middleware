from database.schema import TrainedModel, ModelVersion
from routers.generator.checks.models import check_existing_model
from routers.generator.validation_schema import ModelOutput, TrainingDataInfo


def test_check_existing_model_success():
    trained_model = TrainedModel.select().first()
    assert trained_model is not None

    version = (
        ModelVersion.select().where(ModelVersion.trained_model == trained_model).first()
    )
    assert version is not None

    result = check_existing_model(trained_model.id, version.version_name)

    assert isinstance(result, ModelOutput)
    assert result.model_name == trained_model.name
    assert result.algorithm_name == trained_model.algorithm.name
    assert result.image == version.image_path
    assert result.input_shape == trained_model.input_shape
    assert isinstance(result.training_data_info, list)
    if result.training_data_info:
        assert isinstance(result.training_data_info[0], TrainingDataInfo)


def test_check_existing_model_trained_model_not_found():
    result = check_existing_model(999999, "v1")
    assert result == {}


def test_check_existing_model_version_not_found():
    trained_model = TrainedModel.select().first()
    assert trained_model is not None

    result = check_existing_model(trained_model.id, "non_existing_version")
    assert result == {}
