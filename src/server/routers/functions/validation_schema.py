from typing import List
from pydantic import BaseModel, PositiveInt
from database.validation_schema import Function, Parameter, DataType


class FunctionId(Function):
    id: PositiveInt


class ParameterId(Parameter):
    id: PositiveInt


class DataTypeId(DataType):
    id: PositiveInt


class FunctionParameterDataTypeOut(BaseModel):
    function: Function
    parameters: List[ParameterId]
    datatypes: List[DataTypeId]


class FunctionOut(BaseModel):
    function: FunctionId


class FunctionParameterDataTypeIn(BaseModel):
    function: Function
    parameters: List[Parameter]
    datatypes: List[DataType]
