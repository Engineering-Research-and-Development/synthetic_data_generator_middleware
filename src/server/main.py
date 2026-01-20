from contextlib import asynccontextmanager
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import RedirectResponse, JSONResponse

from config import (
    allowed_origins,
    bootstrap_data,
)
from database.schema import (
    Algorithm,
    DataType,
    AlgorithmDataType,
    TrainedModel,
    TrainModelDatatype,
    ModelVersion,
    Parameter,
    Function,
    FunctionParameter,
    db,
)
from bootstrap_data import insert_data
from routers.trained_models import endpoints as trained_models
from routers.functions import endpoints as functions
from routers.algorithm import endpoints as algorithm
from routers.generator import endpoints as user_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function defines the logic of the FastAPIcls application life-cycle. The code before the yield is run
    BEFORE the application is launched while the code after the yield is run AFTER the app execution. The code
    is run only once.
    """
    logger.info("Starting up lifespan")
    db.create_tables(
        [
            Algorithm,
            DataType,
            AlgorithmDataType,
            TrainedModel,
            TrainModelDatatype,
            ModelVersion,
            Function,
            Parameter,
            FunctionParameter,
        ]
    )

    if bootstrap_data:
        insert_data()

    yield


# Program entry point
app = FastAPI(
    title="GENErative System for Intelligent Synthetic data generation - GENESIS",
    description="Welcome to the official documentation of the middleware co mponent for the ENG Genesis project."
    "It gives persistent storage capabilities to support the model generator",
    version="0.1.5",
    lifespan=lifespan,
)
# Authorizing all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)
app.include_router(user_data.router)
app.include_router(functions.router)
app.include_router(algorithm.router)
app.include_router(trained_models.router)


@app.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")


@app.middleware("http")
async def enforce_utf8_middleware(request: Request, call_next):
    body = await request.body()

    try:
        body.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content="Request body is not valid UTF-8",
        )

    return await call_next(request)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
