from database.schema import FunctionParameter, DataType, FunctionDataType


def _get_existing_function_ids():
    """
    Utility: retrieve at least one function id
    already present in the DB.
    """
    row = FunctionParameter.select().first()
    assert row is not None, "DB must be pre-populated with FunctionParameter"
    return [row.function.id]


def _get_existing_parameter_type():
    """
    Utility: retrieve a parameter_type already associated
    to a function.
    """
    dtype = DataType.select().join(FunctionDataType).first()
    assert dtype is not None
    return dtype.type
