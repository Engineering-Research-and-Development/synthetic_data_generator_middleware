from routers.generator.checks.files import (
    check_user_file,
)
from routers.generator.validation_schema import (
    SupportedDatatypesCategory,
    SupportedDatatypes,
    DatasetOutput,
)


def test_check_user_file_empty_input():
    result = check_user_file([])
    assert result == []


def test_check_user_file_single_int_column(monkeypatch):
    user_file = [
        {" col1 ": "1"},
        {" col1 ": "2"},
        {" col1 ": "3"},
    ]

    monkeypatch.setattr(
        "routers.generator.checks.files.try_parse_number",
        lambda v: int(v),
    )

    monkeypatch.setattr(
        "routers.generator.checks.files.estimate_column_type",
        lambda v: SupportedDatatypesCategory.primary_key,
    )

    monkeypatch.setattr(
        "routers.generator.checks.files.determine_column_datatype",
        lambda v: SupportedDatatypes.int,
    )

    result = check_user_file(user_file)

    assert len(result) == 1
    col = result[0]

    assert isinstance(col, DatasetOutput)
    assert col.column_name == "col1"
    assert col.column_data == [1, 2, 3]
    assert col.column_type == SupportedDatatypesCategory.primary_key
    assert col.column_datatype == SupportedDatatypes.int


def test_check_user_file_removes_empty_column(monkeypatch):
    user_file = [
        {"": "1", "a": "10"},
        {"": "2", "a": "20"},
    ]

    monkeypatch.setattr(
        "routers.generator.checks.files.try_parse_number",
        lambda v: int(v),
    )

    monkeypatch.setattr(
        "routers.generator.checks.files.estimate_column_type",
        lambda v: SupportedDatatypesCategory.continuous,
    )

    monkeypatch.setattr(
        "routers.generator.checks.files.determine_column_datatype",
        lambda v: SupportedDatatypes.int,
    )

    result = check_user_file(user_file)

    assert len(result) == 1
    assert result[0].column_name == "a"


def test_check_user_file_multiple_columns(monkeypatch):
    user_file = [
        {"a": "1", "b": "x"},
        {"a": "2", "b": "y"},
        {"a": "3", "b": "z"},
    ]

    monkeypatch.setattr(
        "routers.generator.checks.files.try_parse_number",
        lambda v: int(v) if v.isdigit() else v,
    )

    def mock_estimate(values):
        return (
            SupportedDatatypesCategory.primary_key
            if isinstance(values[0], int)
            else SupportedDatatypesCategory.categorical
        )

    def mock_determine(values):
        return (
            SupportedDatatypes.int
            if isinstance(values[0], int)
            else SupportedDatatypes.str
        )

    monkeypatch.setattr(
        "routers.generator.checks.files.estimate_column_type", mock_estimate
    )
    monkeypatch.setattr(
        "routers.generator.checks.files.determine_column_datatype", mock_determine
    )

    result = check_user_file(user_file)

    assert len(result) == 2

    col_a = next(c for c in result if c.column_name == "a")
    col_b = next(c for c in result if c.column_name == "b")

    assert col_a.column_data == [1, 2, 3]
    assert col_a.column_datatype == SupportedDatatypes.int

    assert col_b.column_data == ["x", "y", "z"]
    assert col_b.column_datatype == SupportedDatatypes.str
