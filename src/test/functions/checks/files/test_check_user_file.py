from routers.generator.checks.files import check_user_file
from routers.generator.validation_schema import (
    SupportedDatatypes,
)


def test_check_user_file_empty():
    assert check_user_file([]) == []


def test_check_user_file_parsing_and_cleaning():
    user_file = [
        {" col1 ": "1", " col2 ": "a"},
        {" col1 ": "2", " col2 ": "b"},
    ]

    result = check_user_file(user_file)

    assert len(result) == 2

    col1 = next(r for r in result if r.column_name == "col1")
    assert col1.column_data == [1, 2]
    assert col1.column_datatype == SupportedDatatypes.int

    col2 = next(r for r in result if r.column_name == "col2")
    assert col2.column_data == ["a", "b"]
    assert col2.column_datatype == SupportedDatatypes.str


def test_check_user_file_removes_empty_column():
    user_file = [
        {" ": "1", "x": "2"},
        {" ": "3", "x": "4"},
    ]

    result = check_user_file(user_file)

    assert len(result) == 1
    assert result[0].column_name == "x"
