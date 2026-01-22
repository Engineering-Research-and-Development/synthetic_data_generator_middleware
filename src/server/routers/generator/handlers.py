from .checks.features import handle_features_creation
from .checks.files import check_user_file
from .checks.functions import check_function_parameters
from .validation_schema import (
    GeneratorDataOutput,
    UserFeatureInfo,
    GeneratorFunctionOut,
)
from .checks.models import check_ai_model


def handle_user_file_input(
    user_data: dict,
    additional_rows: int,
    feature_types: dict[str, UserFeatureInfo] | None,
) -> tuple[GeneratorDataOutput | None, str]:
    function_data = None

    if user_data.get("functions"):
        function_data = check_function_parameters(user_data["functions"])
        if function_data is None:
            error = "Error analysing functions"
            return None, error

    model = check_ai_model(user_data.get("ai_model"))
    if not model:
        error = "AI model not found in database"
        return None, error

    user_file = user_data.get("user_file", [])
    if len(user_file) == 0:
        error = "Empty user file provided"
        return None, error

    valid_user_file = check_user_file(user_file, feature_types)
    if not valid_user_file:
        return None, "Error parsing input dataset"
    body = GeneratorDataOutput(
        functions=function_data,
        n_rows=additional_rows,
        model=model,
        dataset=valid_user_file,
    )
    return body, ""


def handle_features_created_input(
    user_data: dict, additional_rows: int
) -> tuple[GeneratorFunctionOut | None, str]:
    if len(user_data.get("features_created")) == 0:
        return None, "Empty features list"
    list_function, error = handle_features_creation(
        user_data.get("features_created"), user_data.get("functions")
    )
    if error != "":
        return None, error

    return GeneratorFunctionOut(
        functions=list_function,
        n_rows=additional_rows,
    ), ""
