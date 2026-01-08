import pytest
from fastapi.testclient import TestClient

from bootstrap_data import insert_data
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
from main import app


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def peewee_db():
    db.connect(reuse_if_open=True)
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
    insert_data()
    yield
    db.close()
