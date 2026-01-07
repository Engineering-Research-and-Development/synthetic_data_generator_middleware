from typing import List
from pydantic import BaseModel, PositiveInt
from database.validation_schema import Function, Parameter


class FunctionId(Function):
    id: PositiveInt


class FunctionParameterOut(BaseModel):
    function: Function
    parameters: List[Parameter]


class FunctionOut(BaseModel):
    function: FunctionId


class FunctionParameterIn(BaseModel):
    function: Function
    parameters: List[Parameter]
