import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from database.schema import (
    Algorithm,
    DataType,
    AlgorithmDataType,
    TrainedModel,
    TrainModelDatatype,
    ModelVersion,
    db,
    Parameter,
    Function,
    FunctionParameter,
)
from bootstrap_data import insert_data
from routers.trained_models import trained_models
from routers.functions import functions
from routers.algorithm import algorithm
from routers.generator import user_data

allowed_origins = os.environ.get("allowed_origins", "*").split(",")
allow_credentials = os.environ.get("allow_credentials", True)
allow_methods = os.environ.get("allow_methods", "*").split(",")
allow_headers = os.environ.get("allow_headers", "*").split(",")
init_db = os.environ.get("INIT_DB", False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function defines the logic of the FastAPIcls application life-cycle. The code before the yield is run
    BEFORE the application is launched while the code after the yield is run AFTER the app execution. The code
    is run only once.
    """
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

    if init_db == "True":
        insert_data()

    yield


# Program entry point
app = FastAPI(
    title="Synthetic Data Generator",
    description="Middleware component for the ENG Synthetic Data Generator."
    "It gives persistent storage capabilities to support the model generator",
    version="0.0.1",
    lifespan=lifespan,
)
# Authorizing all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)

app.include_router(user_data.router)
app.include_router(functions.router)
app.include_router(algorithm.router)
app.include_router(trained_models.router)


@app.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
