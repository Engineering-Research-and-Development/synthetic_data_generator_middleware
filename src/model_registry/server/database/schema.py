import os

from peewee import (
    PostgresqlDatabase,
    Model,
    AutoField,
    CharField,
    BooleanField,
    ForeignKeyField,
    IntegerField,
    DoubleField,
    SQL,
    CompositeKey,
)

username = os.environ.get("POSTGRES_USER", "postgres")
password = os.environ.get("POSTGRES_PASSWORD", "postgres")
host = os.environ.get("POSTGRES_HOST", "127.0.0.1")
database = os.environ.get("POSTGRES_DB", "postgres")
port = os.environ.get("POSTGRES_PORT", 5432)
db = PostgresqlDatabase(
    database=database, host=host, user=username, password=password, port=port
)


class BaseModelPeewee(Model):
    class Meta:
        database = db


class Algorithm(BaseModelPeewee):
    id = AutoField()
    name = CharField(unique=True)
    description = CharField()
    default_loss_function = CharField()


class DataType(BaseModelPeewee):
    id = AutoField()
    type = CharField()
    is_categorical = BooleanField()

    class Meta:
        constraints = [SQL('UNIQUE("type", "is_categorical")')]


class AlgorithmDataType(BaseModelPeewee):
    id = AutoField()
    algorithm = ForeignKeyField(
        Algorithm, backref="allowed_data_types", on_delete="CASCADE"
    )
    datatype = ForeignKeyField(DataType, backref="allowed_data_types")


class TrainedModel(BaseModelPeewee):
    id = AutoField()
    name = CharField()
    dataset_name = CharField()
    size = CharField()
    input_shape = CharField()
    algorithm = ForeignKeyField(
        Algorithm, backref="trained_models", on_delete="CASCADE"
    )


class TrainModelDatatype(BaseModelPeewee):
    id = AutoField()
    feature_name = CharField()
    feature_position = IntegerField()
    feature_size = CharField()
    datatype = ForeignKeyField(DataType, backref="trained_model_datatype")
    trained_model = ForeignKeyField(
        TrainedModel, backref="trained_model_datatype", on_delete="CASCADE"
    )


class ModelVersion(BaseModelPeewee):
    id = AutoField()
    version_name = CharField()
    image_path = CharField()
    loss_function = CharField()
    train_loss = DoubleField()
    val_loss = DoubleField()
    train_samples = IntegerField()
    val_samples = IntegerField()
    trained_model = ForeignKeyField(
        TrainedModel, backref="model_versions", on_delete="CASCADE"
    )


######
class Function(BaseModelPeewee):
    id = AutoField()
    name = CharField()
    description = CharField()
    function_reference = CharField()


class Parameter(BaseModelPeewee):
    id = AutoField()
    name = CharField()
    value = CharField()
    parameter_type = (
        CharField()
    )  # constraints=[SQL("CHECK (parameter_type IN ('float'))")])


class FunctionParameter(BaseModelPeewee):
    function = ForeignKeyField(
        Function, backref="function_parameters", on_delete="CASCADE"
    )
    parameter = ForeignKeyField(
        Parameter, backref="function_parameters", on_delete="CASCADE"
    )

    class Meta:
        primary_key = CompositeKey("function", "parameter")
