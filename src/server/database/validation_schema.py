from pydantic import BaseModel, Field, PositiveInt


# Database mapping 1:1
class Algorithm(BaseModel):
    _id: PositiveInt
    name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A name of an algorithm"],
    )
    description: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A description of an algorithm"],
    )
    default_loss_function: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a loss function"],
    )


class DataType(BaseModel):
    _id: PositiveInt
    type: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The type of a datatype"],
    )
    is_categorical: bool


class AlgorithmDataType(BaseModel):
    _id: PositiveInt
    _algorithm: PositiveInt
    _datatype: PositiveInt


class TrainedModel(BaseModel):
    _id: PositiveInt
    name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a trained model"],
    )
    dataset_name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a dataset"],
    )
    size: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The size of a dataset"],
    )
    input_shape: str = Field(
        pattern=r"\([0-9]+,(([0-9]+,?)+)?\)",
        description="The shape of the input that must be in the format of (number,...,number)",
        examples=["(1,3,200,200)"],
    )
    _algorithm: PositiveInt


class TrainModelDatatype(BaseModel):
    _id: PositiveInt
    feature_name: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["The name of a feature"],
    )
    feature_position: int
    feature_size: str
    feature_type: str
    _datatype: PositiveInt
    _trained_model: PositiveInt


class ModelVersion(BaseModel):
    _id: PositiveInt
    version_name: str
    image_path: str
    loss_function: str = Field(
        pattern="^[^ ](.*[^ ])?$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["A loss function"],
    )
    train_loss: float
    val_loss: float
    train_samples: int
    val_samples: int
    _trained_model: PositiveInt


## FUNCTIONS PYDANTIC MODELS
class Function(BaseModel):
    _id: PositiveInt
    name: str
    description: str
    function_reference: str


class Parameter(BaseModel):
    _id: PositiveInt
    name: str
    value: str
    parameter_type: str


class FunctionParameter(BaseModel):
    function: PositiveInt
    parameter: PositiveInt
