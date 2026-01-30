import requests
from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse
from requests.exceptions import ConnectionError

from config import generator_url
from .checks.models import check_ai_model
from .handlers import (
    handle_user_file_input,
    handle_features_created_input,
)
from routers.generator.validation_schema.input import UserDataInput
from routers.generator.validation_schema.output import GeneratorResponse

router = APIRouter(prefix="/sdg_input", tags=["SDG Input"])


@router.post(
    "/",
    name="Synthetic Data Generator input collection",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": str},
    },
    response_model=GeneratorResponse,
)
async def collect_user_input(input_data: UserDataInput):
    data = input_data.model_dump()
    additional_rows = data.get("additional_rows")
    feature_types = data.get("feature_types")
    data_content = data.get("data")
    input_type = data_content.get("input_type")

    if input_type == "user_file":
        model = check_ai_model(data_content.get("ai_model"))
        if not model:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content="AI model not found in database",
            )

        body, error = handle_user_file_input(
            data_content, additional_rows, feature_types
        )
        if error != "":
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error)
        if data_content.get("ai_model").get("new_model") and data_content.get(
            "user_file"
        ):
            url = generator_url + "/train"
        else:
            url = generator_url + "/infer"

    else:
        body, error = handle_features_created_input(data_content, additional_rows)
        if error != "":
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error)
        url = generator_url + "/generate"

    # Sending data to the generator
    try:
        response = requests.post(url, json=body.model_dump())
        if response.status_code != status.HTTP_200_OK:
            return JSONResponse(
                status_code=response.status_code, content=response.json()
            )
        return GeneratorResponse(**response.json())
    except ConnectionError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content="Backend connection error. Please contact the administrator.",
        )
