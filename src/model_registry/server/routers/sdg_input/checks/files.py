import polars as pl
from typing import Union
from routers.sdg_input.validation_schema import (
    SupportedDatatypes,
    DatasetOutput,
    GeneratorDataOutput,
    FunctionDataOut,
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
    if all(isinstance(v, (int, float)) for v in values):
        return "continuous"
    elif all(isinstance(v, list) for v in values):
        return "time_series"
    else:
        return "categorical"


def determine_column_datatype(values: list) -> SupportedDatatypes:
    if all(isinstance(v, (int, float)) for v in values):
        return SupportedDatatypes.int
    return SupportedDatatypes.float


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
