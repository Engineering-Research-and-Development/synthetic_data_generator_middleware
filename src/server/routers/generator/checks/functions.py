from database.schema import FunctionParameter, Function
from routers.generator.validation_schema import (
    FunctionData,
    FunctionDataOut,
    ParametersOut,
)


def check_function_parameters(functions: list[FunctionData]) -> list[FunctionDataOut]:
    """
    Validates function parameters by checking if all input parameters match those in the database.

    :param functions: List of function dictionaries containing function_id and parameters.
    :return: List of valid function IDs if all parameters match, otherwise an empty list.
    """
    function_data = []
    for function in functions:
        parameter_ids = FunctionParameter.select(FunctionParameter.parameter).where(
            FunctionParameter.function == function.function_id
        )
        parameter_ids_list = [p.parameter_id for p in parameter_ids]
        input_param = [item["param_id"] for item in function.parameters]
        selected_param = [p for p in parameter_ids_list if p in input_param]
        # If the functions are passed they must have parameters
        if len(input_param) != len(parameter_ids_list):
            return []
        if all(p in parameter_ids_list for p in input_param):
            function_data.append(
                structure_function_parameters(function, selected_param)
            )
            continue
        else:
            return []
    return function_data


def structure_function_parameters(
    function: FunctionData, selected_param: list[FunctionParameter]
) -> FunctionDataOut:
    """
    Builds a FunctionDataOut object from a FunctionData object, associating each parameter with its value.

    :param function: function data from user input
    :param selected_param: list of selected parameters from the database
    :return: A structured FunctionDataOut object
    """
    function_parameters = {param_id: value for param_id, value in function.parameters}
    function_reference = (
        Function.select(Function.function_reference)
        .where(Function.id == function.function_id)
        .get()
        .function_reference
    )
    params_out = [
        ParametersOut(
            name=p.parameter.name,
            value=function_parameters.get(p.parameter.id),
            parameter_type=p.parameter.parameter_type,
        )
        for p in selected_param
    ]

    return FunctionDataOut(
        function_reference=function_reference,
        feature=function.feature,
        parameters=params_out,
    )
