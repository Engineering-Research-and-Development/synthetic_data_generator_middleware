from database.schema import Parameter, FunctionParameter
from routers.generator.validation_schema import FunctionDataOut, GeneratorDataOutput


def handle_features_creation(
    data: dict, function_data: list[FunctionDataOut] | None, model
) -> tuple[GeneratorDataOutput | None, str]:
    """
    Create the GeneratorDataOutput object from the list of features

    :param data: the dictionary containing the input data
    :param function_data: the list of functions to pass to the generator
    :param model: the chosen AI model
    :return: the GeneratorDataOutput object or an error message
    """
    result, error = check_features_created_types(
        data.get("features_created"), data["functions"]
    )

    if not result:
        return (
            None,
            f"The functions chosen are not compatible with the following feature that you want to create ({error})",
        )

    return (
        GeneratorDataOutput(
            functions=function_data,
            n_rows=data.get("additional_rows"),
            model=model,
        ),
        "",
    )


def check_features_created_types(features: list[dict], function_ids: list[int]):
    """
    This function checks if the features that the user has created and passed in input are
    consistent with the functions' parameters tha have been selected
    :return:
    """
    functions_param_types = (
        Parameter.select()
        .join(FunctionParameter)
        .where(FunctionParameter.function << function_ids)
    )

    function_params_dict = {
        elem["parameter_type"]: "" for elem in functions_param_types.dicts()
    }
    for feature in features:
        if function_params_dict.get(feature["type"]) is None:
            return False, feature["type"]
    return True, None
