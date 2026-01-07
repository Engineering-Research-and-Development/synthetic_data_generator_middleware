from typing import List
from pydantic import BaseModel, PositiveInt
from database.validation_schema import Algorithm, DataType


class AlgorithmOut(Algorithm):
    id: PositiveInt


class AlgorithmDataTypeOut(BaseModel):
    algorithm: AlgorithmOut
    datatypes: List[DataType]


class AlgorithmList(BaseModel):
    algorithms: List[AlgorithmOut]


class AlgorithmDatatype(BaseModel):
    algorithm: Algorithm
    datatypes: List[DataType]


class AlgorithmID(BaseModel):
    id: PositiveInt
