from typing import List, Optional, Literal, Dict, Union

from pydantic import BaseModel, PositiveInt, Field, ConfigDict

from routers.generator.validation_schema.shared import (
    SupportedDatatypes,
    SupportedDatatypesCategory,
)


class ParametersInput(BaseModel):
    param_id: PositiveInt
    value: str


class FunctionParametersIn(BaseModel):
    function_id: PositiveInt
    parameters: List[ParametersInput] = Field(min_length=1)


class FunctionData(BaseModel):
    feature_name: str = Field(
        pattern="^[A-Za-z0-9._\\-]+$",
        description="The name of the feature to analyse",
        examples=["Column_name"],
    )
    associated_functions: List[FunctionParametersIn]


class AiModel(BaseModel):
    selected_model_id: PositiveInt
    new_model: Optional[bool] = False
    new_model_name: Optional[str] = Field(
        pattern="^[A-Za-z0-9._\\-]+$",
        description="The name of the new AI model",
        examples=["A name of a new model"],
        default=None,
    )
    model_version: Optional[str] = Field(
        pattern="^[A-Za-z0-9._\\-]+$",
        description="The name of the version of the AI model",
        examples=["v1"],
        default=None,
    )


class FeaturesCreated(BaseModel):
    name: str = Field(
        pattern="^[A-Za-z0-9._\\-]+$",
        description="The name of the feature to analyse",
        examples=["Column_name"],
    )
    type: SupportedDatatypes
    category: SupportedDatatypesCategory
    associated_functions: List[FunctionParametersIn]
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
