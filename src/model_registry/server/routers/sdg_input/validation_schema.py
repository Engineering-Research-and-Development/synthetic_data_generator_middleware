from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel, PositiveInt, model_validator, Field


class ParametersInput(BaseModel):
    param_id: PositiveInt
    value: str | float


class FunctionData(BaseModel):
    feature: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A feature name"],
    )
    function_id: PositiveInt
    parameters: List[ParametersInput]


class AiModel(BaseModel):
    selected_model_id: PositiveInt
    new_model: Optional[bool] = False
    new_model_name: Optional[str] = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="The name of the new AI model.\n"
        "This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A name of a new model"],
        default=None,
    )
    model_version: Optional[str] = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="The name of the version of the AI model.\n"
        "This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a version"],
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
    feature: str
    type: SupportedDatatypes
    category: SupportedDatatypesCategory

    class Config:
        use_enum_values = True


class UserDataInput(BaseModel):
    additional_rows: PositiveInt
    functions: Optional[List[FunctionData]] = None
    ai_model: AiModel
    user_file: Optional[List[Dict]] = Field(
        default=None, description="The representation of key-value of the data content"
    )
    features_created: Optional[List[FeaturesCreated]] = None

    @model_validator(mode="after")
    def validate_either_present(self):
        if (self.user_file is None) != (self.features_created is None):
            return self
        else:
            raise ValueError(
                "Either 'user_file' or 'features_created' must be provided. Not both"
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

    class Config:
        use_enum_values = True


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
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A feature name"],
    )
    function_reference: str
    parameters: List[ParametersOut]


class GeneratorDataOutput(BaseModel):
    functions: Optional[List[FunctionDataOut]] = []
    model: ModelOutput
    n_rows: PositiveInt
    dataset: List[DatasetOutput] | None = None


class GeneratorResponse(BaseModel):
    doc_id: str
