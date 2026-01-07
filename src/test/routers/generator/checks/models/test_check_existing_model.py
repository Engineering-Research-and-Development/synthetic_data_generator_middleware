from unittest.mock import MagicMock

import peewee

from routers.generator.checks.models import check_existing_model
from routers.generator.validation_schema import ModelOutput, TrainingDataInfo


def test_check_existing_model_trained_model_not_found(monkeypatch):
    """
    Given TrainedModel.get_by_id raises DoesNotExist
    When check_existing_model is called
    Then it should return {}
    """

    monkeypatch.setattr(
        "database.schema.TrainedModel.get_by_id",
        lambda _: (_ for _ in ()).throw(peewee.DoesNotExist()),
    )

    result = check_existing_model(
        selected_model_id=1,
        version_name="v1",
    )

    assert result == {}


def test_check_existing_model_version_not_found(monkeypatch):
    """
    Given trained model exists
    But model version does not
    Then it should return {}
    """

    dummy_trained_model = MagicMock()
    dummy_trained_model.algorithm_id = 10

    monkeypatch.setattr(
        "database.schema.TrainedModel.get_by_id",
        lambda _: dummy_trained_model,
    )

    mock_select = MagicMock()
    mock_select.where.return_value.get.side_effect = peewee.DoesNotExist()

    monkeypatch.setattr(
        "database.schema.ModelVersion.select",
        lambda: mock_select,
    )

    result = check_existing_model(
        selected_model_id=1,
        version_name="v1",
    )

    assert result == {}


def test_check_existing_model_success(monkeypatch):
    """
    Given trained model, version, algorithm and training data exist
    When check_existing_model is called
    Then it should return a fully populated ModelOutput
    """

    # ---- TrainedModel ----
    trained_model = MagicMock()
    trained_model.name = "my-trained-model"
    trained_model.algorithm_id = 5
    trained_model.input_shape = "(10, 5)"

    monkeypatch.setattr(
        "database.schema.TrainedModel.get_by_id",
        lambda _: trained_model,
    )

    # ---- ModelVersion ----
    model_version = MagicMock()
    model_version.image_path = "/tmp/model.png"

    mock_version_select = MagicMock()
    mock_version_select.where.return_value.get.return_value = model_version

    monkeypatch.setattr(
        "database.schema.ModelVersion.select",
        lambda: mock_version_select,
    )

    # ---- Algorithm ----
    algorithm = MagicMock()
    algorithm.name = "RandomForest"

    monkeypatch.setattr(
        "database.schema.Algorithm.get",
        lambda _: algorithm,
    )

    # ---- TrainModelDatatype ----
    datatype = MagicMock()
    datatype.type = "float32"

    train_data_row = MagicMock()
    train_data_row.feature_name = "age"
    train_data_row.feature_type = "continuous"
    train_data_row.feature_size = "1"
    train_data_row.feature_position = 0
    train_data_row.datatype = datatype

    mock_train_select = MagicMock()
    mock_train_select.where.return_value = [train_data_row]

    monkeypatch.setattr(
        "database.schema.TrainModelDatatype.select",
        lambda: mock_train_select,
    )

    # ---- Call ----
    result = check_existing_model(
        selected_model_id=1,
        version_name="v1",
    )

    assert isinstance(result, ModelOutput)

    assert result.algorithm_name == "RandomForest"
    assert result.model_name == "my-trained-model"
    assert result.input_shape == "(10, 5)"
    assert result.image == "/tmp/model.png"

    assert len(result.training_data_info) == 1
    tdi = result.training_data_info[0]

    assert isinstance(tdi, TrainingDataInfo)
    assert tdi.column_name == "age"
    assert tdi.column_type == "continuous"
    assert tdi.column_size == "1"
    assert tdi.column_position == 0
    assert tdi.column_datatype == "float32"
