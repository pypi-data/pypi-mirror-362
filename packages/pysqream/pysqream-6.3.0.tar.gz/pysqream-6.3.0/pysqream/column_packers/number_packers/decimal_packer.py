import operator
import functools
from decimal import Decimal
from typing import Union, List, Any
from pysqream.casting import decimal_to_sq_numeric
from pysqream.column_packers.column_packer import ColumnPacker, ColumnData
from pysqream.casting import sq_numeric_to_decimal


class DecimalPacker(ColumnPacker):
    """
    Packs decimal/numeric types
    """

    def _pack_data(self, data: List[Union[Decimal, str]]) -> bytes:
        values = [decimal_to_sq_numeric(Decimal(n), self.metadata.scale)
                  for n in data]
        packed = functools.reduce(operator.iconcat,
                                  (num.to_bytes(16, byteorder='little', signed=True)
                                   for num in values), [])
        return self.write_packed_data(packed)

    def unpack(self, column_data: ColumnData) -> List[Any]:
        self._cast_data_to_bytes(column_data)
        scale = self.metadata.scale

        if self.metadata.nullable:
            col = [
                sq_numeric_to_decimal(column_data.data_column[idx:idx + 16], scale, is_null=self._is_null(n))
                for idx, n in zip(range(0, len(column_data.data_column), 16), column_data.nullable)
            ]
        else:
            col = [
                sq_numeric_to_decimal(column_data.data_column[idx:idx + 16], scale)
                for idx in range(0, len(column_data.data_column), 16)
            ]
        return col
