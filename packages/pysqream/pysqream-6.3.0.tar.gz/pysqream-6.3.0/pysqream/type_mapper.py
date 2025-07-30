import numbers
import numpy as np
import pandas as pd
from decimal import Decimal
from datetime import date, datetime


class TypeMapper:
    """
    type mapping class to handle every data type for pysqream
    """

    def __init__(self):
        self._type_definitions = {
            "ftBool": {
                "pack_code": "?",
                "typecode": "NUMBER",
                "python_types": (bool, np.bool_),
                "default": False
            },
            "ftUByte": {
                "pack_code": "B",
                "typecode": "NUMBER",
                "python_types": numbers.Integral,
                "default": 0
            },
            "ftShort": {
                "pack_code": "h",
                "typecode": "NUMBER",
                "python_types": numbers.Integral,
                "default": 0
            },
            "ftInt": {
                "pack_code": "i",
                "typecode": "NUMBER",
                "python_types": numbers.Integral,
                "default": 0
            },
            "ftLong": {
                "pack_code": "q",
                "typecode": "NUMBER",
                "python_types": numbers.Integral,
                "default": 0
            },
            "ftDouble": {
                "pack_code": "d",
                "typecode": "NUMBER",
                "python_types": numbers.Real,
                "default": 0.0
            },
            "ftFloat": {
                "pack_code": "f",
                "typecode": "NUMBER",
                "python_types": numbers.Real,
                "default": 0.0
            },
            "ftNumeric": {
                "pack_code": "4i",
                "typecode": "NUMBER",
                "python_types": (Decimal, numbers.Real),
                "default": Decimal("0")
            },
            "ftDate": {
                "pack_code": "i",
                "typecode": "DATETIME",
                "python_types": date,
                "default": None
            },
            "ftDateTime": {
                "pack_code": "q",
                "typecode": "DATETIME",
                "python_types": datetime,
                "default": None
            },
            "ftTimestampTz": {  # (datetime2)
                "pack_code": "4i",
                "typecode": "DATETIME",
                "python_types": pd.Timestamp,
                "default": None
            },
            "ftVarchar": {
                "pack_code": "s",
                "typecode": "STRING",
                "python_types": str,
                "default": lambda size: "".ljust(size, " ")
            },
            "ftBlob": {
                "pack_code": "s",
                "typecode": "STRING",
                "python_types": str,
                "default": ""
            },
            "ftArray": {
                "pack_code": None,
                "typecode": "ARRAY",
                "python_types": list,
                "default": None
            }
        }

    def get_pack_code(self, sqream_type: str):
        return self._type_definitions.get(sqream_type, {}).get("pack_code")

    def get_typecode(self, sqream_type: str):
        return self._type_definitions.get(sqream_type, {}).get("typecode")

    def get_python_types(self, sqream_type: str):
        return self._type_definitions.get(sqream_type, {}).get("python_types")

    def get_default_value(self, sqream_type: str, size: int = 0):
        default = self._type_definitions.get(sqream_type, {}).get("default")
        return default(size) if callable(default) else default
