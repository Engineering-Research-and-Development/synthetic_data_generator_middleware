from database.schema import Parameter, Function, FunctionParameter
from routers.generator.validation_schema import (
    FunctionDataOut,
    FunctionData,
)


def handle_features_creation(
    data: list[dict],
    function_data: list[FunctionData],
) -> tuple[list[FunctionDataOut] | None, str]:
    """
    Create the GeneratorDataOutput object from the list of features

    :param data: the dictionary containing the input data
    :param function_data: the list of functions to pass to the generator
    :return: the GeneratorFunctionOut object or an error message
    """
    function_ids = [f.get("function_id") for f in function_data]
    result, error = check_features_created_types(data, function_ids)

    if not result:
        return (
            None,
            f"The functions chosen are not compatible with the following feature that you want to create ({error})",
        )

    list_function_out = []
    for function in function_data:
        function_id = function.get("function_id")
        func = Function.select().where(Function.id == function_id).dicts()
        complete_func = FunctionDataOut(
            feature=function.get("feature"),
            function_reference=func.get("function_reference"),
            parameters=function.get("parameters"),
        )
        list_function_out.append(complete_func)

    return (
        list_function_out,
        "",
    )


def check_features_created_types(
    features: list[dict], function_ids: list[int]
) -> tuple[bool, str | None]:
    """
    Validate that all feature types are compatible with the parameters
    of the selected functions.
    """

    # Fetch allowed parameter types for the selected functions
    query = (
        Parameter.select(Parameter.parameter_type)
        .join(FunctionParameter)
        .where(FunctionParameter.function.in_(function_ids))
        .distinct()
    )

    allowed_types: set[str] = {row.parameter_type for row in query}

    for feature in features:
        feature_type = feature.get("type")
        if feature_type not in allowed_types:
            return False, feature_type

    return True, None
