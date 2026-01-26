import polars as pl
from typing import Union
from routers.generator.validation_schema.shared import (
    SupportedDatatypes,
    SupportedDatatypesCategory,
)
from routers.generator.validation_schema.output import DatasetOutput

GROUP_INDEX_THRESHOLD = 0.5
CATEGORICAL_THRESHOLD = 0.1


def try_parse_number(value: str | int | float) -> Union[int, float, str]:
    if type(value) is str:
        value = value.strip()
    else:
        return value
    try:
        int_val = int(value)
        return int_val
    except ValueError:
        try:
            float_val = float(value)
            return float_val
        except ValueError:
            return value


def list_type_uniform(values: list) -> bool:
    type_zero = type(values[0])
    if all(isinstance(v, type_zero) for v in values):
        return True
    return False


def estimate_column_type(values: list) -> SupportedDatatypesCategory:
    total_values = len(values)
    n_unique_values = len(set(values))
    set_to_list_percentage = n_unique_values / total_values

    # A primary Key is a column with unique values, only string allowed
    if (
        set_to_list_percentage == 1
        and list_type_uniform(values)
        and all(isinstance(v, str) for v in values)
    ):
        return SupportedDatatypesCategory.primary_key

    # Integers are either group index or continuous or categorical based on specific conditions
    if all(isinstance(v, int) for v in values):
        is_contiguous = values == sorted(values)
        is_just_equal = total_values % n_unique_values == 0
        has_group_index_representation = set_to_list_percentage <= GROUP_INDEX_THRESHOLD
        has_categorical_representation = set_to_list_percentage < CATEGORICAL_THRESHOLD
        if is_contiguous and is_just_equal and has_group_index_representation:
            return SupportedDatatypesCategory.group_index
        elif has_categorical_representation:
            return SupportedDatatypesCategory.categorical
        return SupportedDatatypesCategory.continuous

    elif all(isinstance(v, float) for v in values):
        return SupportedDatatypesCategory.continuous

    elif all(isinstance(v, str) for v in values):
        return SupportedDatatypesCategory.categorical

    return SupportedDatatypesCategory.categorical


def determine_column_datatype(values: list) -> SupportedDatatypes:
    if all(isinstance(v, int) for v in values):
        return SupportedDatatypes.int
    elif all(isinstance(v, float) for v in values):
        return SupportedDatatypes.float
    return SupportedDatatypes.str


def check_user_file(
    user_file: list[dict], feature_types: dict | None
) -> list[DatasetOutput]:
    # Clean keys and parse values
    parsed_data = {}
    for row in user_file:
        for key, val in row.items():
            clean_key = key.strip()
            parsed_data.setdefault(clean_key, []).append(try_parse_number(val))

    # Create Polars DataFrame
    df = pl.DataFrame(parsed_data)

    # Remove empty columns
    if "" in df.columns:
        df = df.drop("")

    if not feature_types:
        feature_types = {}

    outputs = []
    for col in df.columns:
        values = df[col].to_list()
        feature_type = feature_types.get(col, None)
        feature_type = (
            estimate_column_type(values)
            if feature_type is None
            else SupportedDatatypesCategory(feature_type.get("type"))
        )
        outputs.append(
            DatasetOutput(
                column_data=values,
                column_name=col,
                column_type=feature_type,
                column_datatype=determine_column_datatype(values),
            )
        )

    return outputs
