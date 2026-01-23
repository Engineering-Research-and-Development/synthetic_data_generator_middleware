from database.schema import Parameter, Function, FunctionParameter
from routers.generator.validation_schema import (
    FunctionDataOut,
    FunctionData,
    ParametersOut,
)


def handle_features_creation(
    data: list[dict],
    function_data: list[FunctionData] | None,
) -> tuple[list[FunctionDataOut] | None, str]:
    """
    Create the FunctionDataOut object from the list of features

    :param data: the dictionary containing the input data
    :param function_data: the list of functions to pass to the generator
    :return: the FunctionDataOut object or an error message
    """
    if not function_data:
        return [], ""
    
    function_data = [f.model_dump() for f in function_data]
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
        func = Function.select().where(Function.id == function_id).dicts().get()
        
        # Get parameter IDs from input function data
        input_param_ids = [param.get("param_id") for param in function.get("parameters", [])]
        
        # Fetch only parameters that are in the input list
        parameters = (FunctionParameter
                .select(Parameter)
                .join(Parameter)
                .where(
                    (FunctionParameter.function == function.get("function_id")) &
                    (Parameter.id.in_(input_param_ids))
                )
                .dicts())
        
        complete_func = FunctionDataOut(
            feature=function.get("feature"),
            function_reference=func.get("function_reference"),
            parameters=[ParametersOut(
                name=p.get("name"),
                value=next((param.get("value") for param in function.get("parameters", []) 
                          if param.get("param_id") == p.get("id")), ""),
                parameter_type=p.get("parameter_type"),
            ) for p in parameters]
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
    
    # If no functions are selected, no validation needed
    if not function_ids:
        return True, None

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
