import requests
from fastapi import APIRouter
from starlette.responses import JSONResponse

from config import generator_url
from .handlers import (
    check_function_parameters,
    process_input,
)
from .checks.models import check_ai_model
from .validation_schema import UserDataInput, GeneratorResponse

router = APIRouter(prefix="/sdg_input", tags=["SDG Input"])

@router.post(
    "/",
    name="Synthetic Data Generator input collection",
    responses={500: {"model": str}, 400: {"model": str}, 404: {"model": str}},
    response_model=GeneratorResponse,
)
async def collect_user_input(input_data: UserDataInput):
    data = input_data.model_dump()
    function_data = None

    if data.get("functions"):
        function_data = check_function_parameters(data["functions"])
        if not function_data:
            return JSONResponse(status_code=400, content="Error analysing functions")

    model = check_ai_model(data.get("ai_model"))
    if not model:
        return JSONResponse(status_code=404, content="AI model not found in database")

    body, error = process_input(data, function_data, model)
    if error != "":
        return JSONResponse(status_code=400, content=error)

    if data.get("ai_model").get("new_model") and data.get("user_file"):
        url = generator_url + "/train"
    else:
        url = generator_url + "/infer"

    # Sending data to the generator
    response = requests.post(url, json=body.model_dump())
    if response.status_code != 200:
        return JSONResponse(status_code=response.status_code, content=response.json())
    return GeneratorResponse(**response.json())
