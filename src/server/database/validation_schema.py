from pydantic import BaseModel, Field, PositiveInt, StrictBool, StrictInt, StrictFloat, NonNegativeInt


# Database mapping 1:1
class Algorithm(BaseModel):
    _id: PositiveInt
    name: str = Field(
        pattern="^[A-Za-z0-9._-]+$",
        description="A name of an algorithm",
        examples=["VAE"],
    )
    description: str = Field(
        pattern="^[A-Za-z0-9._- ]+$",
        description="A description of an algorithm",
        examples=["Variational Auto Encoder"],
    )
    default_loss_function: str = Field(
        pattern="^[A-Za-z0-9._- ]+$",
        description="The name of a loss function",
        examples=["Mean Squared Error"],
    )


class DataType(BaseModel):
    _id: PositiveInt
    type: str = Field(
        pattern="^[A-Za-z0-9]+$",
        description="Describe the type of the Datatype",
        examples=["integer", "float", "string"],
    )
    is_categorical: StrictBool


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
        pattern="^[A-Za-z0-9._-]+$",
        description="This field does NOT allow strings that"
        " start or end with spaces or are empty",
        examples=["petal_length"],
    )
    feature_position: NonNegativeInt = Field(description="The position of the feature", examples=[1])
    feature_size: str = Field(pattern="^[A-Za-z0-9._-(),]+$", examples=["(28,28,1)"])
    feature_type: str = Field(pattern="^[A-Za-z0-9._-()]+$")
    _datatype: PositiveInt
    _trained_model: PositiveInt


class ModelVersion(BaseModel):
    _id: PositiveInt
    version_name: str
    image_path: str
    loss_function: str = Field(
        pattern="^[A-Za-z0-9._-]+$",
        description="Describe the loss function used",
        examples=["MSE"],
    )
    train_loss: StrictFloat
    val_loss: StrictFloat
    train_samples: StrictInt
    val_samples: StrictInt
    _trained_model: PositiveInt


## FUNCTIONS PYDANTIC MODELS
class Function(BaseModel):
    _id: PositiveInt
    name: str = Field(pattern="^[A-Za-z0-9._-]+$", examples=["Normalize"])
    description: str = Field(
        pattern="^[A-Za-z0-9._\\- +_*=()^:]+$",
        examples=["Generates data using the formula ax^2+bx*c"],
    )
    function_reference: str = Field(
        pattern="^[A-Za-z0-9._-]+$", examples=["lib.normalize"]
    )
    priority: PositiveInt
    is_generative: StrictBool


class Parameter(BaseModel):
    _id: PositiveInt
    name: str = Field(pattern="^[a-z0-9._-]+$", examples=["drop_null"])
    value: str = Field(pattern="^[A-Za-z0-9._-,()]+$", examples=["True"])
    parameter_type: str = Field(pattern="^[A-Za-z0-9._-]+$", examples=["Boolean"])


class FunctionParameter(BaseModel):
    function: PositiveInt
    parameter: PositiveInt
