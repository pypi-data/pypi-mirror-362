#!/usr/bin/env python
# -*- coding: utf-8 -*-

__docformat__ = "NumPy"
__author__ = "Lukas Gold, Simon Stier"

from abc import abstractmethod
from enum import Enum

# Python version dependent import statements:
try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum

from pathlib import Path
from typing import Any

# other modules
import pandas as pd
from pydantic import BaseModel, ConfigDict, field_validator
from typing_extensions import Callable, Dict, List, Literal, Optional, Union


# Classes
class Separator(StrEnum):
    comma = ","
    point = "."
    semicolon = ";"
    tab = "\t"
    space = " "
    newline = "\n"


class DecimalSeparator(StrEnum):
    comma = ","
    point = "."


class ThousandsSeparator(Enum):
    apostrophe = "'"
    comma = ","
    none = None
    point = "."


class Encoding(Enum):
    none = None
    utf8 = "utf-8"
    latin1 = "latin1"
    ascii = "ascii"
    cp1252 = "cp1252"
    iso8859_1 = "iso-8859-1"


class DataFormat(StrEnum):
    raw = "raw"
    txt = "txt"


class ReadTableResult(BaseModel):
    file_path: Union[str, Path]
    meta: dict
    data: "TabularData"

    @field_validator("file_path")
    def check_file_path(cls, v):
        if not Path(v).exists():
            raise ValueError(f"File '{v}' does not exist!")
        return v


class TabularData(BaseModel):
    as_list: List[Dict[str, Any]]
    as_dataframe: Optional[pd.DataFrame] = None
    data_format: DataFormat

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.as_dataframe = self.to_dataframe()

    def to_dataframe(self):
        return pd.DataFrame(self.as_list)

    # avoiding black reformatting
    # fmt: off
    @abstractmethod
    def change_column_names(self, target_format: DataFormat):
        ...
    # fmt: on


ReadTableResult.model_rebuild()


class ReadFileParameter(BaseModel):
    # todo: add date time format and apply
    decimal: DecimalSeparator
    thousands: ThousandsSeparator
    encoding: Encoding
    header: Union[int, Callable]
    skiprows: int
    index_col: Union[Any, Literal[False], None]  # IndexLabel,
    usecols: Any  # UsecolsArgType
    column_names: Union[List[str], Callable]
    skip_blank_lines: bool
    apply_to_cols: Dict[int, Callable] = {}  # {column: function}
    exclude_from_params: List[str] = ["apply_to_cols", "exclude_from_params"]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        for key in ["apply_to_cols", "exclude_from_params"]:
            if key not in self.exclude_from_params:
                self.exclude_from_params.append(key)
