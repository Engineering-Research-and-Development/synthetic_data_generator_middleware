from enum import Enum


class SupportedDatatypes(str, Enum):
    float = "float32"
    int = "int32"
    str = "str"
    bool = "bool"


class SupportedDatatypesCategory(str, Enum):
    continuous = "continuous"
    categorical = "categorical"
    primary_key = "primary_key"
    group_index = "group_index"


class SupportedDataset(str, Enum):
    table = ("table",)
    time_series = "time_series"
