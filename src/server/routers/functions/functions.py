import peewee
from fastapi import APIRouter, Path
from starlette.responses import JSONResponse

from database.schema import Parameter, Function, FunctionParameter
from .validation_schema import FunctionParameterOut, FunctionParameterIn, FunctionOut

router = APIRouter(prefix="/functions", tags=["Functions"])


@router.get(
    "/",
    name="Get all function parameters",
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
    summary="Get all parameters associated with a specific function",
    response_model=FunctionParameterOut,
    responses={404: {"model": str}},
)
async def get_function_parameters_by_function_id(
    function_id: int = Path(
        description="The ID of the function to retrieve parameters for", examples=[1]
    ),
):
    """
    This function returns a function parameter given his id. If not found, a 404 will be returned
    """
    try:
        function = Function.select().where(Function.id == function_id).dicts().get()
    except peewee.DoesNotExist:
        return JSONResponse(status_code=404, content={"message": "Function not found"})

    parameters = [
        Parameter.select().where(Parameter.id == p.parameter).dicts().get()
        for p in FunctionParameter.select().where(
            FunctionParameter.function == function_id
        )
    ]

    return FunctionParameterOut(function=function, parameters=parameters)


@router.post(
    "/",
    status_code=201,
    name="Add new function to the DB",
    summary="Create a new function given the parameters",
    responses={500: {"model": str}},
    response_model=FunctionOut,
)
async def create_new_function(payload: FunctionParameterIn):
    function = payload.function
    parameters = payload.parameters

    function, _ = Function.get_or_create(
        name=function.name,
        defaults={
            "description": function.description,
            "function_reference": function.function_reference,
        },
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

    return FunctionOut(
        function=Function.select().where(Function.id == function.id).dicts().get()
    )


@router.delete(
    "/{function_id}",
    status_code=200,
    name="Delete a function given his id",
    summary="It deletes a function given the id",
    responses={404: {"model": str}},
)
async def delete_function(function_id: int):
    Function.delete_by_id(function_id)
    return JSONResponse(status_code=200, content="ok")
