from routers.generator.checks.files import determine_column_datatype
from routers.generator.validation_schema import SupportedDatatypes


def test_all_int_returns_int():
    values = [1, 2, 3, 4]
    result = determine_column_datatype(values)
    assert result == SupportedDatatypes.int


def test_all_float_returns_float():
    values = [1.0, 2.5, 3.14]
    result = determine_column_datatype(values)
    assert result == SupportedDatatypes.float


def test_all_string_returns_str():
    values = ["a", "b", "c"]
    result = determine_column_datatype(values)
    assert result == SupportedDatatypes.str


def test_mixed_int_and_float_returns_str():
    values = [1, 2.0, 3]
    result = determine_column_datatype(values)
    assert result == SupportedDatatypes.str


def test_mixed_string_and_int_returns_str():
    values = ["1", 2, "3"]
    result = determine_column_datatype(values)
    assert result == SupportedDatatypes.str


def test_single_int_value():
    values = [42]
    result = determine_column_datatype(values)
    assert result == SupportedDatatypes.int


def test_single_float_value():
    values = [3.14]
    result = determine_column_datatype(values)
    assert result == SupportedDatatypes.float
