from struct import pack_into
from typing import Any, List
from pysqream.globals import TYPE_MAPPER
from pysqream.column_packers.column_packer import ColumnPacker, ColumnData


class NumberPacker(ColumnPacker):
    """
    Packs all numbers data types except for decimal(numeric)
    """

    def _pack_data(self, data: List[Any]) -> bytes:
        pack_into(f'{len(data)}{TYPE_MAPPER.get_pack_code(self.metadata.col_type)}',
                  memoryview(self.buf_map), self.buf_idx, *data)

        return self.buf_map[:self.buf_idx + len(data) * self.metadata.size]

    def unpack(self, column_data: ColumnData) -> List[Any]:
        self._cast_data_by_pack_code(column_data)
        unpacked_data = [None if self._is_null(n) else d for d, n in zip(column_data.data_column, column_data.nullable)] if self.metadata.nullable \
            else column_data.data_column

        if self.metadata.nullable:
            null_mask = [self._is_null(x) for x in column_data.nullable]
            return [None if is_null else value
                    for is_null, value in zip(null_mask, unpacked_data)]

        return unpacked_data
