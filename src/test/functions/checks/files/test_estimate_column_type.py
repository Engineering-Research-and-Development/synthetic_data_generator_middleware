from routers.generator.checks.files import estimate_column_type
from routers.generator.validation_schema.shared import SupportedDatatypesCategory


def test_primary_key_all_unique():
    values = ["1", "2", "3", "4", "5"]
    result = estimate_column_type(values)
    assert result == SupportedDatatypesCategory.primary_key


def test_int_continuous_large_representation():
    # 6 valori, 4 unici → 4/6 ≈ 0.66 > 0.5
    values = [1, 2, 3, 4, 1, 2]
    result = estimate_column_type(values)
    assert result == SupportedDatatypesCategory.continuous


def test_int_group_index():
    # Contiguous, equal repetition, group index ratio
    values = [1, 1, 2, 2, 3, 3]
    # unique = 3, total = 6
    # contiguous: True
    # just_equal: True
    # group_index_representation: True (0.01 < 0.5 <= 0.5)
    result = estimate_column_type(values)
    assert result == SupportedDatatypesCategory.group_index


def test_int_categorical_low_score():
    # Non contiguous
    values = [1] * 100 + [3] * 100 + [2] * 100
    result = estimate_column_type(values)
    assert result == SupportedDatatypesCategory.categorical


def test_float_continuous():
    values = [0.1, 0.2, 0.3, 0.4]
    result = estimate_column_type(values)
    assert result == SupportedDatatypesCategory.continuous


def test_string_categorical():
    values = ["a", "b", "a", "c"]
    result = estimate_column_type(values)
    assert result == SupportedDatatypesCategory.categorical


def test_mixed_types_fallback():
    values = [1, "a", 2]
    result = estimate_column_type(values)
    assert result == SupportedDatatypesCategory.categorical


def test_single_value_primary_key():
    values = ["42"]
    result = estimate_column_type(values)
    assert result == SupportedDatatypesCategory.primary_key
