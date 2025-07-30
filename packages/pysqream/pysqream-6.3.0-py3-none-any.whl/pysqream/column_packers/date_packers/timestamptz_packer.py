import operator
import functools
from pysqream.casting import pandas_timestamp_to_sq_datetime2
from struct import pack
from typing import Any, List
from pysqream.globals import TYPE_MAPPER
from pysqream.column_packers.column_packer import ColumnPacker, ColumnData
from pysqream.casting import sq_datetime2_to_pandas_timestamp


class TimestampTzPacker(ColumnPacker):
    """
    Packs datetime2 (ftTimestampTz) data type
    """

    def _pack_data(self, data: List[Any]) -> bytes:
        values = [pandas_timestamp_to_sq_datetime2(d) for d in data]
        packed = functools.reduce(operator.iconcat,
                                  (pack(TYPE_MAPPER.get_pack_code(self.metadata.col_type), *dt_tuple)
                                   for dt_tuple in values), [])

        return self.write_packed_data(packed)

    def unpack(self, column_data: ColumnData) -> List[Any]:
        self._cast_data_to_bytes(column_data)

        if self.metadata.nullable:
            col = [sq_datetime2_to_pandas_timestamp(column_data.data_column[idx:idx + 16], is_null=self._is_null(n))
                   for idx, n in zip(range(0, len(column_data.data_column), 16), column_data.nullable)]
        else:
            col = [sq_datetime2_to_pandas_timestamp(column_data.data_column[idx:idx + 16])
                   for idx in range(0, len(column_data.data_column), 16)]
        return col
