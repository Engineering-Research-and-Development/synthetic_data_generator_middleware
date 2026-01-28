import peewee
from fastapi import APIRouter, Path
from starlette import status
from starlette.responses import JSONResponse

from database.schema import (
    Parameter,
    Function,
    FunctionParameter,
    DataType,
    FunctionDataType,
)
from .validation_schema import (
    FunctionParameterDataTypeOut,
    FunctionParameterDataTypeIn,
    FunctionOut,
)

router = APIRouter(prefix="/functions", tags=["Functions"])


@router.get(
    "/",
    name="Get all function parameters",
    status_code=status.HTTP_200_OK,
    summary="Get all the available function parameters",
    response_model=list[FunctionOut],
)
async def get_all_functions() -> list[FunctionOut]:
    """
    This method returns all the function parameters that are present in the model registry
    """
    functions = Function.select().dicts()
    results = [
        FunctionOut(
            function=function,
        )
        for function in functions
    ]

    return results


@router.get(
    "/{function_id}",
    name="Get function parameters by function ID",
    status_code=status.HTTP_200_OK,
    summary="Get all parameters associated with a specific function",
    response_model=FunctionParameterDataTypeOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": str}},
)
async def get_function_parameters_datatype_by_function_id(
    function_id: int = Path(
        description="The ID of the function to retrieve parameters for",
        examples=[1],
        gt=0,
    ),
):
    """
    This function returns a function parameter given his id. If not found, a 404 will be returned
    """
    try:
        function = Function.select().where(Function.id == function_id).dicts().get()
    except peewee.DoesNotExist:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="Function not found"
        )

    parameters = [
        Parameter.select().where(Parameter.id == p.parameter).dicts().get()
        for p in FunctionParameter.select().where(
            FunctionParameter.function == function_id
        )
    ]

    datatypes = [
        DataType.select().where(DataType.id == d.datatype).dicts().get()
        for d in FunctionDataType.select().where(
            FunctionDataType.function == function_id
        )
    ]

    return FunctionParameterDataTypeOut(
        function=function, parameters=parameters, datatypes=datatypes
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    name="Add new function to the DB",
    summary="Create a new function given the parameters",
    responses={
        status.HTTP_201_CREATED: {"model": FunctionOut},
        status.HTTP_409_CONFLICT: {"model": str},
    },
    response_model=FunctionOut,
)
async def create_new_function(payload: FunctionParameterDataTypeIn):
    function = payload.function
    parameters = payload.parameters
    datatypes = payload.datatypes

    function, function_created = Function.get_or_create(
        name=function.name,
        defaults={
            "description": function.description,
            "function_reference": function.function_reference,
            "is_generative": function.is_generative,
            "priority": function.priority,
        },
    )

    if not function_created:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content="Function already exists"
        )

    for parameter in parameters:
        parameter, _ = Parameter.get_or_create(
            name=parameter.name,
            defaults={
                "parameter_type": parameter.parameter_type,
                "value": parameter.value,
            },
        )
        FunctionParameter.get_or_create(function=function, parameter=parameter)

    for datatype in datatypes:
        retrieved_datatype, _ = DataType.get_or_create(
            type=datatype.type, is_categorical=datatype.is_categorical
        )
        FunctionDataType.create(
            function=function,
            datatype=retrieved_datatype,
        )

    return FunctionOut(
        function=Function.select().where(Function.id == function.id).dicts().get()
    )


@router.delete(
    "/{function_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete a function given his id",
    summary="It deletes a function given the id",
    responses={status.HTTP_404_NOT_FOUND: {"model": str}},
)
async def delete_function(function_id: int = Path(gt=0)):
    try:
        Function.get_by_id(function_id)
    except peewee.DoesNotExist:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="Function not found"
        )
    Function.delete_by_id(function_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="ok")
