from typing import Any
from pysqream.casting import date_to_int, sq_date_to_py_date
from pysqream.column_packers.date_packers.abstract_date_packer import AbstractDatePacker


class DatePacker(AbstractDatePacker):
    """
    Packs date data type
    """

    def _transform_value(self, value: Any) -> int:
        return date_to_int(value)

    def _backward_transform_value(self, value: Any, is_null: bool = False) -> Any:
        return sq_date_to_py_date(value, is_null=is_null)
