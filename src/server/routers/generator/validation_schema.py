from enum import Enum
from typing import List, Optional, Dict, Literal, Union

from pydantic import BaseModel, PositiveInt, Field, ConfigDict


class ParametersInput(BaseModel):
    param_id: PositiveInt
    value: str | float


class FunctionData(BaseModel):
    feature: str = Field(
        pattern="^[A-Za-z0-9._\-]+$",
        description="The name of the feature to analyse",
        examples=["Column_name"],
    )
    function_id: PositiveInt
    parameters: List[ParametersInput] = Field(min_length=1)


class AiModel(BaseModel):
    selected_model_id: PositiveInt
    new_model: Optional[bool] = False
    new_model_name: Optional[str] = Field(
        pattern="^[A-Za-z0-9._\-]+$",
        description="The name of the new AI model",
        examples=["A name of a new model"],
        default=None,
    )
    model_version: Optional[str] = Field(
        pattern="^[A-Za-z0-9._\-]+$",
        description="The name of the version of the AI model",
        examples=["v1"],
        default=None,
    )


class SupportedDatatypes(str, Enum):
    float = "float32"
    int = "int32"
    str = "str"


class SupportedDatatypesCategory(str, Enum):
    continuous = "continuous"
    categorical = "categorical"
    primary_key = "primary_key"
    group_index = "group_index"


class SupportedDataset(str, Enum):
    table = ("table",)
    time_series = "time_series"


class FeaturesCreated(BaseModel):
    feature: str = Field(
        pattern="^[A-Za-z0-9._\-]+$",
        description="The name of the feature to analyse",
        examples=["Column_name"],
    )
    type: SupportedDatatypes
    category: SupportedDatatypesCategory

    model_config = ConfigDict(use_enum_values=True)


class UserFileInput(BaseModel):
    input_type: Literal["user_file"]
    user_file: List[Dict] = Field(min_length=1)
    ai_model: AiModel
    functions: Optional[List[FunctionData]] = None


class FeaturesCreatedInput(BaseModel):
    input_type: Literal["features_created"]
    features_created: List[FeaturesCreated] = Field(min_length=1)
    functions: List[FunctionData]


class UserFeatureInfo(BaseModel):
    type: str


class UserDataInput(BaseModel):
    additional_rows: PositiveInt
    data: Union[UserFileInput, FeaturesCreatedInput] = Field(discriminator="input_type")
    # data: Union[UserFileInput] = Field(discriminator="input_type")
    feature_types: Optional[Dict[str, UserFeatureInfo]] = Field(default=None)


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


"""
TODO: Implement DatasetOutput as a list of DataOutput objects and a dataset_type
class DatasetOutput(BaseModel):
    dataset_type: SupportedDataset
    data: List[DataOutput]

    class Config:
        use_enum_values = True
"""


class ParametersOut(BaseModel):
    name: str
    value: str
    parameter_type: str


class FunctionDataOut(BaseModel):
    feature: str = Field(
        pattern="^[A-Za-z0-9._\-]+$",
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
