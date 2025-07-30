from pysqream.casting import datetime_to_long, sq_datetime_to_py_datetime
from typing import Any
from pysqream.column_packers.date_packers.abstract_date_packer import AbstractDatePacker


class DateTimePacker(AbstractDatePacker):
    """
    Packs datetime data type
    """

    def _transform_value(self, value: Any) -> int:
        return datetime_to_long(value)

    def _backward_transform_value(self, value: Any, is_null: bool = False) -> Any:
        return sq_datetime_to_py_datetime(value, is_null=is_null)
