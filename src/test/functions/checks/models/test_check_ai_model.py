from database.schema import TrainedModel, ModelVersion, Algorithm
from routers.generator.checks.models import check_ai_model
from routers.generator.validation_schema.output import ModelOutput


def test_check_ai_model_new_model_branch():
    algo = Algorithm.select().first()
    assert algo is not None

    data = {
        "new_model": True,
        "selected_model_id": algo.id,
        "new_model_name": "TestNewModel",
    }

    result = check_ai_model(data)
    assert isinstance(result, ModelOutput)
    assert result.algorithm_name == algo.name
    assert result.model_name == "TestNewModel"


def test_check_ai_model_existing_model_branch_success():
    trained_model = TrainedModel.select().first()
    assert trained_model is not None

    version = (
        ModelVersion.select().where(ModelVersion.trained_model == trained_model).first()
    )
    assert version is not None

    data = {
        "new_model": False,
        "selected_model_id": trained_model.id,
        "model_version": version.version_name,
    }

    result = check_ai_model(data)
    assert isinstance(result, ModelOutput)
    assert result.model_name == trained_model.name


def test_check_ai_model_existing_model_branch_not_found():
    data = {
        "new_model": False,
        "selected_model_id": 999999,
        "model_version": "v1",
    }

    result = check_ai_model(data)
    assert result == {}
