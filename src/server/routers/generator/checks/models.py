from typing import Dict

import peewee

from database.schema import Algorithm, TrainedModel, ModelVersion, TrainModelDatatype
from routers.generator.validation_schema import ModelOutput, TrainingDataInfo


def check_new_model(new_model: int, model_name: str) -> ModelOutput | Dict:
    """
    Checks if a new model exists in the Algorithm database and returns model details.

    :param new_model: Algorithm ID of the new model.
    :param model_name: Name of the model.
    :return: ModelOutput object with algorithm and model name, or an empty dictionary if not found.
    """
    try:
        algorithm = Algorithm.get(Algorithm.id == new_model)
        return ModelOutput(algorithm_name=algorithm.name, model_name=model_name)
    except peewee.DoesNotExist:
        return {}


def check_existing_model(
    selected_model_id: int, version_name: str
) -> ModelOutput | Dict:
    """
    Checks if an existing trained model and its version exist in the database.

    :param selected_model_id: ID of the trained model.
    :param version_name: Version name of the model.
    :return: ModelOutput object with model details, or an empty dictionary if not found.
    """
    try:
        trained_model = TrainedModel.get_by_id(selected_model_id)
    except peewee.DoesNotExist:
        return {}

    try:
        model_version = (
            ModelVersion.select()
            .where(
                ModelVersion.version_name == version_name
                and ModelVersion.trained_model == trained_model
            )
            .get()
        )
    except peewee.DoesNotExist:
        return {}

    algorithm = Algorithm.get(Algorithm.id == trained_model.algorithm_id)

    training_data_info = list(
        TrainModelDatatype.select().where(
            TrainModelDatatype.trained_model == trained_model
        )
    )

    training_data_info_out = []
    for data in training_data_info:
        training_data_info_out.append(
            TrainingDataInfo(
                column_name=data.feature_name,
                column_type=data.feature_type,
                column_size=data.feature_size,
                column_position=data.feature_position,
                column_datatype=data.datatype.type,
            )
        )

    return ModelOutput(
        algorithm_name=algorithm.name,
        model_name=trained_model.name,
        input_shape=trained_model.input_shape,
        image=model_version.image_path,
        training_data_info=training_data_info_out,
    )


def check_ai_model(data: dict) -> ModelOutput | Dict:
    """
    Determines whether to check for a new or existing AI model and retrieves its details.

    :param data: Dictionary containing AI model selection details.
    :return: ModelOutput object or an empty dictionary if the model is not found.
    """
    new_model = data.get("new_model", False)
    if new_model:
        model_output = check_new_model(
            data["selected_model_id"], data["new_model_name"]
        )
    else:
        model_output = check_existing_model(
            data["selected_model_id"], data["model_version"]
        )

    if model_output == {}:
        return {}
    return model_output
