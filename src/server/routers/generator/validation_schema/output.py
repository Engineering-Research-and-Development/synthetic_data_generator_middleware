from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from routers.generator.validation_schema.shared import (
    SupportedDatatypesCategory,
    SupportedDatatypes,
)


class TrainingDataInfo(BaseModel):
    column_name: str
    column_type: str
    column_datatype: str
    column_size: str
    column_position: int


class ModelOutput(BaseModel):
    algorithm_name: str
    model_name: str
    input_shape: Optional[str] = None
    image: Optional[str] = None
    training_data_info: Optional[List[TrainingDataInfo]] = None


class DatasetOutput(BaseModel):
    column_data: List[float | int | str]
    column_name: str
    column_type: SupportedDatatypesCategory
    column_datatype: SupportedDatatypes
    model_config = ConfigDict(use_enum_values=True)


class ParametersOut(BaseModel):
    name: str
    value: str
    parameter_type: str


class FunctionDataOut(BaseModel):
    feature: str = Field(
        pattern="^[A-Za-z0-9._\\-]+$",
        description="The name of the feature to analyse",
        examples=["Column_name"],
    )
    function_reference: str
    parameters: List[ParametersOut]


class GeneratorFunctionOut(BaseModel):
    functions: List[FunctionDataOut]
    n_rows: PositiveInt


class GeneratorDataOutput(BaseModel):
    functions: Optional[List[FunctionDataOut]] = []
    model: ModelOutput
    n_rows: PositiveInt
    dataset: List[DatasetOutput] | None = None


class GeneratorResponse(BaseModel):
    doc_id: str


"""
TODO: Implement DatasetOutput as a list of DataOutput objects and a dataset_type
class DatasetOutput(BaseModel):
    dataset_type: SupportedDataset
    data: List[DataOutput]

    class Config:
        use_enum_values = True
"""
