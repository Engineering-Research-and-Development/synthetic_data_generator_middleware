from fastapi import APIRouter
from starlette.responses import JSONResponse

from database.schema import Algorithm, DataType, AlgorithmDataType
from routers.algorithm.validation_schema import (
    AlgorithmList,
    AlgorithmDataTypeOut,
    AlgorithmID,
    AlgorithmDatatype as PydanticAlgorithmDataType,
)


router = APIRouter(prefix="/algorithms", tags=["Algorithms"])


@router.post(
    "/",
    status_code=201,
    name="Create a new algorithm",
    summary="Creates an algorith given the information and allowed datatypes",
    responses={500: {"model": str}},
    response_model=AlgorithmID,
)
async def create_new_algorithm(payload: PydanticAlgorithmDataType):
    """
    This method lets the user add a new algorithm to the model registry. An algorithm name must be ***unique*** (error 400
    will be returned if not) and the datatypes must be ***already present*** in the model registry, otherwise an error will be
    returned and the user must add the new datatype it wants to use with POST /datatypes
    """
    algorithm = payload.algorithm
    data_types = payload.datatypes
    alg, algo_is_created = Algorithm.get_or_create(
        name=algorithm.name,
        defaults={
            "description": algorithm.description,
            "default_loss_function": algorithm.default_loss_function,
        },
    )

    if algo_is_created:
        for data_type in data_types:
            data_type, _ = DataType.get_or_create(
                type=data_type.type, is_categorical=data_type.is_categorical
            )
            _ = AlgorithmDataType.create(algorithm=alg, datatype=data_type)

    return AlgorithmID(id=alg.id)


@router.get(
    "/", status_code=200, name="Get all algorithms", response_model=AlgorithmList
)
async def get_all_algorithms():
    """
    This method returns all the algorithms that are present in the model registry.
    """
    algorithms = Algorithm.select().dicts()
    return AlgorithmList(algorithms=list(algorithms))


@router.get(
    "/{algorithm_id}",
    status_code=200,
    name="Get algorithm by id",
    summary="It returns an algorithm given the id",
    responses={404: {"model": str}},
    response_model=AlgorithmDataTypeOut,
)
async def get_algorithm_by_id(algorithm_id: int):
    """
    Returns an algorithm given its ID
    """
    algorithm = Algorithm.select().where(Algorithm.id == algorithm_id).dicts()
    if len(algorithm) == 0:
        return JSONResponse(status_code=404, content={"message": "Algorithm not found"})

    all_dtypes = (
        AlgorithmDataType.select(DataType)
        .join(DataType)
        .where(AlgorithmDataType.algorithm == algorithm_id)
        .dicts()
    )
    return AlgorithmDataTypeOut(algorithm=algorithm.get(), datatypes=list(all_dtypes))


@router.delete(
    "/{algorithm_id}",
    status_code=200,
    name="Delete an algorithm given his id",
    summary="It deletes an algorithm given the id and his allowed datatypes and trained models",
    responses={404: {"model": str}},
)
async def delete_algorithm(algorithm_id: int):
    """
    Given an id, this method deletes an algorithm and all the allowed datatypes as well as trained models, training info
    and feature schema
    """
    Algorithm.delete_by_id(algorithm_id)
    return JSONResponse(status_code=200, content="ok")
