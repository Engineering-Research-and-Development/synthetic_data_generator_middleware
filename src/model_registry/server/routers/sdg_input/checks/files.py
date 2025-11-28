import polars as pl
from typing import Union
from routers.sdg_input.validation_schema import (
    SupportedDatatypes,
    DatasetOutput,
    GeneratorDataOutput,
    FunctionDataOut, SupportedDataset,
)
import json


def try_parse_number(value: str) -> Union[int, float, str]:
    value = value.strip()
    try:
        int_val = int(value)
        return int_val
    except ValueError:
        try:
            float_val = float(value)
            return float_val
        except ValueError:
            return value


def determine_column_type(values: list) -> str:
    set_to_list_percentage = len(set(values)) / len(values)
    if all(isinstance(v, int) for v in values):
        if set_to_list_percentage < 0.1:
            return "categorical"
        elif 0.1 < set_to_list_percentage < 0.6:
            return "group_index"
        return "continuous"
    elif all(isinstance(v, float)for v in values):
        return "continuous"
    elif all(isinstance(v, str) for v in values):
        if set_to_list_percentage < 1:
            return "categorical"
        return "primary_key"
    return "categorical"


def determine_column_datatype(values: list) -> SupportedDatatypes:
    if all(isinstance(v, int) for v in values):
        return SupportedDatatypes.int
    elif all(isinstance(v, float) for v in values):
        return SupportedDatatypes.float
    return SupportedDatatypes.str


def determine_dataset_type(col_type_names: str) -> SupportedDataset:
    if "group_index" in col_type_names:
        return SupportedDataset.time_series
    return SupportedDataset.table

def check_user_file(user_file: list[dict]) -> list[DatasetOutput]:
    if not user_file:
        return []

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

    outputs = []
    for col in df.columns:
        values = df[col].to_list()
        if all(isinstance(v, str) for v in values):
            values = [json.loads(v) for v in values]
        outputs.append(
            DatasetOutput(
                column_data=values,
                column_name=col,
                column_type=determine_column_type(values),
                column_datatype=determine_column_datatype(values),
            )
        )

    return outputs


def handle_user_file(
    data: dict, function_data: list[FunctionDataOut] | None, model
) -> (GeneratorDataOutput, str):
    """
    Create the GeneratorDataOutput object from the user file

    :param data: the dictionary containing the input data
    :param function_data: the list of functions to pass to the generator
    :param model: the chosen AI model
    :return: the GeneratorDataOutput object or an error message
    """
    user_file = check_user_file(data.get("user_file"))
    if not user_file:
        return None, "Error parsing input dataset"

    return (
        GeneratorDataOutput(
            functions=function_data,
            n_rows=data.get("additional_rows"),
            model=model,
            dataset=user_file,
        ),
        "",
    )
