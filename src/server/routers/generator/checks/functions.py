from database.schema import (
    Parameter,
    FunctionParameter,
    Function,
    FunctionDataType,
    DataType,
)
from routers.generator.validation_schema.output import ParametersOut, FunctionDataOut


def handle_data_function_mapping(
    data: list[dict],
    function_data: list[dict] | None,
) -> tuple[list[FunctionDataOut] | None, str]:
    """
    Create the FunctionDataOut object from the list of features

    :param data: the dictionary containing the input data following the FeatureFunctionIn model
    :param function_data: the list of function dictionaries following the FunctionData Model
    :return: the FunctionDataOut object or an error message
    """
    if not function_data:
        return [], ""

    for feature_function in function_data:
        associated_functions = feature_function.get("associated_functions")
        associated_function_ids = [
            f.get("function").get("id") for f in associated_functions
        ]
        feature_name = feature_function.get("feature_name")
        selected_feature = [f for f in data if f.get("name") == feature_name][0]
        result, error = check_features_created_types(
            selected_feature.get("type"), associated_function_ids
        )

        if not result:
            return (
                None,
                f"The functions chosen are not compatible with the following feature that you want to create ({error})",
            )

    list_function_out = structure_function_parameters(function_data)

    return (
        list_function_out,
        "",
    )


def structure_function_parameters(function_data: list[dict]) -> list[FunctionDataOut]:
    """
    Validates function parameters by checking if all input parameters match those in the database.

    :param function_data: List of function dictionaries following the FunctionData validation model
    :return: List of valid function IDs if all parameters match, otherwise an empty list.
    """
    list_function_out = []
    for feature_function in function_data:
        associated_functions = feature_function.get("associated_functions")
        feature_name = feature_function.get("feature_name")
        for function in associated_functions:
            function_id = function.get("function").get("id")
            func = Function.select().where(Function.id == function_id).dicts().get()

            # Get parameter IDs from input function data
            input_param_ids = [
                param.get("id") for param in function.get("parameters", [])
            ]

            # Fetch only parameters that are in the input list
            parameters = (
                FunctionParameter.select(Parameter)
                .join(Parameter)
                .where(
                    (FunctionParameter.function == function.get("function").get("id"))
                    & (Parameter.id.in_(input_param_ids))
                )
                .dicts()
            )

            complete_func = FunctionDataOut(
                feature=feature_name,
                function_reference=func.get("function_reference"),
                parameters=[
                    ParametersOut(
                        name=p.get("name"),
                        value=next(
                            (
                                param.get("value")
                                for param in function.get("parameters", [])
                                if param.get("id") == p.get("id")
                            ),
                            "",
                        ),
                        parameter_type=p.get("parameter_type"),
                    )
                    for p in parameters
                ],
            )
            list_function_out.append(complete_func)
    return list_function_out


def check_features_created_types(
    feature_type: str, function_ids: list[int]
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
        DataType.select(DataType.type)
        .join(FunctionDataType)
        .where(FunctionDataType.function.in_(function_ids))
        .distinct()
    )

    allowed_types: set[str] = {row.type for row in query}

    if feature_type not in allowed_types:
        return False, feature_type

    return True, None
