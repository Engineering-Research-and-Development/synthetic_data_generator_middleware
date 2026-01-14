from database.schema import Parameter, FunctionParameter
from routers.generator.validation_schema import (
    GeneratorDataOutput,
    ModelOutput,
)


def handle_features_creation(
    data: list[dict],
    function_data: list[int] | None,
    model: ModelOutput,
    additional_rows: int,
) -> tuple[GeneratorDataOutput | None, str]:
    """
    Create the GeneratorDataOutput object from the list of features

    :param additional_rows: the number of additional rows to create
    :param data: the dictionary containing the input data
    :param function_data: the list of functions to pass to the generator
    :param model: the chosen AI model
    :return: the GeneratorDataOutput object or an error message
    """
    result, error = check_features_created_types(data, function_data)

    if not result:
        return (
            None,
            f"The functions chosen are not compatible with the following feature that you want to create ({error})",
        )

    return (
        GeneratorDataOutput(
            functions=function_data,
            n_rows=additional_rows,
            model=model,
        ),
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
