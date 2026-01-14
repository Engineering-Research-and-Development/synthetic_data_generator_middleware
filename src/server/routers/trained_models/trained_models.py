import peewee
from fastapi import APIRouter, Path, Query
from starlette.responses import JSONResponse

from database.schema import (
    TrainedModel,
    ModelVersion,
    TrainModelDatatype,
    Algorithm,
    DataType,
)
from routers.trained_models.validation_schema import (
    TrainedModelVersionList,
    TrainedModelVersion,
    TrainedModelVersionDatatype,
    PostTrainedModelVersionDatatype,
    PostTrainedModelOut,
    MergedDataType,
)

router = APIRouter(prefix="/trained_models", tags=["Trained Models"])


@router.get(
    "/",
    status_code=200,
    summary="Get all the trained model in the repository",
    name="Get all trained models",
    response_model=TrainedModelVersionList,
)
async def get_all_trained_models():
    """
    Retrieves a complete list of all trained models in the repository with their associated versions.

    This endpoint returns:

    - A comprehensive list of all trained models

    - Each model's metadata (name, description, algorithm, etc.)

    - All versions associated with each model

    - Basic information about each version (version number, creation date)
    """
    response = []
    trained_models = TrainedModel.select().dicts()
    for model in trained_models:
        model_versions = (
            ModelVersion.select()
            .where(ModelVersion.trained_model == model["id"])
            .dicts()
        )
        response.append(TrainedModelVersion(model=model, versions=model_versions))
    return TrainedModelVersionList(models=response)


@router.get(
    "/{model_id}",
    status_code=200,
    name="Get a single trained model",
    summary="It returns a trained model given the id",
    responses={404: {"model": str}},
    response_model=TrainedModelVersionDatatype,
)
async def get_trained_model_id(
    model_id: int = Path(
        description="The id of the trained model you want to get", examples=[1], gt=0
    ),
):
    """
    Retrieves comprehensive information about a specific trained model including:

    - Model metadata (name, description, algorithm)

    - All associated versions with their details

    - Feature schema (data types and their characteristics)
    """
    trained_model = TrainedModel.select().where(TrainedModel.id == model_id).dicts()
    if len(trained_model) == 0:
        return JSONResponse(status_code=404, content="Model not found")

    model_versions = (
        ModelVersion.select().where(ModelVersion.trained_model == trained_model).dicts()
    )
    datatypes = (
        DataType.select(DataType, TrainModelDatatype)
        .join(TrainModelDatatype)
        .where(TrainModelDatatype.trained_model == trained_model)
        .dicts()
    )
    merged_datatypes = []
    for datatype in datatypes:
        merged_datatypes.append(MergedDataType(**datatype))
    [merged_datatypes.append(MergedDataType(**datatype)) for datatype in datatypes]

    return TrainedModelVersionDatatype(
        model=trained_model.get(), versions=model_versions, datatypes=merged_datatypes
    )


@router.post(
    "/",
    name="Create a new training model",
    status_code=201,
    summary="It creates a trained model given the all the information,version,training infos and feature schema",
    responses={
        404: {"model": str},
        201: {"model": PostTrainedModelOut},
    },
    response_model=PostTrainedModelOut,
)
async def create_model_and_version(payload: PostTrainedModelVersionDatatype):
    """
    Creates a new trained model and its initial version in the system.

    This endpoint accepts comprehensive information including:

    - Model details (algorithm, name, description)

    - Version information (version number, performance metrics)

    - Training configuration (parameters, training data info)

    - Feature schema (data types and their characteristics)
    """
    try:
        Algorithm.get_by_id(payload.model.algorithm)
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content="Algorithm not found")

    trained_model, model_created = TrainedModel.get_or_create(
        **payload.model.model_dump()
    )
    model_version = payload.version.model_dump()
    model_version["trained_model"] = trained_model
    model_version = ModelVersion.create(**model_version)

    if model_created:
        datatypes = payload.datatypes
        for datatype in datatypes:
            retrieved_datatype, _ = DataType.get_or_create(
                type=datatype.type, is_categorical=datatype.is_categorical
            )
            TrainModelDatatype.create(
                trained_model=trained_model,
                datatype=retrieved_datatype,
                feature_name=datatype.feature_name,
                feature_position=datatype.feature_position,
                feature_type=datatype.feature_type,
                feature_size=datatype.feature_size,
            )

    return PostTrainedModelOut(
        trained_model_id=trained_model.id, model_version_id=model_version.id
    )


@router.delete(
    "/{model_id}",
    status_code=204,
    name="Deletes a trained model",
    summary="Given an id it deletes only a specific version from the trained model leaving the model intact",
    responses={404: {"model": str}},
)
async def delete_train_model(
    model_id: int = Path(
        description="The id of the trained model you want to delete", examples=[1], gt=0
    ),
    version_name: str = Query(default=None, description="The version to delete"),
):
    """
    Delete a trained model or a specific version of a trained model.

    This endpoint allows you to:

    - Delete an entire trained model (all versions) if no version_name is specified

    - Delete only a specific version of a trained model if version_name is provided
    """
    try:
        trained_model = TrainedModel.get_by_id(model_id)
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content="Trained model not found")

    if version_name is None:
        TrainedModel.delete_by_id(trained_model)
        return JSONResponse(status_code=204, content=trained_model.id)
    else:
        ModelVersion.select().where(
            trained_model == trained_model and version_name == version_name
        ).get().delete_instance()
        return JSONResponse(status_code=204, content=version_name)
